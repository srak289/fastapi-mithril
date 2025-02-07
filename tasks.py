import json

from invoke import task, call
from pathlib import Path
from hashlib import sha256

fp_conf_hash = Path("oci/nginx/.nginx.conf.sha256")
fp_cf_hash = Path("oci/nginx/.Containerfile.sha256")
d_content = None

@task
def nginx_vol(c):
    global d_content
    r = c.run("podman volume inspect content", warn=True)
    if r.exited not in (0, 125):
        breakpoint()
    if r.exited == 0:
        vol = json.loads(r.stdout)
        if vol:
            vol = vol[0]
            d_content = vol["Mountpoint"]
            return
    c.run("podman volume create content")

@task
def nginx_img(c):
    conf_hash = None
    cf_hash = None

    if fp_cf_hash.is_file():
        cf_hash = fp_cf_hash.read_text()
    cur_cf_hash = sha256(Path("oci/nginx/Containerfile").read_bytes()).hexdigest()

    if fp_conf_hash.is_file():
        conf_hash = fp_conf_hash.read_text()
    cur_conf_hash = sha256(Path("oci/nginx/nginx.conf").read_bytes()).hexdigest()

    if (
        cur_conf_hash == conf_hash
        and cur_cf_hash == cf_hash
    ):
        return
    print("Mismatch!")
    fp_cf_hash.write_text(cur_cf_hash)
    fp_conf_hash.write_text(cur_conf_hash)
    print("Regenerating nginx")
    c.run("podman build -t proxy:latest -f oci/nginx/Containerfile")

@task(pre=[nginx_vol], aliases=["content"])
def nginx_content(c):
    if d_content == None:
        print(f"ERROR: d_content is 'None'")
        breakpoint()
    c.run(f"rsync --no-compress -a -d static/ {d_content}")

@task(pre=[nginx_img, nginx_content], aliases=["proxy"])
def nginx(c):
    r = c.run("podman ps -q -f name=nginx")
    if r.stdout != "":
        return
    c.run("podman run -d --rm "
        "--name nginx "
        "--network=host "
        "-v content:/usr/share/nginx/html:ro,Z "
        "localhost/proxy:latest",
        warn=True
    )

@task(post=[nginx])
def restart(c):
    c.run("podman stop nginx", warn=True)

@task
def server(c):
    c.run("uvicorn --reload main:app", pty=True)

@task
def postgres(c):
    c.run("""podman run -d --rm --name test 
-e "POSTGRES_ADMIN=admin" 
-e "POSTGRES_PASSWORD=admin" 
-e "POSTGRES_DATABASE=test" 
docker.io/library/postgres:latest""")

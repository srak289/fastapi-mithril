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

    r = c.run("podman image ls -q -f label=proxy")
    force = False
    if r.stdout == "": force = True

    cur_cf_hash = sha256(Path("oci/nginx/Containerfile").read_bytes()).hexdigest()
    cur_conf_hash = sha256(Path("oci/nginx/nginx.conf").read_bytes()).hexdigest()

    if not force:
        if fp_cf_hash.is_file():
            cf_hash = fp_cf_hash.read_text()

        if fp_conf_hash.is_file():
            conf_hash = fp_conf_hash.read_text()

        if (
            cur_conf_hash == conf_hash
            and cur_cf_hash == cf_hash
        ):
            return

    fp_cf_hash.write_text(cur_cf_hash)
    fp_conf_hash.write_text(cur_conf_hash)

    print("Building proxy image...")

    c.run("podman build -t proxy:latest -f oci/nginx/Containerfile")

@task(pre=[nginx_vol], aliases=["content"])
def nginx_content(c):
    if d_content == None:
        print(f"ERROR: d_content is 'None'")
        breakpoint()
    c.run(f"rsync --no-compress -a -d static/ {d_content}")

@task(pre=[nginx_img, nginx_content], aliases=["proxy"], optional=["local"])
def nginx(c, local=None):
    r = c.run("podman ps -q -f name=nginx")
    if r.stdout != "":
        return

    cmd = ["podman run -d --rm",
        "--name nginx",
        "-v content:/usr/share/nginx/html:ro,Z",
    ]
    if local:
        print("Adding local args")
        cmd += ["-p 8080:80 -p 8443:443"]
    else:
        print("Adding production args")
        cmd += ["--network=host"]
    cmd += ["localhost/proxy:latest"]
        
    cmd = " ".join(cmd)
    c.run(cmd, warn=True)

@task(pre=[nginx_vol])
def sync(c):
    c.run(f"for((;;)); do echo 'Syncing'; rsync --no-compress --delete -r static/ {d_content}; echo 'Done!'; sleep 2; done")

@task(post=[nginx])
def restart(c):
    c.run("podman stop nginx", warn=True)

@task
def server(c):
    c.run("uvicorn --reload main:app", pty=True)

@task
def fetch_js(c):
    for k, v in {
        "mithril.min.js": "https://cdnjs.cloudflare.com/ajax/libs/mithril/2.2.12/mithril.min.js",
        "cytoscape.esm.min.mjs": "https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.4/cytoscape.esm.min.mjs",
    }.items():
        if not Path(f"static/js/{k}").is_file():
            print(f"Fetching {v}")
            c.run(f"wget {v} -O static/js/{k}")
        else:
            print(f"Already fetched {k}")

@task
def snakeoil(c):
    certs = Path("oci/nginx/certs")
    if not certs.is_dir():
        certs.mkdir()
    if not (certs / "privkey.pem").is_file():
        c.run(f"openssl req -x509 -nodes -newkey rsa:2048 -out {str(certs)}/cert.pem -keyout {str(certs)}/privkey.pem -subj \"/C=US/ST=NH/L=Concord/O=NHARNG/CN=minotaur.nharng.net\"")

@task
def postgres(c):
    c.run("podman run -d --rm --name test "
        "-e \"POSTGRES_ADMIN=admin\" "
        "-e \"POSTGRES_PASSWORD=admin\" " 
        "-e \"POSTGRES_DATABASE=test\" " 
        "docker.io/library/postgres:latest")

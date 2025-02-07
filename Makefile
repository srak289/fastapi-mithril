nginx-vol:
	-podman volume create content

nginx-content: nginx-vol
	$(eval VOL=$(shell podman volume inspect content | jq '.[]["Mountpoint"]'))
	rsync --no-compress -a -d static/ $(VOL)


nginx: nginx-content
	podman run -d --rm --name nginx \
		-v ./nginx.conf:/etc/nginx/nginx.conf:ro,Z \
		-v content:/usr/share/nginx/html:ro,Z \
		--network=host \
		docker.io/library/nginx:latest
restart:
	podman stop nginx
	$(MAKE) nginx

all:
	podman run -d --rm --name test \
		-e "POSTGRES_ADMIN=admin" \
		-e "POSTGRES_PASSWORD=admin" \
		-e "POSTGRES_DATABASE=test" \
		docker.io/library/postgres:latest

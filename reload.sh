docker stop office-status
docker rm office-status
docker pull alannix/office-status:latest
docker run -it \
           --name office-status \
           --privileged \
           --restart=always \
           --volume $(pwd)/:/app/data \
           --volume $(pwd)/credentials.json:/app/data/credentials.json:ro \
           alannix/office-status:latest

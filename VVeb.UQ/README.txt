# Docker container for Apache2-PHP server to run Docker

This Docker container runs an Apache2-PHP server that can deploy other containers using Docker-in-Docker.

Install Docker on Ubuntu, and as root, build and run the container as:

docker build -t web_front .
mkdir VVebUQ_runs
echo `pwd`/VVebUQ_runs/ > config.in
docker container run --privileged --name web_front -v /var/run/docker.sock:/var/run/docker.sock -v /root/ALC_IRIS/Dakota/web_front/VVebUQ_runs/:/VVebUQ_runs/ -p 8080:80 -d web_front

Then, you can access the web-page by going to:
<IP-address>:8080/




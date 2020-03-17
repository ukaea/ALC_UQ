# Docker container for Apache2-PHP server to run Docker

This Docker container runs an Apache2-PHP server that can deploy other containers using Docker-in-Docker.

Install Docker on Ubuntu, and as root, build and run the container as:

cd dakota_container
docker build -t dakota_image .
cd -
echo `pwd`/VVebUQ_runs/ > config.in
docker build -t vvebuq .
docker container run --privileged --name dakota_web_front -v /var/run/docker.sock:/var/run/docker.sock -v /root/ALC_UQ/VVeb.UQ/VVebUQ_runs/:/VVebUQ_runs/ -p 8080:80 -d vvebuq

Note: It is important to note that you can change the image name 'vvebuq' of the main app to whatever you wish, but the Dakota image needs to be called 'dakota_image'.

Then, you can access the web-page by going to:
<IP-address>:8080/




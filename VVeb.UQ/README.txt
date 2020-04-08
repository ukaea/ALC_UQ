# Docker container for Apache2-PHP server to run Docker-in-Docker

This Docker container runs an Apache2-PHP server that can deploy other containers using Docker-in-Docker.
It includes a Dakota container and uses the python user_interface (one dir up) to interface with Dakota.
Instead of launching MPI parallel jobs, Dakota is used to launch Docker containers for each run it needs.

More info on the Wiki:
https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ





# Docker container for Apache2-PHP server to run Docker-in-Docker

This Docker container runs an Apache2-PHP server that can deploy other containers using Docker-in-Docker.
It includes a Dakota container and uses the python user_interface (one dir up) to interface with Dakota.
Instead of launching MPI parallel jobs, Dakota is used to launch Docker containers for each run it needs.

More info on the Wiki:
https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ



This code is organised as follows:

./etc/
Contains the Apache web-server and the PHP libs.

./VVwebUQ_runs/
Empty folder, this is just a run-directory that will be used to share data and runs by the App at run-time.

./dakota_container/
The Dockerfile that needs to be built, and is launched inside the app.
For now, the app is restricted to Dakota, but one development would be to include other VVUQ softwares, like VECMA.

./entrypoint.sh
./wrapdocker
Scripts for the Apache and the Docker-in-Docker containers

./www/
Contains most of the code

./www/Logos/
Images, like the background of the web-page, a waiting gif etc.

./www/css/
The .css style sheets for the web-page

./www/example_user_workflow/
Basic examples for the user, a Doeckerfile with user-code, some input file examples to feed to the app.

./www/js/
Contains the javascripts for the web front-end. 
At the moment this is just all in one file, could be split into several, but it's not that big...

./www/interfaces/
Perl script that is run inside Dakota, and which launches the containers instead of MPI jobs.

./www/php/
All the PHP functions, including the REST-API, to upload files, execute commands, launch runs, pull docker images etc.






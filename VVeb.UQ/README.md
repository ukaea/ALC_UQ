This work was co-funded by the UKRI grant SBS IT18160 UKRI "Ada Lovelace Centre" Software Development, in collaboration with STFC, using IRIS computing resources. This work was donc in collaboration with Prominence a H-2020 project, "EOSC-hub" (Horizon 2020 grant number 777536).<br/>
https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/7208 <br/>
https://stfc.ukri.org/news-events-and-publications/features/ada-lovelace/ <br/>
https://prominence-eosc.github.io/docs/


# Installation of VVeb.UQ

This App enables to run a Docker Apache2-PHP server that can deploy other Docker containers.<br/>
We embed Dakota as a container, which then deploys other containers for each job (instead of just parallelising with MPI).<br/>

VVeb.UQ workflow:<br/>
<img src="https://github.com/ukaea/ALC_UQ/blob/master/VVeb.UQ/www/Logos/VVebUQ_workflow.png" width="1200">
<br/>

The `Dockerfile` of the main app was built by combining two other different cases, namely Apache2-PHP and Docker-in-Docker. The original Dockerfiles can be found in
* Apache2-PHP from: [https://github.com/jpetazzo/dind.git](https://github.com/jpetazzo/dind.git)
* Docker-in-Docker (DinD) from: [https://github.com/alfg/docker-php-apache.git](https://github.com/alfg/docker-php-apache.git)

Here are a few slides presenting the App:
https://github.com/ukaea/ALC_UQ/raw/master/VVeb.UQ/mini_presentation_slides.pdf

### Future desirable developments

There are several areas where developments are desirable:<br/>

1. Alternative UQ software:<br/>
At the moment, the app gives a choice between Dakota and VECMA's EasyVVUQ, but the user-interface for EasyVVUQ still needs to be fully developped like it is for Dakota.

2. Meta-data record:<br/>
At the moment, the data is saved on a directory where the app is run. Once the app is stopped, the data stays. However, the user may remove the data within the app. In all cases the meta data should be saved for each job, at least recording the name of the docker container, the Dakota input file, etc.

3. Embedded post-processing. It would be nice to allow the user to run post-processing on all instances of a job. Either directly at the end of a job, or even after the job has finished and return. In particular, it would be good to allow specific post-processing from Dakota and EasyVVUQ themselves.

### Install Docker
Installation on Ubuntu-19.04 is a bit shifty because Docker is only up to 18.04 at the moment, but it is definitely possible, using:

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable edge test"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
```

### Get ALC-UQ git repo
Clone the code:
```
git clone https://github.com/ukaea/ALC_UQ.git
cd ALC_UQ/VVeb.UQ/
```

### Register Docker image of user-code
Build and store the container image for your code. Or, do it with the provided example:
```
cd www/example_user_workflow/
docker build -t username/vvuq_example:latest .
docker login -u username
docker push username/vvuq_example:latest
cd -
```
This is the image name that you will need to provide once inside the app.<br/>
Please have a look at the Docker file in this directory.<br/>
It needs to store the code in a certain directory which is required by the app.<br/>
In addition, if you choose to use this example user-code, look at the file user_code.py, there is a parameter called `file_type`. This can be changed between `csv` and `netcdf`, but obviously this needs to be coherent with the input file-type you will feed to the app once running (ie. don't use `csv` in the user-code and then `netcdf` format for the input...)

### Pre-requisites: build Docker images for Dakota and/or VECMA's EasyVVUQ
The Dakota/EasyVVUQ image will be used to launch a container inside the app.<br/>
For Dakota:
```
cd dakota_container/
docker build -t dakota_image .
cd -
```
Note that the Dakota docker-build needs to download the Dakota software zipfile, which may take a while.<br/>
(At STFC, sometimes this download step just hangs, then just ctrl-C and retry build command).<br/>
For EasyVVUQ
```
cd easyvvuq_container/
docker build -t easyvvuq_image .
cd -
```
Note-1: the images HAVE TO be called 'dakota_image' and 'easyvvuq_image'.<br/>
Note-2: only one VVUQ software is really necessary, for example, if you know you will only use EasyVVUQ, you don't need to build the Dakota container.<br/>
Note-3: the EasyVVUQ interface is installed but limited types of vvuq sampling are available at the moment (only MC sampling), further development will be integrated in the near future.<br/>
More info can be found about Dakota and EasyVVUQ here:<br/>
https://dakota.sandia.gov/quickstart.html<br/>
https://easyvvuq.readthedocs.io/en/latest/basic_tutorial.html

### Build and run the app itself
A config file is used to specify whether we allow runs to be launched on the same machine as the app itself (otherwise, Prominence will need to be used). In most cases, we do not want to launch production user-containers on the app's server machine.<br/>
In this example, we build and run the app container with local-runs forbidden (otherwise use <code>TRUE</code>):
```
echo "LOCAL_RUNS_ALLOWED = FALSE" > config.in
docker build -t vvebuq_image .
export MOUNT_DIRS=" "
export MOUNT_DIRS=$MOUNT_DIRS"-v /var/run/docker.sock:/var/run/docker.sock "
export MOUNT_DIRS=$MOUNT_DIRS"-v /working/directory/of/your/choice/:/VVebUQ_runs/ "
export MOUNT_DIRS=$MOUNT_DIRS"-v /download/directory/of/your/choice/:/var/www/html/VVebUQ_downloads/ "
export MOUNT_DIRS=$MOUNT_DIRS"-v /path/to/ALC_UQ/user_interface/:/VVebUQ_user_interface/ "
docker container run --privileged --name vvebuq_app $MOUNT_DIRS -p 8080:80 -d vvebuq_image
```
Note-1: the image name can be anything, but THE CONTAINER NAME MUST BE <code>vvebuq_app</code> because this is used internally.<br/>
Note-2: the mount-paths have to correspond to existing work-dir and download-dir. This can be anything, particularly mounted scratch file-servers, if you do not want to dump data on the server machine where your app is running.<br/>
Note-3: the vvuq_user_interface takes care of interactions with the Dakota and/or EasyVVUQ software, and the mount path must also be correct (normally on directory up from this app).<br/>
Note-4: here we used PORT number 8080, but that can be anything of course, including 80.<br/>
Note-5: the environment variable <code>$MOUNT_DIRS</code> is never used in the app, this was just written like this for the clarity of this Wiki. For those who prefer one-liners, here is the full last command:
```
docker container run --privileged --name vvebuq_app -v /var/run/docker.sock:/var/run/docker.sock -v /working/directory/of/your/choice/:/VVebUQ_runs/ -v /download/directory/of/your/choice/:/var/www/html/VVebUQ_downloads/ -v /path/to/ALC_UQ/user_interface/:/VVebUQ_user_interface/ -p 8080:80 -d vvebuq_image
```


<br/><br/><br/><br/><br/>



# Using the App with the web front-end
You can access the web-page by going to:
```
<IP-address>:8080/
```
Once on the login page, you can request a new session with your username, and you will be given a link to your session. If you close the app and come back later, you can recover your session if using the same username. Here is a screenshot of what the web-front should look like:

<img src="https://github.com/ukaea/ALC_UQ/blob/master/VVeb.UQ/www/Logos/VVebUQ_screenshot3.png" width="1200">




<br/><br/><br/><br/><br/>




# Using the App from command line restAPI
If you do not want to use the web front-end to launch your runs, you can also use the RESTfull-API commands.

### Start a new session
First, you will need to request a new session:
```
curl http://<IP-address>:8080/php/login_session.php -GET -d "username=your_user_name"
```
This command will return the link you must use for your session, which will be the same <code>IP-address:PORT</code> but with an additional hash id unique to your user.<br/>
This is the link you will need to use for all the other restAPI calls.<br/>
For convenience, in all the rest-API commands below, we use an environment variable to record the restAPI address, eg.:
```
export VVEBUQ_RESTAPI=http://<IP-address>:8080/<hash-id>/rest_api.php
```
Here is an example of a basic set-up with IP-address 123.456.789.100
```
[ john@pc01 ~ ]$ curl http://123.456.789.100:8080/php/login_session.php -GET -d "username=new_vvuq_user"
You now have a new session running, please follow this link:
http://123.456.789.100:8080/1bb56c75f3a4f5dd4c811b8e286a7a3a/
[ john@pc01 ~ ]$ export VVEBUQ_RESTAPI=http://123.456.789.100:8080/1bb56c75f3a4f5dd4c811b8e286a7a3a/rest_api.php
[ john@pc01 ~ ]$ curl $VVEBUQ_RESTAPI -GET -d "action=check_app"
Hello new_vvuq_user.
Welcome to VVebUQ.
Please visit https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ
for detailed instructions.
[ john@pc01 ~ ]$
```

### Launch the VVUQ container
Before using the app, you will need to launch the VVUQ container you wish to use:
```
curl $VVEBUQ_RESTAPI -POST -d \
"action=launch_vvuq\
&selected_vvuq=dakota"
```
where the <code>selected_vvuq</code> can be either "dakota" or "easyvvuq".<br/>
Note: you can launch both Dakota and EasyVVUQ if you wish and then switch from one to the other in the run-options specified further down.

### Upload an input file
Note: file formats allowed are CSV (.csv) and NETCDF (.nc)
```
curl $VVEBUQ_RESTAPI -F 'fileToUpload[]=@/path/to/input.csv'
```
Examples of simple .csv input files can be found here:<br/>
https://github.com/ukaea/ALC_UQ/blob/master/VVeb.UQ/www/example_user_workflow/input_mc.csv
https://github.com/ukaea/ALC_UQ/blob/master/VVeb.UQ/www/example_user_workflow/input_scan.csv

### Upload a zipped data input file (optional)
Note: file formats allowed are ZIP (.zip) file. It can contain files and folders. It will be unzipped at the top directory for each run.
```
curl $VVEBUQ_RESTAPI -F 'dataFileToUpload[]=@/path/to/data_input.zip'
```

### Request a Prominence Token (optional)
This is only necessary if you want to deploy your runs through Prominence.<br/>
For more information about Prominence, please visit https://prominence-eosc.github.io/docs/
```
curl $VVEBUQ_RESTAPI -POST -d \
"action=request_prominence_token\
&selected_vvuq=dakota"
```
Note: The Prominence token request must be done this way, because the Token must be valid inside the App itself.<br/>
ie. you cannot just request a Prominence Token directly following instructions on the Prominence website, because this will give you a Token that the App will not recognise.<br/>
If you decide to change VVUQ software between Dakota and EasyVVUQ while using the app, you will need to request a new Token with the new VVUQ software (eg. "dakota" or "easyvvuq").<br/>
Note, the Prominence Tokens expire after 1-hour.

### Launch the run
To launch a run, use this command:
```
curl $VVEBUQ_RESTAPI -POST -d \
"action=launch_run\
&docker_image_run=username/vvuq_example:latest\
&selected_vvuq=dakota\
&n_cpu=3\
&RAM=2\
&input_file_name=input_mc.csv\
&input_file_type=csv\
&input_data_file_name=data_input.zip\
&use_prominence=false"
```
where you will need to replace the corresponding entries for the parameters:<br/>
`docker_image_run`: name of the user-code docker image<br/>
`selected_vvuq`: name of the VVUQ app you want to use (either "dakota" or "easyvvuq")<br/>
`n_cpu`: number of cores for each instance of your workflow.<br/>
`RAM`: size of RAM of each instance (only for Prominence)<br/>
`input_file_name`: name of the input file containing the values and errors to be sampled<br/>
`input_file_type`: can be either `csv` or `nc` (for netcdf).<br/>
`input_data_file_name`: (optional) name of the zipped data input file containing additional inputs for your run (default="none").<br/>
`use_prominence`: (optional) either `true` or `false` (default).<br/>

### List previous runs
This command will give you a list of all the previous runs you've launched. These are typically tagged with the date/time of the launch, as well as the user-code docker image name:
```
curl $VVEBUQ_RESTAPI -GET -d "action=list_runs"
```

### Get Run status
This command will give you the status of the latest run you submitted, including all its deployed tasks and containers
```
curl $VVEBUQ_RESTAPI -GET -d "action=get_run_status"
```
You can also view older runs by using the optional tag <code>run_name</code> (where you can get the run-name from the action <code>list_runs</code> above)
```
curl $VVEBUQ_RESTAPI -GET -d \
"action=get_run_status\
&run_name=name_of_run"
```

### List data contained inside a run
This will show you how many containers have been launched inside the latest run, and what files+folders the run-dir of a container includes (assuming all containers include the same files+folders).
```
curl $VVEBUQ_RESTAPI -GET -d "action=list_run_files"
```
Here as well, as above, you can view older runs by using the optional tag <code>run_name</code>

### Get Download URLs for run data
Specific to Prominence, this will retrieve URLs for each individual instance of a run, together with a bash script that loops through these URLs and executes the downloads. This enables the user to choose which instances to download, instead of retrieving 100's or 1000's of jobs at once, which can take a long time when running on remote clouds with Prominence. To get the URLs for the latest run, into a file named `run_URLs.zip`, use the command:
```
curl $VVEBUQ_RESTAPI -GET --output run_URLs.zip -d "action=download_run_urls"
```
Again, as above, you can download older runs by using the optional tag <code>run_name</code>

### Download entire run data
To download the entire data produced by the latest run, into a file named `run_data.zip`, use the command:
```
curl $VVEBUQ_RESTAPI -GET --output run_data.zip -d "action=download_run"
```
Again, as above, you can download older runs by using the optional tag <code>run_name</code><br/>
Be aware that when using remote Clouds through Prominence, this can take a long time, depending on the size of your workflow and the amount of data. It is strongly recommended to use the <code>download_run_urls</code> option instead when using Prominence.

### Download selected files from run
If you do not want to download the entire run, you can download only specific files and/or folders, using the following command:
```
curl $VVEBUQ_RESTAPI -GET --output run_data.zip -d \
"action=download_run_files\
&files[]=filename1.txt\
&files[]=filename2\
&files[]=foldername"
```
Again, as above, you can download selected-file from older runs by using the optional tag <code>run_name</code><br/>
Important note: This function is not yet available for Prominence runs. The download of Prominence files is done with a tarball in the ECHO S3 server, and thus the entire run needs to be downloaded at once for Prominence.

### Remove containers belonging to a run
This will stop and delete all docker containers belonging to the latest run:
```
curl $VVEBUQ_RESTAPI -GET -d 'action=delete_run'
```
Again, as above, you can delete an older run by using the optional tag <code>run_name</code><br/>
Note that when using prominence, deleting runs does not make much sense, since Prominence will anyway keep the containers there for some time before deleting them completely. However, if you delete the run data (function below), then as far as you will see, the run containers will "not exist".

### Remove data belonging to a run
Similarly, to remove all the data corresponding to a run, simply:
```
curl $VVEBUQ_RESTAPI -GET -d 'action=delete_run_data'
```
Note that deleting data from a run automatically deletes the corresponding containers, which will not be retrievable.




<br/><br/><br/><br/><br/>




# Running VVeb.UQ at UKAEA
An instance of the app is running at CCFE:<br/>
http://vvebuq.apps.l:8080<br/>
You will need to be inside the CCFE network to access it, ie. either through VPN or through NoMachine connection.<br/>
There is no specific port, so a session request would look like:
```
curl http://vvebuq.apps.l:8080/php/login_session.php -GET -d "username=johnsmith"
```
Local runs are not allowed on this server, so all runs need to be done through Prominence.




<br/><br/><br/><br/><br/>




# Some more use-cases
Additional use-cases are available in <code>ALC_UQ/VVeb.UQ/www/example_user_workflow/</code><br/>


### OpenMC
An example of an OpenMC workshop has been adapted from<br/>
https://github.com/ukaea/openmc_workshop<br/>
To build the image, use these commands:
```
cd www/example_user_workflow/OpenMC/
docker build -t username/vvuq_openmc:latest .
docker login -u username
docker push username/vvuq_openmc:latest
cd -
```
Then, you can run a VVebUQ job using the input file <code>ALC_UQ/VVeb.UQ/www/example_user_workflow/OpenMC/input_mc.csv</code><br/>
This will run the Task-4 of the OpenMC-workshop, while varying:<br/>
- the number of mesh points in the simulations
- the energy of the neutrons from the main neutron source
- the number of particles in the simulation

After retrieving the data, you can compare the output files and the <code>tally_on_mesh.vtk</code> files.<br/>
Here is a presentation showing how to view the vtk files on Paraview:<br/>
https://slides.com/openmc_workshop/neutronics_workshop#/16


### Nektar++
An example of a Nektar++ tutorial (the Advection-Diffusion) has been adapted from<br/>
https://www.nektar.info/community/tutorials/<br/>
To build the image, use these commands:
```
cd www/example_user_workflow/NektarPP/
docker build -t username/vvuq_nektar:latest .
docker login -u username
docker push username/vvuq_nektar:latest
cd -
```
Then, you can run a VVebUQ job using the input file <code>ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP/input_mc.csv</code><br/>
This will run the tutorial, while varying:<br/>
- the advection speed of the blobs
- the polynomial order (p) of the spectral-hp finite elements

After retrieving the data, you can compare the output files and the last file simulation file <code>ADR_mesh_aligned_9.vtu</code> in Paraview or Vizit.


<br/>
For convenience, we provide here a full sequence of the commands to follow for this use-case:

```
[ stan@my-pc:~/Work ]$ mkdir VVebUQ_use_cases
[ stan@my-pc:~/Work ]$ cd VVebUQ_use_cases/
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ git clone https://github.com/ukaea/ALC_UQ.git
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ cd ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP/
[ stan@my-pc:~/Work/VVebUQ_use_cases/ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP ]$ docker build -t your_username/vvuq_nektar:latest .
[ stan@my-pc:~/Work/VVebUQ_use_cases/ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP ]$ docker login -u your_username
[ stan@my-pc:~/Work/VVebUQ_use_cases/ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP ]$ docker push your_username/vvuq_nektar:latest
[ stan@my-pc:~/Work/VVebUQ_use_cases/ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP ]$ cd -
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl http://vvebuq.apps.l:8080/php/login_session.php -GET -d "username=your_username"
You now have a new session running, please use this link for you rest-API calls:
http://vvebuq.apps.l:8080/1c103a3b7481d504e8d2ead811dac588/rest_api.php
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ export VVEBUQ_RESTAPI=http://vvebuq.apps.l:8080/1c103a3b7481d504e8d2ead811dac588/rest_api.php
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -POST -d "action=launch_vvuq&selected_vvuq=dakota"
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -POST -d "action=request_prominence_token&selected_vvuq=dakota"
Client registration successful
To obtain a token, use a web browser to open the page https://host-130-246-215-158.nubes.stfc.ac.uk/device and enter the code XXYYZZ when requested
Successfully retrieved token
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -F 'fileToUpload[]=@./ALC_UQ/VVeb.UQ/www/example_user_workflow/NektarPP/input_mc.csv'
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -POST -d \
> "action=launch_run\
> &docker_image_run=your_username/vvuq_nektar:latest\
> &selected_vvuq=dakota\
> &n_cpu=1\
> &input_file_name=input_mc.csv\
> &input_file_type=csv\
> &use_prominence=false"
Your job is being prepared for submission...
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -GET -d "action=get_run_status"
ID      NAME               CREATED               STATUS   ELAPSED      IMAGE                              CMD
40657   workdir_VVebUQ_1   2020-09-25 15:17:43   idle                  your_username/vvuq_nektar:latest      
40658   workdir_VVebUQ_2   2020-09-25 15:17:43   idle                  your_username/vvuq_nektar:latest      
40659   workdir_VVebUQ_3   2020-09-25 15:17:45   idle                  your_username/vvuq_nektar:latest      
40660   workdir_VVebUQ_4   2020-09-25 15:17:45   idle                  your_username/vvuq_nektar:latest      
40661   workdir_VVebUQ_5   2020-09-25 15:17:47   idle                  your_username/vvuq_nektar:latest      
40662   workdir_VVebUQ_6   2020-09-25 15:17:47   idle                  your_username/vvuq_nektar:latest      
```

Then, you'll need to wait until Prominence deploys and runs the jobs.<br/>
After completion, you'll be able to download the run results.
```
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -GET -d "action=get_run_status"
ID      NAME               CREATED               STATUS      ELAPSED      IMAGE                              CMD
40657   workdir_VVebUQ_1   2020-09-25 15:17:43   completed   0+00:04:01   your_username/vvuq_nektar:latest      
40658   workdir_VVebUQ_2   2020-09-25 15:17:43   completed   0+00:04:01   your_username/vvuq_nektar:latest      
40659   workdir_VVebUQ_3   2020-09-25 15:17:45   completed   0+00:04:01   your_username/vvuq_nektar:latest      
40660   workdir_VVebUQ_4   2020-09-25 15:17:45   completed   0+00:04:01   your_username/vvuq_nektar:latest      
40661   workdir_VVebUQ_5   2020-09-25 15:17:47   completed   0+00:04:01   your_username/vvuq_nektar:latest      
40662   workdir_VVebUQ_6   2020-09-25 15:17:47   completed   0+00:04:01   your_username/vvuq_nektar:latest      
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ curl $VVEBUQ_RESTAPI -GET --output run_data.zip -d "action=download_run"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  640k    0  640k    0     0  40959      0 --:--:--  0:00:16 --:--:--  169k
[ stan@my-pc:~/Work/VVebUQ_use_cases ]$ 
```


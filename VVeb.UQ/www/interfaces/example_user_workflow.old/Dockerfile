FROM python:3

# --- Packages and environment
RUN pip3 install netCDF4

# --- The way this is run is important!
# --- All the data/codes necessary must be in a separate directory
ADD user_code.py /data_dir/
# --- The code MUST be run in a directory named exactly /work_dir/
# --- This is because this directory will be mounted to an external directory in the app (ie. available outside the container)
# --- Hence, before running your code, you must copy/move all your data/codes into this work_dir directory, as below
WORKDIR /work_dir/
CMD ["/bin/bash","-c","mv ../data_dir/* . ; python3 user_code.py"]


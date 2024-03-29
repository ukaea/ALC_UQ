# --- Docker file for Dakota
FROM centos:7
ENV container docker
MAINTAINER Stan Pamela <stanislas.pamela@ukaea.uk>

# --- Packages and environment
RUN yum update -y 
RUN yum install -y gcc-c++ gcc-gfortran gdb zip unzip make lapack-devel blas-devel openmpi-devel zlib-devel wget perl perl-Data-Dumper libicu-devel libhdf5-dev libnetcdf-dev hdf5-openmpi-devel compat-openmpi16 
# --- Install Docker
RUN yum install -y http://vault.centos.org/centos/7.3.1611/extras/x86_64/Packages/container-selinux-2.9-4.el7.noarch.rpm 
RUN yum install -y yum-utils device-mapper-persistent-data lvm2 
RUN yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo 
RUN yum install -y docker-ce 
# --- Install netcdf
RUN yum install -y netcdf4-python.x86_64 python3-pip.noarch 
RUN pip3 install --upgrade pip
RUN pip3 install numpy cftime netCDF4==1.4.3 xarray
ENV PATH="/usr/lib64/openmpi/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/lib64/compat-openmpi16/lib/:${LD_LIBRARY_PATH}"
ENV HOME="/dakota_dir"

# --- Install Dakota
WORKDIR /dakota_dir/
RUN wget --no-check-certificate --no-cache --no-cookies https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.10-release-public-rhel7.x86_64.tar.gz 
RUN tar -xvf dakota-6.10-release-public-rhel7.x86_64.tar.gz --transform 's/dakota-6.10.0.Linux.x86_64/dakota/' 
RUN rm dakota-6.10-release-public-rhel7.x86_64.tar.gz
ENV INSTALL_DIR="/dakota_dir/dakota"
ENV PATH="${INSTALL_DIR}/bin:${INSTALL_DIR}/share/dakota/test:${INSTALL_DIR}/gui:${PATH}"
ENV PYTHONPATH="${PYTHONPATH}:${INSTALL_DIR}/share/dakota/Python"
ENV LD_LIBRARY_PATH="/usr/lib64/openmpi/lib/:${LD_LIBRARY_PATH}"

# --- Install Prominence
RUN pip3 install prominence
ENV PROMINENCE_URL=https://host-130-246-215-158.nubes.stfc.ac.uk/prominence/v1
ENV PROMINENCE_OIDC_URL=https://host-130-246-215-158.nubes.stfc.ac.uk

# --- Get Docker in place
ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker
VOLUME /var/lib/docker

# --- Run waiting script
WORKDIR /dakota_dir/
CMD ["wrapdocker"]



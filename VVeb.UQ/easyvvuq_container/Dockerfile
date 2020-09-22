# --- Docker file for VECMA's easyvvuq
FROM centos:7
ENV container docker
MAINTAINER Stan Pamela <stanislas.pamela@ukaea.uk>

# --- Packages and environment
RUN yum update -y \
 && yum install -y git gcc-c++ gcc-gfortran gdb zip unzip make lapack-devel blas-devel openmpi-devel zlib-devel wget perl perl-Data-Dumper libicu-devel hdf5-openmpi-devel compat-openmpi16 \
# --- Install Docker
 && yum install -y http://vault.centos.org/centos/7.3.1611/extras/x86_64/Packages/container-selinux-2.9-4.el7.noarch.rpm \
 && yum install -y yum-utils device-mapper-persistent-data lvm2 \
 && yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo \
 && yum install -y docker-ce \
# --- Install netcdf
 && yum install -y netcdf4-python.x86_64 python3-pip.noarch python3-devel \
 && pip3 install netCDF4 xarray
ENV PATH="/usr/lib64/openmpi/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/lib64/compat-openmpi16/lib/:${LD_LIBRARY_PATH}"
ENV LD_LIBRARY_PATH="/usr/lib64/openmpi/lib/:${LD_LIBRARY_PATH}"
ENV HOME="/easyvvuq_dir"

# --- Install Dakota
WORKDIR /easyvvuq_dir/
RUN git clone https://github.com/UCL-CCS/EasyVVUQ.git
WORKDIR /easyvvuq_dir/EasyVVUQ
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade setuptools
RUN python3 setup.py install

# --- Install Prominence
RUN pip3 install prominence
ENV PROMINENCE_URL=https://host-130-246-215-158.nubes.stfc.ac.uk/prominence/v1
ENV PROMINENCE_OIDC_URL=https://host-130-246-215-158.nubes.stfc.ac.uk

# --- Get Docker in place
ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker
VOLUME /var/lib/docker

# --- Run waiting script
WORKDIR /easyvvuq_dir/
CMD ["wrapdocker"]



FROM ubuntu:18.04 as base

# --- Install Nektar++
RUN apt-get --yes update && apt-get --yes install wget gpg mpi && \
    wget http://www.nektar.info/nektar-apt.gpg -O - | apt-key add - && \
    echo "deb http://www.nektar.info/ubuntu-bionic bionic contrib" > /etc/apt/sources.list.d/nektar.list && \
    echo "deb http://deb.debian.org/debian buster main non-free" > /etc/apt/source.list && \
    apt-get --yes update
    #apt-get install ca-certificates && \
RUN apt-get --yes install nektar++

# --- Download advection tutorial
WORKDIR /prepare_run/
RUN wget http://doc.nektar.info/tutorials/5.0.0/basics/advection-diffusion/basics-advection-diffusion.tar.gz && \
    tar -xvzf basics-advection-diffusion.tar.gz

# --- Prepare files for run
WORKDIR /prepare_run/basics-advection-diffusion/tutorial/
RUN NekMesh ADR_mesh.msh ADR_mesh.xml
RUN FieldConvert ADR_mesh.xml ADR_mesh.vtu
RUN NekMesh -m peralign:surf1=200:surf2=400:dir=x ADR_mesh.xml ADR_mesh_aligned.xml
RUN cp ../completed/ADR_conditions.xml .

# --- Add the file that changes the input conditions of the simulation
ADD change_inputs.sh /prepare_run/basics-advection-diffusion/tutorial/
RUN chmod +x /prepare_run/basics-advection-diffusion/tutorial/change_inputs.sh

WORKDIR /tmp/work_dir/
CMD ["/bin/bash","-c","cp -r /prepare_run/basics-advection-diffusion/tutorial/* . ; ./change_inputs.sh ; ADRSolver ADR_mesh_aligned.xml ADR_conditions.xml ; FieldConvert ADR_mesh_aligned.xml ADR_conditions.xml ADR_mesh_aligned_9.chk ADR_mesh_aligned_9.vtu"]



# build with the following command
# sudo docker build -t openmcworkshop/workshop .

FROM openmcworkshop/openmc_workshop_dependencies:openmc_dagmc_nndc_dependencies

RUN git clone https://github.com/ukaea/openmc_workshop

ADD 2_example_neutron_flux_tokamak_vvuq.py /openmc_workshop/tasks/task_4/
WORKDIR /tmp/work_dir/
CMD ["/bin/bash","-c","cp -r /openmc_workshop/tasks/task_4/* . ; python3 2_example_neutron_flux_tokamak_vvuq.py"]



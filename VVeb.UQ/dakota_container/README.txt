# Container for Dakota alone

This image contains a few scripts.
- The waiting_for_actions.sh script will be launched inside the container.
  It just runs a sleeping loop to keep the container alive for actions to be executed from outside

To build and run this image, you can use the following commands:
docker build -t dakota_alone .
docker container run --name dakota_alone -d dakota_alone
docker exec -it dakota_alone dakota -version


# Container for Dakota alone

To build and run this image, you can use the following commands:
docker build -t dakota_alone .
docker container run --name dakota_alone -d dakota_alone
docker exec -it dakota_alone dakota -version


# DockerPorkbunDDNS

A docker image for dynamic dns using porkbun.

## Getting started

First, build the image. To make this easier, the repository includes a shell script.
When running the image, assign a volume or directory bind to /config in the container.
On the first run, the image will create a new config file and exit, if it didn't find one.
Define your domain(s) and api token there, and restart the container.

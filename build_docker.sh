#!/bin/bash

docker build -t porkbun_ddns:latest .
echo "Docker image built successfully"
echo "ATTENTION: The image tag in this case is 'porkbun_ddns:latest'"
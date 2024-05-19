#!/bin/bash

docker build -t raspberry-ams .

echo "Docker save .tar"
docker save -o raspberry-ams.tar raspberry-ams

echo "Transferindo arquivo .tar"
scp -P 2222 raspberry-ams.tar raspbian@127.0.0.1:/home/raspbian

echo "Iniciando docker"
ssh -p 2222 raspbian@127.0.0.1 << EOF
docker load -i /home/raspbian/raspberry-ams.tar
docker run --privileged -d raspberry-ams
EOF
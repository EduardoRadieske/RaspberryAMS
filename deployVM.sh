#!/bin/bash
#Faz o deploy em VM para testes

docker build -t raspberry-ams .

echo "Docker save .tar"
docker save -o raspberry-ams.tar raspberry-ams

echo "Transferindo arquivo .tar"
scp -P 2222 raspberry-ams.tar raspbian@127.0.0.1:/home/raspbian

echo "Iniciando docker"
ssh -p 2222 raspbian@127.0.0.1 << EOF
docker stop raspberry-ams 
docker rm raspberry-ams
docker load -i /home/raspbian/raspberry-ams.tar
docker run --privileged -d --name raspberry-ams raspberry-ams
EOF
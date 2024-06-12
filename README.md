# RaspberryAMS
Projeto desenvolvido para o projeto FAHOR E-Racing
Este projeto é um sistema AMS e foi projetado para executar em um Raspberry PI

## Informações importantes / Comandos Úteis
1. Install requirements, sendo que o pacote dalybms-0.5.0 já está integrado ao projeto
```bash
pip install -r requirements.txt
```

2. Para deploy em Máquina Virtual Raspbian
```bash
./deployVM.sh
```

3. Para deploy em Raspberry PI via SSH na própria rede
```bash
./deploy.sh
```

4. Para deploy em Raspberry PI via SSH com Hotspot local
```bash
scp -P 22 -r src requirements.txt Dockerfile eracing@192.168.137.222:ams
ssh -p 22 eracing@192.168.137.222 
docker build -t raspberry-ams .
docker run --privileged -d --name raspberry-ams raspberry-ams
```
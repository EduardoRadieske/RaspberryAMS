#!/bin/bash
#Faz o deploy e build no raspberry pi via SSH 

# Variáveis
REMOTE_DIR="/home/eracing/ams"
LOCAL_SRC_DIR="src"
LOCAL_REQUIREMENTS="requirements.txt"
LOCAL_DOCKERFILE="Dockerfile"

read -s -p "Digite a senha SSH: " PASSWORD
echo

# Função para verificar o retorno de status
check_status() {
    if [ $1 -ne 0 ]; then
        echo "Erro: $2"
        exit $1
    fi
}

# Validar e parar a aplicação
sshpass -p $PASSWORD ssh -p 22 eracing@raspberrypi << EOF 
docker stop raspberry-ams 
docker rm raspberry-ams
EOF
check_status $? "Falha ao parar o Docker remotamente"

# Criar diretório remoto
echo "Criando diretório remoto"
sshpass -p $PASSWORD ssh  -p 22 eracing@raspberrypi "mkdir -p $REMOTE_DIR"
check_status $? "Falha ao criar diretório remoto"

# Transferir arquivos locais para o remoto
echo "Transferindo arquivos locais para o servidor remoto"
sshpass -p $PASSWORD scp -P 22 -r $LOCAL_SRC_DIR $LOCAL_REQUIREMENTS $LOCAL_DOCKERFILE eracing@raspberrypi:$REMOTE_DIR
check_status $? "Falha ao transferir arquivos para o servidor remoto"

# Construir e rodar o docker remotamente
echo "Construindo e rodando o Docker remotamente"
sshpass -p $PASSWORD ssh -p 22 eracing@raspberrypi << EOF
cd $REMOTE_DIR
docker build -t raspberry-ams . && \
rm -rf $REMOTE_DIR/src $REMOTE_DIR/requirements.txt $REMOTE_DIR/Dockerfile && \
docker run --privileged -d --name raspberry-ams raspberry-ams
EOF
check_status $? "Falha ao construir e rodar o Docker remotamente"

echo "Deploy finalizado"
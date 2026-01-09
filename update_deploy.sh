#!/bin/bash

#############################################
# Быстрое обновление приложения на сервере
#############################################

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

APP_NAME="estate"
APP_DIR="/home/$APP_NAME/estate-catalog"

if [ -z "$1" ]; then
    echo -e "${RED}❌ Укажите IP адрес сервера${NC}"
    echo "Использование: ./update_deploy.sh SERVER_IP"
    exit 1
fi

SERVER_IP=$1

echo -e "${BLUE}🔄 Обновление приложения на сервере...${NC}"
echo ""

ssh root@$SERVER_IP "
cd $APP_DIR
su - $APP_NAME -c 'cd $APP_DIR && git pull origin main'
su - $APP_NAME -c 'cd $APP_DIR && source venv/bin/activate && pip install -r requirements.txt'
supervisorctl restart $APP_NAME
"

echo ""
echo -e "${GREEN}✅ Обновление завершено!${NC}"
echo -e "${BLUE}Сайт: http://$SERVER_IP${NC}"

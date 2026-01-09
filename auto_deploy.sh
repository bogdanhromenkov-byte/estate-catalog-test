#!/bin/bash

#############################################
# Автоматический деплой на DigitalOcean
# Estate Catalog - Flask Application
#############################################

set -e  # Exit on error

echo "🚀 Starting automatic deployment..."
echo ""

# Цвета для красивого вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Конфигурация
APP_NAME="estate"
APP_DIR="/home/$APP_NAME/estate-catalog"
REPO_URL="https://github.com/bogdanhromenkov-byte/estate-catalog-test.git"
DOMAIN=""  # Оставьте пустым если используете только IP

# Проверка IP адреса
if [ -z "$1" ]; then
    echo -e "${RED}❌ Ошибка: Не указан IP адрес сервера${NC}"
    echo "Использование: ./auto_deploy.sh SERVER_IP [DOMAIN]"
    echo "Пример: ./auto_deploy.sh 142.93.45.123"
    echo "Пример с доменом: ./auto_deploy.sh 142.93.45.123 estate.com"
    exit 1
fi

SERVER_IP=$1
if [ ! -z "$2" ]; then
    DOMAIN=$2
fi

echo -e "${BLUE}📡 Сервер: $SERVER_IP${NC}"
if [ ! -z "$DOMAIN" ]; then
    echo -e "${BLUE}🌐 Домен: $DOMAIN${NC}"
fi
echo ""

# Функция для выполнения команд на сервере
run_remote() {
    ssh -o StrictHostKeyChecking=no root@$SERVER_IP "$@"
}

echo -e "${GREEN}✅ Шаг 1/8: Проверка подключения к серверу${NC}"
if ! ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$SERVER_IP "echo 'Connected'" > /dev/null 2>&1; then
    echo -e "${RED}❌ Не удалось подключиться к серверу${NC}"
    echo "Убедитесь что:"
    echo "  1. IP адрес правильный"
    echo "  2. SSH ключ настроен: ssh-copy-id root@$SERVER_IP"
    echo "  3. Сервер запущен"
    exit 1
fi
echo "✓ Подключение успешно"
echo ""

echo -e "${GREEN}✅ Шаг 2/8: Обновление системы${NC}"
run_remote "apt-get update -qq && apt-get upgrade -y -qq"
echo "✓ Система обновлена"
echo ""

echo -e "${GREEN}✅ Шаг 3/8: Установка зависимостей${NC}"
run_remote "DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3 python3-pip python3-venv nginx supervisor git ufw"
echo "✓ Установлены: Python3, Nginx, Supervisor, Git"
echo ""

echo -e "${GREEN}✅ Шаг 4/8: Создание пользователя для приложения${NC}"
run_remote "
if ! id -u $APP_NAME > /dev/null 2>&1; then
    adduser --disabled-password --gecos '' $APP_NAME
    echo '✓ Пользователь $APP_NAME создан'
else
    echo '✓ Пользователь $APP_NAME уже существует'
fi
"
echo ""

echo -e "${GREEN}✅ Шаг 5/8: Клонирование проекта и установка зависимостей${NC}"
run_remote "
# Удалить старую версию если есть
rm -rf $APP_DIR

# Клонировать проект
su - $APP_NAME -c 'git clone $REPO_URL estate-catalog'
cd $APP_DIR

# Создать виртуальное окружение
su - $APP_NAME -c 'cd $APP_DIR && python3 -m venv venv'

# Установить зависимости
su - $APP_NAME -c 'cd $APP_DIR && source venv/bin/activate && pip install -q -r requirements.txt'

# Инициализировать базу данных
su - $APP_NAME -c 'cd $APP_DIR && source venv/bin/activate && timeout 5 python3 main.py || true'

echo '✓ Проект установлен'
"
echo ""

echo -e "${GREEN}✅ Шаг 6/8: Настройка Supervisor${NC}"
run_remote "
# Создать директорию для логов
mkdir -p /var/log/$APP_NAME
chown $APP_NAME:$APP_NAME /var/log/$APP_NAME

# Создать конфигурацию supervisor
cat > /etc/supervisor/conf.d/$APP_NAME.conf << 'SUPERVISOR_EOF'
[program:$APP_NAME]
command=$APP_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 main:app
directory=$APP_DIR
user=$APP_NAME
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/$APP_NAME/$APP_NAME.err.log
stdout_logfile=/var/log/$APP_NAME/$APP_NAME.out.log
SUPERVISOR_EOF

# Перезапустить supervisor
supervisorctl reread
supervisorctl update
supervisorctl start $APP_NAME

echo '✓ Supervisor настроен'
"
echo ""

echo -e "${GREEN}✅ Шаг 7/8: Настройка Nginx${NC}"

if [ -z "$DOMAIN" ]; then
    SERVER_NAME=$SERVER_IP
else
    SERVER_NAME=$DOMAIN
fi

run_remote "
# Удалить дефолтную конфигурацию
rm -f /etc/nginx/sites-enabled/default

# Создать конфигурацию nginx
cat > /etc/nginx/sites-available/$APP_NAME << 'NGINX_EOF'
server {
    listen 80;
    server_name $SERVER_NAME;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control 'public, immutable';
    }

    client_max_body_size 10M;
}
NGINX_EOF

# Активировать конфигурацию
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/

# Проверить конфигурацию
nginx -t

# Перезапустить nginx
systemctl restart nginx

echo '✓ Nginx настроен'
"
echo ""

echo -e "${GREEN}✅ Шаг 8/8: Настройка Firewall${NC}"
run_remote "
# Настроить UFW
ufw --force enable
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw allow 22/tcp

echo '✓ Firewall настроен'
"
echo ""

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Деплой завершён успешно!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📱 Ваш сайт доступен по адресу:${NC}"
if [ -z "$DOMAIN" ]; then
    echo -e "${BLUE}   👉 http://$SERVER_IP${NC}"
else
    echo -e "${BLUE}   👉 http://$DOMAIN${NC}"
    echo -e "${BLUE}   👉 http://$SERVER_IP${NC}"
fi
echo ""
echo -e "${BLUE}📊 Полезные команды:${NC}"
echo ""
echo "Проверить статус приложения:"
echo "  ssh root@$SERVER_IP 'supervisorctl status $APP_NAME'"
echo ""
echo "Посмотреть логи:"
echo "  ssh root@$SERVER_IP 'tail -f /var/log/$APP_NAME/$APP_NAME.err.log'"
echo ""
echo "Обновить код:"
echo "  ssh root@$SERVER_IP 'cd $APP_DIR && su - $APP_NAME -c \"cd $APP_DIR && git pull && source venv/bin/activate && pip install -r requirements.txt\" && supervisorctl restart $APP_NAME'"
echo ""
echo "Перезапустить приложение:"
echo "  ssh root@$SERVER_IP 'supervisorctl restart $APP_NAME'"
echo ""

# SSL сертификат (опционально)
if [ ! -z "$DOMAIN" ]; then
    echo -e "${BLUE}🔒 Хотите установить SSL (HTTPS)? [y/N]${NC}"
    read -t 10 -r ssl_response || ssl_response="n"
    if [[ "$ssl_response" =~ ^[Yy]$ ]]; then
        echo ""
        echo -e "${GREEN}Установка SSL сертификата...${NC}"
        run_remote "
        apt-get install -y certbot python3-certbot-nginx
        certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email
        "
        echo -e "${GREEN}✅ SSL установлен! Сайт доступен по https://$DOMAIN${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✨ Готово! Откройте сайт в браузере! ✨${NC}"

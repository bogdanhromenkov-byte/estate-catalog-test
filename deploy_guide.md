# Деплой на DigitalOcean

## Подготовка проекта

### 1. Создайте файлы для деплоя

Уже готовы:
- `requirements.txt` - зависимости Python
- `.gitignore` - игнорируемые файлы

### 2. Подключение к серверу

```bash
ssh root@ваш_ip_адрес
```

## Установка на сервере

### Шаг 1: Обновите систему

```bash
apt update && apt upgrade -y
```

### Шаг 2: Установите Python и зависимости

```bash
apt install python3 python3-pip python3-venv nginx supervisor git -y
```

### Шаг 3: Создайте пользователя для приложения

```bash
adduser estate
usermod -aG sudo estate
su - estate
```

### Шаг 4: Клонируйте проект

```bash
cd /home/estate
git clone https://github.com/ваш-username/estate-catalog.git
cd estate-catalog
```

### Шаг 5: Создайте виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Шаг 6: Инициализируйте базу данных

```bash
python3 main.py
# Дождитесь создания базы данных, затем Ctrl+C
```

## Настройка Gunicorn

### Создайте файл конфигурации

```bash
sudo nano /etc/supervisor/conf.d/estate.conf
```

Вставьте:

```ini
[program:estate]
command=/home/estate/estate-catalog/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 main:app
directory=/home/estate/estate-catalog
user=estate
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/estate/estate.err.log
stdout_logfile=/var/log/estate/estate.out.log
```

### Создайте директорию для логов

```bash
sudo mkdir -p /var/log/estate
sudo chown estate:estate /var/log/estate
```

### Запустите supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start estate
```

## Настройка Nginx

### Создайте конфигурацию Nginx

```bash
sudo nano /etc/nginx/sites-available/estate
```

Вставьте:

```nginx
server {
    listen 80;
    server_name ваш_домен.com;  # или IP адрес

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/estate/estate-catalog/static;
        expires 30d;
    }
}
```

### Активируйте конфигурацию

```bash
sudo ln -s /etc/nginx/sites-available/estate /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Настройка Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Готово! 🎉

Ваш сайт доступен по адресу:
- http://ваш_ip_адрес
- или http://ваш_домен.com (если настроили домен)

## Обновление проекта

Когда обновите код на GitHub:

```bash
cd /home/estate/estate-catalog
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart estate
```

## Установка SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d ваш_домен.com
```

## Полезные команды

```bash
# Проверить статус приложения
sudo supervisorctl status estate

# Перезапустить приложение
sudo supervisorctl restart estate

# Посмотреть логи
tail -f /var/log/estate/estate.err.log
tail -f /var/log/estate/estate.out.log

# Проверить статус Nginx
sudo systemctl status nginx

# Перезапустить Nginx
sudo systemctl restart nginx
```

## Бэкап базы данных

```bash
# Создать бэкап
cp /home/estate/estate-catalog/estate.db /home/estate/backups/estate_$(date +%Y%m%d).db

# Автоматический бэкап (добавьте в crontab)
crontab -e
# Добавьте строку:
0 2 * * * cp /home/estate/estate-catalog/estate.db /home/estate/backups/estate_$(date +\%Y\%m\%d).db
```

# 🚀 Быстрый старт

## Шаг 1: Push на GitHub

Выполните на своём компьютере:

```bash
cd "/Users/bogdan/Documents/WibeCoding Projects/Test project"
git push -u origin main
```

Если попросит авторизацию:
- Username: `bogdanhromenkov-byte`
- Password: используйте **Personal Access Token** (не пароль!)

Как получить токен:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → выберите `repo` scope → Generate
3. Скопируйте токен и используйте вместо пароля

---

## Шаг 2: Деплой на DigitalOcean (АВТОМАТИЧЕСКИ!)

### Подготовка SSH ключа (один раз):

```bash
# Если у вас ещё нет SSH ключа
ssh-keygen -t rsa -b 4096

# Скопировать ключ на сервер
ssh-copy-id root@ваш_ip_адрес
```

### Запуск автоматического деплоя:

```bash
# Дать права на выполнение
chmod +x auto_deploy.sh

# Запустить деплой (замените на ваш IP)
./auto_deploy.sh 142.93.45.123

# Или с доменом:
./auto_deploy.sh 142.93.45.123 estate.example.com
```

**Всё!** Скрипт автоматически:
- ✅ Обновит систему
- ✅ Установит Python, Nginx, Supervisor
- ✅ Скачает ваш код
- ✅ Настроит базу данных
- ✅ Настроит автозапуск
- ✅ Настроит веб-сервер
- ✅ Настроит firewall

**Время:** 5-10 минут

---

## Шаг 3: Обновление кода

Когда изменили код локально:

```bash
# 1. Закоммитить изменения
git add .
git commit -m "Описание изменений"
git push origin main

# 2. Обновить на сервере (АВТОМАТИЧЕСКИ!)
chmod +x update_deploy.sh
./update_deploy.sh ваш_ip_адрес
```

**Готово!** Сайт обновлён за 30 секунд.

---

## 🔧 Полезные команды

### Проверить статус:
```bash
ssh root@ваш_ip 'supervisorctl status estate'
```

### Посмотреть логи:
```bash
ssh root@ваш_ip 'tail -f /var/log/estate/estate.err.log'
```

### Перезапустить:
```bash
ssh root@ваш_ip 'supervisorctl restart estate'
```

### Подключиться к серверу:
```bash
ssh root@ваш_ip
```

---

## 🌐 Настройка домена (опционально)

Если у вас есть домен (например `estate.com`):

1. **В панели домена** добавьте A-запись:
   ```
   Type: A
   Host: @
   Value: ваш_ip_адрес
   TTL: 3600
   ```

2. **Запустите деплой с доменом:**
   ```bash
   ./auto_deploy.sh ваш_ip estate.com
   ```

3. **Установите SSL (скрипт спросит автоматически)**

**Результат:** `https://estate.com` с зелёным замочком! 🔒

---

## 🐛 Решение проблем

### Не могу подключиться к серверу:
```bash
# Проверьте SSH ключ
ssh-copy-id root@ваш_ip

# Или подключитесь с паролем
ssh root@ваш_ip
```

### Сайт не открывается:
```bash
# Проверьте статус
ssh root@ваш_ip 'supervisorctl status estate'
ssh root@ваш_ip 'systemctl status nginx'

# Перезапустите
ssh root@ваш_ip 'supervisorctl restart estate'
ssh root@ваш_ip 'systemctl restart nginx'
```

### Посмотреть ошибки:
```bash
ssh root@ваш_ip 'tail -50 /var/log/estate/estate.err.log'
```

---

## 📝 Что дальше?

После успешного деплоя вы можете:

1. **Добавить функции** - редактируйте код локально, пушьте на GitHub, обновляйте сервер
2. **Интегрировать с Bitrix** - используйте REST API или iframe
3. **Настроить домен** - следуйте инструкции выше
4. **Добавить SSL** - скрипт сделает автоматически

---

## 💡 Совет

Сохраните IP адрес сервера:
```bash
echo "export ESTATE_SERVER=142.93.45.123" >> ~/.bashrc
source ~/.bashrc

# Теперь можно:
./update_deploy.sh $ESTATE_SERVER
```

**Удачи!** 🚀

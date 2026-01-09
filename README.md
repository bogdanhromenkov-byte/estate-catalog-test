# 🏠 Каталог недвижимости для Bitrix24

Профессиональное веб-приложение для управления каталогом недвижимости с интеграцией в Bitrix24.

## 📋 Что это?

Это веб-каталог для просмотра и управления объектами недвижимости, который:
- ✅ Встраивается в Bitrix24 через iframe
- ✅ Предоставляет REST API для интеграции
- ✅ Хранит данные на сервере (SQLite база данных)
- ✅ Автоматически деплоится на DigitalOcean
- ✅ Защищен и готов к production использованию

## 🚀 Быстрый старт

### Что уже работает:
- Сервер развернут на: **http://164.92.223.4**
- GitHub репозиторий: https://github.com/bogdanhromenkov-byte/estate-catalog-test
- Автодеплой настроен

### Обновление на сервере:

1. **Закоммитьте изменения локально:**
```bash
git add .
git commit -m "Описание изменений"
git push origin main
```

2. **Обновите на сервере (автоматически):**
```bash
./update_deploy.sh 164.92.223.4
```

Готово! Сайт обновлен за 30 секунд.

## 🔧 Интеграция с Bitrix24

### Способ 1: iframe (Самый простой)

1. В Bitrix24 перейдите: **Сайты → Страницы → Создать**
2. Вставьте код:

```html
<iframe
    src="http://164.92.223.4"
    width="100%"
    height="1200px"
    frameborder="0"
    style="border: none; min-height: 100vh;">
</iframe>
```

3. Сохраните - каталог теперь внутри Bitrix24!

### Способ 2: REST API

Доступные endpoints:

```bash
# Получить все объекты
GET http://164.92.223.4/api/properties

# Получить один объект
GET http://164.92.223.4/api/properties/1

# Создать объект
POST http://164.92.223.4/api/properties
Content-Type: application/json

{
  "title": "Новая квартира",
  "price": 5000000,
  "address": "Москва, ул. Ленина, 10",
  "property_type": "Apartment",
  "rooms": 2,
  "area": 65.5
}
```

Полная документация API в файле [BITRIX_INTEGRATION.md](BITRIX_INTEGRATION.md)

## 📂 Где хранятся данные?

**База данных находится на сервере:**
- Путь: `/home/estate/estate-catalog/instance/estate.db`
- Тип: SQLite (простая и надежная)
- Бэкап: автоматически при обновлении

**Добавление объектов:**
- Через веб-форму: http://164.92.223.4/add
- Через REST API (см. выше)
- Напрямую в базе (для массовой загрузки)

## 🔐 Безопасность (ВАЖНО!)

После первого деплоя нужно настроить безопасность:

### 1. Укажите ваш Bitrix24 домен

Подключитесь к серверу:
```bash
ssh root@164.92.223.4
```

Отредактируйте `.env`:
```bash
nano /home/estate/estate-catalog/.env
```

Измените:
```bash
# Вместо * укажите ваш реальный домен Bitrix24
BITRIX24_DOMAIN=https://your-company.bitrix24.ru
ALLOWED_ORIGINS=https://your-company.bitrix24.ru
```

Перезапустите:
```bash
supervisorctl restart estate
```

### 2. SECRET_KEY

При первом деплое автоматически генерируется уникальный ключ. Проверить можно:
```bash
ssh root@164.92.223.4 'cat /home/estate/estate-catalog/.env'
```

## 📊 Структура проекта

```
estate-catalog/
├── main.py              # Основное приложение Flask
├── models.py            # Модели базы данных
├── api.py               # REST API endpoints
├── requirements.txt     # Python зависимости
├── .env.example         # Пример конфигурации
├── templates/           # HTML шаблоны
│   ├── index.html       # Список объектов
│   ├── property_detail.html
│   └── add_property.html
├── static/              # CSS, JS, изображения
│   ├── css/
│   └── js/
├── auto_deploy.sh       # Скрипт автоматического деплоя
└── update_deploy.sh     # Скрипт быстрого обновления
```

## 🛠 Полезные команды

### Проверить статус на сервере:
```bash
ssh root@164.92.223.4 'supervisorctl status estate'
```

### Посмотреть логи:
```bash
ssh root@164.92.223.4 'tail -f /var/log/estate/estate.err.log'
```

### Перезапустить приложение:
```bash
ssh root@164.92.223.4 'supervisorctl restart estate'
```

### Бэкап базы данных:
```bash
ssh root@164.92.223.4 'cp /home/estate/estate-catalog/instance/estate.db ~/backup_$(date +%Y%m%d).db'
```

## 📈 Следующие шаги

### Сейчас доступно:
- ✅ Просмотр каталога
- ✅ Добавление объектов вручную
- ✅ REST API
- ✅ Поиск и фильтрация
- ✅ Интеграция с Bitrix24 (iframe)

### Можно добавить позже:
- 🔜 Автоматический подбор объектов по параметрам клиента
- 🔜 Загрузка объектов из Excel/CSV
- 🔜 Автоматическая синхронизация с Bitrix24
- 🔜 Фотогалереи для объектов
- 🔜 Уведомления в Telegram

## ❓ Вопросы и поддержка

Если что-то не работает:

1. Проверьте логи: `ssh root@164.92.223.4 'tail -50 /var/log/estate/estate.err.log'`
2. Проверьте статус: `ssh root@164.92.223.4 'supervisorctl status estate'`
3. Перезапустите: `ssh root@164.92.223.4 'supervisorctl restart estate'`

## 📝 История изменений

- **2026-01-09**: Исправлена безопасность (SECRET_KEY, CORS)
- **2026-01-09**: Добавлена поддержка .env конфигурации
- **2026-01-09**: Первый деплой на production

---

**Версия:** 1.0.0
**Статус:** Production Ready ✅

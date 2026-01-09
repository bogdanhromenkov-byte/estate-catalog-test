# 🔗 Интеграция с Bitrix24

## Способ 1: iframe (Простейший) ⭐

### Встроить каталог в Bitrix24:

1. **Создайте страницу в Bitrix24:**
   - Перейдите: **Сайты** → **Страницы** → **Создать**
   - Или: **Знания** → **Создать страницу**

2. **Вставьте код:**

```html
<iframe 
    src="http://164.92.223.4" 
    width="100%" 
    height="1200px" 
    frameborder="0"
    style="border: none; min-height: 100vh;">
</iframe>
```

3. **Сохраните и опубликуйте**

**Готово!** Каталог работает внутри Bitrix24.

---

## Способ 2: Добавить в меню Bitrix24

1. **Bitrix24** → **Настройки** → **Настройка меню**
2. **Добавить пункт:**
   - Название: `📋 Недвижимость`
   - URL: `http://164.92.223.4`
   - Иконка: 🏠
   - Открывать: `В iframe` или `В новой вкладке`

---

## Способ 3: REST API (Полная интеграция) 🚀

### API Endpoints:

**Base URL:** `http://164.92.223.4/api`

### Получить все объекты:
```http
GET /api/properties
```

**Ответ:**
```json
[
  {
    "id": 1,
    "title": "Modern Apartment",
    "description": "Beautiful apartment...",
    "price": 325000,
    "address": "New York, 5th Avenue, 123",
    "property_type": "Apartment",
    "rooms": 3,
    "area": 85.5,
    "floor": 7,
    "total_floors": 16,
    "image_url": "https://...",
    "created_at": "2026-01-09T01:20:00"
  }
]
```

---

### Получить один объект:
```http
GET /api/properties/1
```

---

### Создать объект (из Bitrix):
```http
POST /api/properties
Content-Type: application/json

{
  "title": "New Apartment",
  "description": "Great location",
  "price": 250000,
  "address": "Chicago, Main St, 456",
  "property_type": "Apartment",
  "rooms": 2,
  "area": 65.0,
  "floor": 5,
  "total_floors": 10,
  "image_url": "https://example.com/image.jpg"
}
```

**Ответ:**
```json
{
  "success": true,
  "id": 6,
  "message": "Property created successfully"
}
```

---

### Обновить объект:
```http
PUT /api/properties/1
Content-Type: application/json

{
  "price": 280000,
  "description": "Updated description"
}
```

---

### Удалить объект:
```http
DELETE /api/properties/1
```

---

### Проверка работоспособности:
```http
GET /api/health
```

**Ответ:**
```json
{
  "status": "ok",
  "properties_count": 5
}
```

---

## Настройка в Bitrix24

### Автоматическое создание объектов из сделок:

1. **Bitrix24** → **CRM** → **Настройки** → **Бизнес-процессы**

2. **Создайте бизнес-процесс:**
   - Триггер: "При создании сделки"
   - Условие: "Тип сделки = Недвижимость"
   - Действие: "Webhook"

3. **Настройте Webhook:**
   - URL: `http://164.92.223.4/api/properties`
   - Метод: `POST`
   - Тело запроса:
   ```json
   {
     "title": "{TITLE}",
     "description": "{COMMENTS}",
     "price": "{OPPORTUNITY}",
     "address": "{ADDRESS}",
     "property_type": "Apartment",
     "rooms": "{UF_ROOMS}",
     "area": "{UF_AREA}"
   }
   ```

**Теперь:** Создали сделку в Bitrix → автоматически добавилось в каталог! ✅

---

## Примеры использования API

### JavaScript (для Bitrix24):

```javascript
// Получить все объекты
fetch('http://164.92.223.4/api/properties')
  .then(response => response.json())
  .then(data => console.log(data));

// Создать объект
fetch('http://164.92.223.4/api/properties', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Luxury Villa',
    price: 1500000,
    address: 'Miami Beach',
    property_type: 'House',
    rooms: 6,
    area: 350
  })
})
.then(response => response.json())
.then(data => console.log('Created:', data));
```

---

### Python (для автоматизации):

```python
import requests

# Получить объекты
response = requests.get('http://164.92.223.4/api/properties')
properties = response.json()

# Создать объект
new_property = {
    'title': 'Penthouse',
    'price': 950000,
    'address': 'New York, Manhattan',
    'property_type': 'Apartment',
    'rooms': 4,
    'area': 180
}
response = requests.post('http://164.92.223.4/api/properties', json=new_property)
print(response.json())
```

---

### cURL (для тестирования):

```bash
# Получить все объекты
curl http://164.92.223.4/api/properties

# Создать объект
curl -X POST http://164.92.223.4/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Property",
    "price": 300000,
    "address": "Test Address",
    "property_type": "Apartment"
  }'

# Проверить здоровье API
curl http://164.92.223.4/api/health
```

---

## Безопасность API

Для production добавьте аутентификацию:

1. **API ключи**
2. **OAuth токены**
3. **JWT токены**

Я могу добавить любой из этих методов, если нужно!

---

## Что дальше?

1. **Простой старт:** Используйте iframe (Способ 1)
2. **Если нужна синхронизация:** Настройте webhook в Bitrix24
3. **Для полной интеграции:** Используйте REST API

**Какой способ хотите попробовать?** 😊

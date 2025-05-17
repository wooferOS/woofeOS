# woofeOS

**Woofer SMM Helper Bot** – Telegram-бот для автоматизації TikTok-контенту з використанням GPT 🐶🍔

---

## 📦 Встановлення

### 1. Клонувати репозиторій:

```bash
git clone https://github.com/wooferOS/woofeOS.git
cd woofeOS
```

### 2. 🔧 Установка залежностей:

```bash
pip install -r requirements.txt
```

---

## 🔐 Секрети (GitHub Actions)

У репозиторії вже налаштовані змінні середовища для GPT і Telegram:

- `TELEGRAM_API_TOKEN` – токен Telegram-бота  
- `OPENAI_API_KEY` – ключ до OpenAI GPT

> 🛡️ Не потрібно створювати `.env` вручну — секрети автоматично доступні при деплої через GitHub або Render.

---

## 🚀 Запуск

### 1. Локально (для розробки):

```bash
python main.py
```

### 2. На Render.com:

- Задати `Build Command`:  
  `pip install -r requirements.txt`

- `Start Command`:  
  `gunicorn main:app`

- Тип сервісу: **Web Service**  
- `PORT`: **10000**
- Увімкнути Webhook для Telegram:  
  `https://<твоє-доменне-ім’я>.onrender.com`

---

## 📁 Структура

```
├── main.py            # Основна логіка бота
├── requirements.txt   # Залежності
├── Procfile           # Команда для gunicorn
├── .gitignore         # Ігнорування системних файлів
└── README.md          # Ця інструкція
```

---

## 👨‍💻 Автор

Розроблено для TikTok-акаунту **ChefWoofTV** — смішні відео з цуценятами-кухарями.


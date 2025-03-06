# 🚀 Проект задеплоен на Railway и доступен по тегу @VoiceAIBot_test_task_bot в телеграме

# Telegram Voice AI Bot

Этот бот для Telegram использует OpenAI API (Whisper, Assistant API, TTS) для обработки голосовых сообщений. Вы можете пообщаться с ним по душам или спросить что-то волнующее вас.

## 🚀 Функционал
- Распознавание голосовых сообщений с помощью Whisper.
- Генерация ответов на сообщения с помощью Assistant API.
- Озвучивание текстовых ответов с помощью OpenAI TTS.

---

## 🔧 Локальный запуск
##### 1. Установление зависимостей
```sh
pip install -r requirements.txt
```
##### 2. FFmpeg
```sh
sudo apt-get install ffmpeg
```
(или скачайте с [официального сайта](https://ffmpeg.org/download.html))

##### 3. Создание `.env` файла
Создайте файл `.env` в корневой директории и добавьте:
```env
TG_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
FFMPEG_PATH=/usr/bin/ffmpeg **или свой путь до FFMPEG**
```

##### 4. Запуск
```sh
python -m app.main
```

---

## 🐳 Запуск в Docker

```sh
docker compose up --build
```




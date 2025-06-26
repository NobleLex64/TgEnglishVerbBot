#!/bin/bash

set -e  # Прекратить выполнение при ошибке

cd "$(dirname "$0")"

echo "Проверка папок..."

mkdir -p "data/database"
echo "Папка data/database создана или уже существует."

mkdir -p "data/image"
echo "Папка data/image создана или уже существует."

mkdir -p "data/backgroundimage"
echo "Папка data/backgroundimage создана или уже существует."

mkdir -p "logs"
echo "Папка logs создана или уже существует."

echo "Введите значение для BOT_TOKEN:"
read -r BOT_TOKEN
if [ -z "$BOT_TOKEN" ]; then
    echo "BOT_TOKEN не может быть пустым. Попробуйте снова."
    exit 1
fi

echo "Введите значение для каналов, на которые нужно подписаться;\nНапример:@channel_1,@channel_2,...;\nCHANNEL_USERNAMES:"
read -r CHANNEL

env_file="code/.env"
if [ ! -f "$env_file" ]; then
    cat > "$env_file" <<EOL
BOT_TOKEN=$BOT_TOKEN

CHANNEL_USERNAMES=$CHANNEL
ADMIN_ID=1

DB_PATH=./data/database/EnLessonsBot.db
IMAGE_PATH=./data/image/
TEXT_PATH=./data/irregularverbs/sqlite_verbs.txt
BACKGROUND_IMG_PATH=./data/backgroundimage/
LOG_PATH=./logs/logs.db
BOT_TEXT_PATH=./data/text/bot_text.txt

VERBS_COUNT=159
VERB_ON_PAGE=15

VERB_TEXT_COLOR=0xDC140C
VERB_TRANSLATION_COLOR=0x228B22
FONT =/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf

CARTS_WIDTH=800
CARTS_HEIGHT=450
CARTS_BACKGROUND_COLOR=0xFFFFFFE0
CARTS_TEXT_SIZE=40

TABLE_WIDTH=1600
TABLE_HEIGHT=900
TABLE_BACKGROUND_COLOR=0xFFFFFF00
TABLE_HEADER_TEXT_COLOR=0x4040FF
TABLE_HEADER_TEXT_SIZE=30
TABLE_TEXT_SIZE=25
EOL
    echo "Файл .env создан в code/."
else
    echo "Файл .env уже существует."
fi

echo "Установка зависимостей..."
pip install python-dotenv Pillow aiofiles aiosqlite nest-asyncio asyncio python-telegram-bot
if [ $? -ne 0 ]; then
    echo "Ошибка при установке библиотек."
    exit 1
fi

echo "Установка прав на выполнение .sh файлов..."
chmod +x irregular_verb_bot.sh

if ! python3 "code/create_new_database.py"; then
    echo "Ошибка при выполнении create_new_database.py"
    exit 1
fi

if ! python3 "code/create_image_for_bot.py"; then
    echo "Ошибка при выполнении create_image_for_bot.py"
    exit 1
fi

echo "Скрипт выполнен успешно."

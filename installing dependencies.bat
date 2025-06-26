@echo off

chcp 65001
cd /d "%~dp0"

:: Проверка и создание папок
echo Проверка папок...

if not exist "data/database" (
    mkdir "data/database"
    echo Папка data/database создана.
) else (
  echo Папка data/database уже существует.
)

if not exist "data/image" (
    mkdir "data/image"
    echo Папка data/image создана.
) else (
  echo Папка data/image уже существует.
)

if not exist "data/backgroundimage" (
    mkdir "data/backgroundimage"
    echo Папка data/backgroundimage создана.
) else (
  echo Папка data/backgroundimage уже существует.
)

if not exist "logs" (
    mkdir "logs"
    echo Папка logs создана.
) else (
  echo Папка logs уже существует.
)

echo Проверка файлов и запись текста...

echo Введите значение для BOT_TOKEN:
set /p BOT_TOKEN=
if "%BOT_TOKEN%"=="" (
  echo BOT_TOKEN не может быть пустым. Попробуйте снова.
  goto input_loop
)
echo Введите значение для канала\ов на которые нужно подписаться:
echo например:@имя_канала_1,@имя_канала_2, и тд...
echo CHANNEL_USERNAMES:
set /p CHANNEL=

if not exist ".\code\.env" (
  (
  echo BOT_TOKEN=%BOT_TOKEN%
  echo ......................................................
  echo CHANNEL_USERNAMES=%CHANNEL%
  echo ADMIN_ID=1
  echo ......................................................
  echo DB_PATH=./data/database/EnLessonsBot.db
  echo IMAGE_PATH=./data/image/
  echo TEXT_PATH=./data/irregularverbs/sqlite_verbs.txt
  echo BACKGROUND_IMG_PATH=./data/backgroundimage/
  echo LOG_PATH=./logs/logs.db
  echo BOT_TEXT_PATH=./data/text/bot_text.txt
  echo ......................................................
  echo VERBS_COUNT=159
  echo VERB_ON_PAGE=15
  echo ......................................................
  echo VERB_TEXT_COLOR=0xDC140C
  echo VERB_TRANSLATION_COLOR=0x228B22
  echo FONT =/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
  echo ......................................................
  echo CARTS_WIDTH=800
  echo CARTS_HEIGHT=450
  echo CARTS_BACKGROUND_COLOR=0xFFFFFFE0
  echo CARTS_TEXT_SIZE=40
  echo ......................................................
  echo TABLE_WIDTH=1600
  echo TABLE_HEIGHT=900
  echo TABLE_BACKGROUND_COLOR=0xFFFFFF00
  echo TABLE_HEADER_TEXT_COLOR=0x4040FF
  echo TABLE_HEADER_TEXT_SIZE=30
  echo TABLE_TEXT_SIZE=25
  
  ) > ".\code\.env"
  echo Файл .env создан в ".\code\".
) else (
  echo Файл .env уже существует.
)

pip install python-dotenv Pillow aiofiles aiosqlite nest-asyncio asyncio python-telegram-bot
if %errorlevel% neq 0 (
  echo Ошибка при установке библиотек.
  pause
  exit /b
)

python code/create_new_database.py
if errorlevel 1 (
    echo Ошибка при выполнении create_new_database.py
    pause
    exit /b 1
)

python code/create_image_for_bot.py
if errorlevel 1 (
    echo Ошибка при выполнении create_image_for_bot.py
    pause
    exit /b 1
)

exit /b
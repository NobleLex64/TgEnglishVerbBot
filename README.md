Для работы бота необходимы следущее:
  Python3: https://www.python.org/downloads/
  Sqlite: https://www.sqlite.org/download.html

  Python for Linux (Ubuntu, Debian): sudo apt update && sudo apt install python3
  Sqlite for Linux (Ubuntu, Debian): sudo apt update && sudo apt install -y sqlite3

1) Windows:
    git clone https://github.com/NobleLex64/TgEnglishVerbBot.git; cd TgEnglishVerbBot; ./installing_dependencies.bat

   Linux: 
    git clone https://github.com/NobleLex64/TgEnglishVerbBot.git && cd TgEnglishVerbBot && chmod +x installing_dependencies.sh && ./installing_dependencies.sh

1) Что вводить в окне:
    
  Введите значение для BOT_TOKEN:
  >>сюда ваш токен из Bot_Father

  Введите значение для каналов, на которые нужно подписаться;
  Например:@channel_1,@channel_2,...;
  CHANNEL_USERNAMES:
  >>сюда ссылки на каналы на которое нужно подписатьтя для доступа к боту

2) Как запустить самого бота:

  -- Если все действия выше были выполнены, достаточно будет ввести в консоль: 
      Windows: ./irregular_verb_bot.bat 
      Linux:   ./irregular_verb_bot.sh

3) Для того, чтобы добавить админа:

  -- в файл code/.env добавьте в ADMIN_ID=свой id

  свой id можно узнать посмотрев в базе данных EnLessonsBot.db, запустив бота и написав ему /start
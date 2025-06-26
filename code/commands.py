from telegram.ext   import ContextTypes
from telegram       import Update, InlineKeyboardButton, InlineKeyboardMarkup

from help_functions  import *
from globals         import DB_PATH, IMAGE_PATH, ADMIN_ID, CHANNEL_USERNAMES, VERBS_INDEXES, VERBS_COUNT, VERBS_ON_PAGE
from loger           import create_log
from session_manager import *
from channel_signed  import *
from db_updater      import add_user_in_db

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id  = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  text = "Это меню администратора"

  keyboard = [
    [InlineKeyboardButton("📈❓ Проверить прогресс студентов", callback_data="stud_progress")],  
    [InlineKeyboardButton("⬅️ Back", callback_data="start")]
  ]  

  try:
    message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id) 
  except Exception as e:
    await create_log(user_id, f"Ошибке в admin: {e}")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id  = update.effective_user.id
  username = update.effective_user.name

  await delete_message(user_id, update.effective_chat.id, context)
  await add_user_in_db(user_id, username)

  if VERBS_INDEXES.get(user_id): 
    del VERBS_INDEXES[user_id]

  if CHANNEL_USERNAMES and CHANNEL_USERNAMES != [""] and not await is_signed(update, context):
    await not_signed(update, context)
    return

  text     = "Привет! Я бот для изучения неправильных глаголов."
  keyboard = [
      [InlineKeyboardButton("❓  Помощь",  callback_data="help_command")],
      [InlineKeyboardButton("📔  Учить неправильные глаголы", callback_data="irregular_verbs")],
      [InlineKeyboardButton("🔣  Таблица неправильных глаголов", callback_data="table")],
      [InlineKeyboardButton("📈  Прогресс", callback_data="progress")],
  ]  

  if ADMIN_ID and user_id == int(ADMIN_ID):
    keyboard.append([InlineKeyboardButton("Меню АДМИНА", callback_data="admin")])  

  try:
    if update.message:
      await context.bot.delete_message(update.effective_chat.id, update.effective_message.id)
      message = await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
      message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id) 
  except Exception as e: 
    await create_log(user_id, f"Ошибка в start: {e}")

# Button: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  text = '''Привет! Я расскажу тебе, что я могу сделать.. 

            '📔 Учить неправильные глаголы'
                - 7 карточек с неправильными глаголами
                - тест по этим глаголам после их изучения
                - оценка и сохранение прогресса, правильно выученных карточек
    
            '🔣 Таблица неправильных глаголов'
                - Таблица с неправильными глаголами 
                - по 15 штук на страницу
                - 11 страниц с 159 глаголами
    
            '📈  Прогресс'
                - эта команда покажет как много глаголов ты успел изучить и сколько еще осталось выучить.
                - также здесь можно сбросить весь прогресс
    
            p.s. Также присутствуют карточки по запросу.
                Пиши в чат глагол или его часть, и получишь карточку с ним)    
        '''

  keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="start")]]
  try:
    message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id) 
  except Exception as e:
    await create_log(user_id, f"Ошибке в help: {e}")

# Button: /irregular_verb
async def irregular_verb(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id  = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  try:
    async with aiosqlite.connect(DB_PATH) as conn:
      cursor   = await conn.execute("SELECT progress FROM users WHERE id = ?", (user_id,))
      row      = await cursor.fetchone()
      progress = bytearray(row[0])

      verbs = find_next_unlearned(progress, 7)
      VERBS_INDEXES[user_id] = { "verbs": verbs, "index": 0, "progress": bytearray(1)}

      if len(VERBS_INDEXES[user_id]) == 0:
        text = "Вы уже изучили все доступные глаголы!"
        keyboard = [ [InlineKeyboardButton("⬅️ Back", callback_data="start")] ]
        message = await update.callback_query.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
        await add_message_id(user_id, message.id)
        return
    
    text = "Вы готовы начать изучение следующего набора глаголов?"
    keyboard = [
      [InlineKeyboardButton("🎫 Приступить к выполнению", callback_data="ok")],
      [InlineKeyboardButton("⬅️ Back", callback_data="start")]
    ]
    message = await update.callback_query.message.reply_text(
      text=text,
      reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id)
  except Exception as e:
    await create_log(user_id, f"Ошибке в irregular_verb: {e}")

# Button: /irregular_verb_table
async def irregular_verb_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id  = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  pages_count = (VERBS_COUNT // VERBS_ON_PAGE) + 1
  pages = []
  for i in range(0, pages_count):
    n = i + 1
    pages.append(f"table_{n}")
  VERBS_INDEXES[user_id] = { "verbs": pages, "index": 0, "progress": None }
  
  text = "Хотите получить таблицу неправильных глаголов?"
  keyboard = [
    [InlineKeyboardButton("🎫 Получить", callback_data="ok")],
    [InlineKeyboardButton("⬅️ Back", callback_data="start")]
  ]
  try:
    message = await update.callback_query.message.reply_text(
      text=text,
      reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await add_message_id(user_id, message.id)
  except Exception as e:
    await create_log(user_id, f"Ошибке в irregular_verb_table: {e}")

# Button: /progress
async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  count = 0
  try:
    async with aiosqlite.connect(DB_PATH) as conn:
      cursor   = await conn.execute("SELECT progress FROM users WHERE id = ?", (user_id,))
      row      = await cursor.fetchone()
      progress = bytearray(row[0])

      for i in range(0, len(progress) * 8):
        if is_bit_set(progress, i):
          count += 1

    text = "Ваш прогресс: " + f"{count}/{len(progress) * 8}"
    keyboard = [
      [InlineKeyboardButton("⬅️ Back", callback_data="start")],
      [InlineKeyboardButton("❌ Delete progress?", callback_data="ask_delete_progress")]
    ]
    message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id)
  except Exception as e:
    await create_log(user_id, f"Ошибке в progress: {e}")

# Help: /progress/ask_delete_progress
async def ask_del_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  text = "Вы точно хотите удались весь ваш прогресс?"
  keyboard = [
    [InlineKeyboardButton("⬅️ Back", callback_data="progress")],
    [InlineKeyboardButton("❌ Delete", callback_data="delete_progress")]
  ]
  try:
    message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id) 
  except Exception as e:
    await create_log(user_id, f"Ошибке в ask_del_progress: {e}")


# Help: /progress/ask_delete_progress/delete
async def del_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)
  
  try:
    async with aiosqlite.connect(DB_PATH) as conn:
      await conn.execute("UPDATE users SET progress = ? WHERE id = ?", (bytearray(VERBS_COUNT // 8), user_id))
      await conn.commit()

    text = "Ваш прогресс был удален! Вы можете начать сначала."
    keyboard = [
      [InlineKeyboardButton("⬅️ Back", callback_data="progress")],
      [InlineKeyboardButton("⬅️⬅️ Menu", callback_data="start")]
    ]

    message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id)
  except Exception as e:
    await create_log(user_id, f"Ошибке в del_progress: {e}")

async def check_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id  = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  result = {}
  try:
    async with aiosqlite.connect(DB_PATH) as conn:
      cursor   = await conn.execute("SELECT username, progress, data_last_update FROM users")
      rows     = await cursor.fetchall()

      for name, progress, data in rows:
        count = sum(1 for i in range(len(progress) * 8) if is_bit_set(progress, i))
        result[name] = {"count": count, "data": data}

    text = ''
    keyboard = [
      [InlineKeyboardButton("⬅️ Back", callback_data="admin")]
    ]  

    for name, cd in result.items():
      text += f"'{name}':\n    Выученно глаголов: '{cd["count"]}'\n    Дата последнего входа: '{cd["data"]}'\n\n"

    message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id)
  except Exception as e:
    await create_log(user_id, f"Ошибке в check_progress: {e}")

# Echo handler, send ans. on your req.
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context) # no except function
  await context.bot.delete_message(update.effective_chat.id, update.message.id) # no except, because it only works on message

  if update.message.text.startswith("/"):
    return

  if VERBS_INDEXES.get(user_id): 
    del VERBS_INDEXES[user_id]

  functions = [ search_present_simple, search_past_simple, search_past_participle ]
  verb      = update.message.text.lower() # no except

  for function in functions:
    verb_id = await function(verb, DB_PATH)
    if verb_id:
      image_path = IMAGE_PATH + str(verb_id) + '.png'
      try:
        img      = get_image(image_path)
        keyboard = [ [InlineKeyboardButton("⬅️ Back", callback_data="start")] ]
        message  = await update.message.reply_photo(img, reply_markup=InlineKeyboardMarkup(keyboard))
        await add_message_id(user_id, message.id)
        return
      except Exception as e:
        await create_log(user_id, f"Ошибка в echo: {e}")
        return
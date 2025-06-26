from globals      import CHANNEL_USERNAMES
from telegram     import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ContextTypes
from loger        import create_log
from session_manager import delete_message, add_message_id


async def is_signed(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id   = update.effective_user.id
  bot: Bot  = context.bot

  try:
    for CHANNEL_USERNAME in CHANNEL_USERNAMES:
      member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
      status = member.status
      if status not in ["member", "administrator", "creator"]:
        False
  except Exception as e:
    await create_log(user_id, f"Ошибка в функции check_subscrption: {e}")
    return False  
  
  return True

async def not_signed(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  text = "Привет ты еще не подписался на канал! Прежде чем начать пользоваться моим функционалом подпишись на " + ', '.join(CHANNEL_USERNAMES) + '!'
  keyboard = [
      [InlineKeyboardButton("Я подписался!", callback_data="not_signed")]
  ]
  
  try:
    if update.message:
      await context.bot.delete_message(update.effective_chat.id, update.effective_message.id)
      message = await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
      message = await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    await add_message_id(user_id, message.id) 
  except Exception as e:
    await create_log(user_id, f"Ошибка в функции not_signed: {e}")

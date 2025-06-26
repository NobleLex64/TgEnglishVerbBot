import asyncio
import nest_asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from globals  import BOT_TOKEN
from commands import *
from loger    import start_writing_log
from handlers import button_handler

nest_asyncio.apply()

async def start_bot():
  app = Application.builder().token(BOT_TOKEN).build()
  app.add_handler(CommandHandler('start', start))
  app.add_handler(MessageHandler(filters.TEXT, echo))
  app.add_handler(CallbackQueryHandler(button_handler))
  log_task = app.create_task(start_writing_log())
  
  print("bot started!")
  try: 
    app.run_polling()
  except Exception as e:
    print("bot is close!")

if __name__ == "__main__": 
  asyncio.run(start_bot())
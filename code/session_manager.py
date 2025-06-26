import time

from telegram.ext import ContextTypes
from globals import LAST_MESSAGE, IMAGES_CASH
from loger import create_log

## message buffer functions ##

async def add_message_id(user_id: int, message_id: int) -> None:
  messages_id = []
  if LAST_MESSAGE.get(user_id) is not None:
    for message in LAST_MESSAGE[user_id]:
      messages_id.append(message)
  messages_id.append(message_id)
  LAST_MESSAGE[user_id] = messages_id

async def delete_message(user_id: int, chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
  message_id = LAST_MESSAGE.get(user_id)
  if message_id is not None and len(message_id) != 0:
    message_id = LAST_MESSAGE[user_id][0]
    await clean_messages_buffer(user_id)
    try:
      await context.bot.delete_message(chat_id, message_id)
    except Exception as e:
      await create_log(user_id, f"Ошибка в delete_messege: {e}")

async def clean_messages_buffer(user_id: int) -> None: 
   if LAST_MESSAGE.get(user_id):
    del LAST_MESSAGE[user_id]
## end message functions ##

## image cash functions ##

def get_image(image_path: str) -> bytes:
  current_time = time.time()
  cached_image = IMAGES_CASH.get(image_path)
  if cached_image:
    return cached_image['data']
  else:
    return add_image_in_cash(image_path, current_time)
  
def add_image_in_cash(image_path: str, current_time: float) -> bytes:
  with open(image_path, 'rb') as f:
    image_data = f.read()
    IMAGES_CASH[image_path] = {'data': image_data, 'timestamp': current_time}
    return image_data
## end image cash functions ##
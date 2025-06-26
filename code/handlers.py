from telegram     import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from verbs_test      import test, correct_quiz, incorrect_quiz
from channel_signed  import is_signed, not_signed
from commands        import *
from session_manager import get_image, add_message_id, delete_message
from globals         import IMAGE_PATH, VERBS_INDEXES, VERBS_COUNT, VERBS_ON_PAGE
from loger           import create_log


async def send_button_interface(update: Update, user_id: int, verb_id: int, keyboard) -> None:
  if verb_id:
    reply_markup = InlineKeyboardMarkup(keyboard)
    image_path   = IMAGE_PATH + str(verb_id) + '.png'
    img          = get_image(image_path)
    message      = await update.callback_query.message.reply_photo(photo=img, reply_markup=reply_markup)
    await add_message_id(user_id, message.id)
  else:
    await create_log(user_id, "Проблема с индексом глаголов")

# ## START BUTTON HANDLER SEGMENT
async def button_ok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  usr_verbs: dict = VERBS_INDEXES.get(user_id)
  verb_id: int    = usr_verbs.get("verbs")[0]
  keyboard        = [
    [InlineKeyboardButton("⬅️ Exit", callback_data="start"),
    InlineKeyboardButton("Next", callback_data="next")]
  ]
  await send_button_interface(update, user_id, verb_id, keyboard)
  
# # Handler for button 'next'
async def button_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  usr_verbs: dict    = VERBS_INDEXES.get(user_id)
  verbs_id: list     = usr_verbs.get("verbs")
  index: int         = usr_verbs.get("index") + 1
  usr_verbs["index"] = index
  verb_id: int       = verbs_id[index]

  if index == (len(verbs_id) - 1):
    
    keyboard = [
      [
        InlineKeyboardButton("Prev", callback_data="prev")
      ],
      [
        InlineKeyboardButton("⬅️ Exit", callback_data="start"),
      ]
    ]
    if index != (VERBS_COUNT // VERBS_ON_PAGE):
      keyboard[0].append(InlineKeyboardButton("start test", callback_data="test"))
  else:
    keyboard = [
        [
            InlineKeyboardButton("Prev", callback_data="prev"),
            InlineKeyboardButton("Next", callback_data="next"),
        ],
        [
            InlineKeyboardButton("⬅️ Exit", callback_data="start"),
        ]
    ]

  await send_button_interface(update, user_id, verb_id, keyboard)

# # Handler for button 'prev' -> void
async def button_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  usr_verbs: dict    = VERBS_INDEXES.get(user_id)
  verbs_id: list     = usr_verbs.get("verbs")
  index: int         = usr_verbs.get("index") - 1
  usr_verbs["index"] = index
  verb_id: int       = verbs_id[index]

  if index != 0:
    keyboard = [
        [
            InlineKeyboardButton("Prev", callback_data="prev"),
            InlineKeyboardButton("Next", callback_data="next"),
        ],
        [
            InlineKeyboardButton("⬅️ Exit", callback_data="start"),
        ]
    ]
  else:
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Exit", callback_data="start"),
            InlineKeyboardButton("Next", callback_data="next")
        ]
    ]

  await send_button_interface(update, user_id, verb_id, keyboard)

# # Handler for button 'test' irregular verbs test -> void
async def button_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)

  usr_verbs: dict    = VERBS_INDEXES.get(user_id)
  usr_verbs["index"] = 0
  await test(update, context)

# Handler for buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    qdata = query.data

    if qdata == "not_signed":
      if await is_signed(update, context):
        qdata = "start"
      else: 
        qdata = "not_signed"

    button_command = {
      "admin": admin,
      "start": start,
      "help_command": help_command,
      "irregular_verbs": irregular_verb,
      "table": irregular_verb_table,
      "progress": progress,
      "ask_delete_progress": ask_del_progress,
      "delete_progress": del_progress,
      "stud_progress": check_progress,
      "ok": button_ok,
      "next": button_next,
      "prev": button_prev,
      "test": button_test,
      "correct": correct_quiz,
      "incorrect": incorrect_quiz,
      "not_signed": not_signed
    }

    user_id = update.effective_user.id
    action  = button_command.get(qdata)

    if action:
      await action(update, context)
    else:
      await create_log(user_id, f"Команда не существует!")
#
## END BOTTOM SEGMENT
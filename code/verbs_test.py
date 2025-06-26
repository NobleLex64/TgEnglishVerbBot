import io
import random
import aiosqlite

from io           import BytesIO
from telegram     import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from PIL          import Image, ImageDraw, ImageFont

from globals         import DB_PATH, VERBS_INDEXES
from db_updater      import upd_usr_progress
from session_manager import add_message_id, delete_message
from help_functions  import is_bit_set
from loger           import create_log

verb_form = ["Present Simple (1)", "Past Simple (2)", "Past Participle (3)"]

def create_image_test_card(form, verb):
    width, height = 800, 450
    text_color, background_color = (30, 105, 255), (255, 255, 255)
    word_color = (255, 10, 10)
    img = Image.new("RGBA", (width, height), background_color)

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    text_1 = "Выберите для глагола: "
    text_2 = f"'{verb}'"
    text_3 = "его"
    text_4 = f"'{form}'"
    text_5 = "форму"

    draw.text((200, 100), text_1, font=font, fill=text_color)
    draw.text((400 - (len(verb) * 10), 200), text_2, font=font, fill=word_color)
    draw.text((130, 300), text_3, font=font, fill=text_color)
    draw.text((220, 300), text_4, font=font, fill=word_color)
    draw.text((590, 300), text_5, font=font, fill=text_color)

    return img

def quiz_1(verbs):
    correct_form_index   = random.randint(0, 2)
    form                 = verb_form[correct_form_index]
    correct_verb_index   = random.randint(0, 2)

    part_incorrect_verb  = verbs[0].split()
    incorrect_1 = part_incorrect_verb[0] + "ed " + part_incorrect_verb[1].replace("]", "d]")
    incorrect_2 = part_incorrect_verb[0] + "en " + part_incorrect_verb[1].replace("]", "n]")

    img = create_image_test_card(form, verbs[3])

    j = True
    keyboard = []
    for i in range(3):
        if i == correct_verb_index:
            keyboard.append(
                [InlineKeyboardButton(verbs[0], callback_data="correct")]
            )
        else:
            verb = incorrect_1 if j == True else incorrect_2
            keyboard.append(
                [InlineKeyboardButton(verb, callback_data="incorrect")]
            )
            j = False

    return img, keyboard

def quiz_2(verbs):
    correct_form_index = random.randint(0, 2)
    form               = verb_form[correct_form_index]
    correct_verb_index = random.randint(0, 2)

    img = create_image_test_card(form, verbs[3])

    keyboard = []
    for i in range(3):
        if i == correct_verb_index:
            keyboard.append(
                [InlineKeyboardButton(verbs[correct_form_index], callback_data="correct")]
            )
        else:
            j = i if i != correct_form_index else correct_verb_index
            keyboard.append(
                [InlineKeyboardButton(verbs[j], callback_data="incorrect")]
            )

    return img, keyboard

def quiz_3(verbs):
    form = verb_form[1]
    correct_verb_index = random.randint(0, 2)

    img = create_image_test_card(form, verbs[3])

    keyboard = []
    for i in range(3):
        if i == correct_verb_index:
            keyboard.append(
                [InlineKeyboardButton(verbs[1], callback_data="correct")]
            )
        else:
            j = i if i != 1 else correct_verb_index
            keyboard.append(
                [InlineKeyboardButton(verbs[j], callback_data="incorrect")]
            )

    return img, keyboard

def quiz_4(verbs):
    form = verb_form[0]
    correct_verb_index = random.randint(0, 2)

    img = create_image_test_card(form, verbs[3])

    keyboard = []
    for i in range(3):
        if i == correct_verb_index:
            keyboard.append(
                [InlineKeyboardButton(verbs[0], callback_data="correct")]
            )
        else:
            j = i if i != 0 else correct_verb_index
            keyboard.append(
                [InlineKeyboardButton(verbs[j], callback_data="incorrect")]
            )

    return img, keyboard

async def send_quiz(update: Update, verbs):
    user_id = update.effective_user.id

    if verbs[0] == verbs[1] == verbs[2]:
        img, keyboard = quiz_1(verbs)
    elif verbs[0] != verbs[1] != verbs[2]:
        img, keyboard = quiz_2(verbs)
    elif (verbs[0] == verbs[2]) and (verbs[1] != verbs[2]):
        img, keyboard = quiz_3(verbs)
    else:
        img, keyboard = quiz_4(verbs)

    try:
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        message = await update.callback_query.message.reply_photo(photo=buffer, reply_markup=InlineKeyboardMarkup(keyboard))
        await add_message_id(user_id, message.id)
    except Exception as e:
        await create_log(user_id, f"Ошибке в send_quiz: {e}")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id   = update.effective_user.id
    await delete_message(user_id, update.effective_chat.id, context)

    user_dict = VERBS_INDEXES.get(user_id)
    verbs_id  = user_dict["verbs"]
    count     = user_dict["index"]

    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cursor   = await conn.execute(''' 
                SELECT  base_form, past_simple, past_participle, translate
                FROM verbs 
                WHERE id = ?
            ''', (verbs_id[count],))

            verbs = await cursor.fetchone()
    except Exception as e:
        await create_log(user_id, f"Ошибке в test: {e}")
    await send_quiz(update, verbs)

async def correct_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id            = update.effective_user.id
  user_dict          = VERBS_INDEXES.get(user_id)
  count              = user_dict["index"]
  user_dict["index"] = count + 1

  user_dict["progress"][0] |= (1 << count)

  if (count + 1) == len(user_dict["verbs"]):
    await end_test(update, context)
  else:
    await test(update, context)

async def incorrect_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id            = update.effective_user.id
  user_dict          = VERBS_INDEXES.get(user_id)
  count              = user_dict["index"]
  user_dict["index"] = count + 1
  
  if (count + 1) == len(user_dict["verbs"]):
      await end_test(update, context)
  else:
      await test(update, context)
  
async def end_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id       = update.effective_user.id
  await delete_message(user_id, update.effective_chat.id, context)
  
  user_dict     = VERBS_INDEXES.get(user_id)
  verbs_id      = user_dict["verbs"]
  user_progress = user_dict["progress"]
  
  keyboard = [
    [
      InlineKeyboardButton("Menu", callback_data="start")
    ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  
  learned_verbs_id = []
  count = 0
  for i in range(len(verbs_id)):
    if is_bit_set(user_progress, i):  # Проверяем бит в прогрессе
      learned_verbs_id.append(verbs_id[i])
      count += 1
  
  await upd_usr_progress(user_id, learned_verbs_id)
  
  if count == 7:
    text = f"Отлично! Твой результат {count}/7!"
  elif count > 4:
    text = f"Хорошо! Ты был близок. Твой результат {count}/7!"
  elif count > 2:
    text = f"Неплохо, но ты можешь лучше! Твой результат {count}/7!"
  else:
    text = f"Эх, повтори еще раз! Твой результат {count}/7!"
  
  if VERBS_INDEXES.get(user_id):
    del VERBS_INDEXES[user_id]
  
  try:
    message = await update.callback_query.message.reply_text(text, reply_markup=reply_markup)
    await add_message_id(user_id, message.id)
  except Exception as e:
    await create_log(user_id, f"Ошибке в end_test: {e}")
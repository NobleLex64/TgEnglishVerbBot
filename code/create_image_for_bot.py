import sqlite3
import os
from PIL    import Image, ImageDraw, ImageFont
from globals import *

if os.path.exists(BACK_IMAGE):
    files = os.listdir(BACK_IMAGE)
else:
    files = []

# Функция для получения неправильных глаголов из базы данных
def get_array_irregular_verbs():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM verbs")
        verbs = cursor.fetchall()
    finally:
        conn.close()
    return verbs

# Удаляем все карточки в папке py_bot/data/irregular_verbs_cards/
def delete_cards():
    for file_name in os.listdir(IMAGE_PATH):
        file_path = os.path.join(IMAGE_PATH, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

# Функция для создания карточек
def create_cards():
    background_color = (CB_R, CB_G, CB_B, C_ALPHA_CANAL)
    text_color = (T_R, T_G, T_B)
    last_word_color = (LW_R, LW_G, LW_B)

    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)

    use_background = bool(files)  # Проверяем, есть ли файлы для фона
    if use_background:
        try:
            first_file = files[0]  # Берем первый файл
            background = Image.open(os.path.join(BACK_IMAGE, first_file)).convert("RGBA")
        except IOError:
            raise ValueError(f"Фоновое изображение не найдено по пути {BACK_IMAGE}")

    verbs = get_array_irregular_verbs()  # Загружаем глаголы
    VERBS_COUNT = len(verbs)

    for verb in verbs:
        img = Image.new("RGBA" if use_background else "RGB", (800, 450), background_color)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(FONT, CARTS_TEXT_SIZE)
        except IOError:
            font = ImageFont.truetype("arial.ttf", CARTS_TEXT_SIZE)

        padding = 25
        x_start = 800 // 2
        y_start = 0
        offset_y = (450 - 50) // 4

        indx = verb[0]
        for i in range(1, len(verb)):
            text = verb[i].capitalize()
            y_line = y_start + ((i - 1) * offset_y) + padding
            x_line = x_start - (len(verb[i]) // 2) * 18
            draw.text((x_line, y_line), text, font=font, fill=last_word_color if i == (len(verb) - 1) else text_color)

        file_path = os.path.join(IMAGE_PATH, f"{indx}.png")

        if use_background:
            img = Image.alpha_composite(background, img)

        img.save(file_path)
        file_path = os.path.join(IMAGE_PATH, f"{indx}.png")
        img.save(file_path, "PNG")

def create_irregular_verbs_table():
    background_color  = (TB_R, TB_G, TB_B, T_ALPHA_CANAL)
    text_color        = (0, 0, 0)
    last_word_color   = (LW_R, LW_G, LW_B)
    grid_color        = (100, 100, 100)

    header_text_color = (TH_R, TH_G, TH_B)

    verbs = get_array_irregular_verbs()

    cols  = 4
    rows  = ROW + 1

    cell_width  = TABLE_WIDTH // 4
    cell_height = TABLE_HEIGHT // rows

    indx = 1
    for i in range(0, len(verbs), rows - 1):
        img  = Image.new("RGB", (TABLE_WIDTH, TABLE_HEIGHT), background_color)
        draw = ImageDraw.Draw(img)

        try:
            text_font   = ImageFont.truetype(FONT, TABLE_TEXT_SIZE)
            header_font = ImageFont.truetype(FONT, TABLE_HEADER_TEXT_SIZE)
        except IOError:
            text_font   = ImageFont.truetype("arial.ttf", TABLE_TEXT_SIZE)
            header_font = ImageFont.truetype("arial.ttf", TABLE_HEADER_TEXT_SIZE)

        for row in range(rows + 1):
            y = row * cell_height
            draw.line([(0, y), (TABLE_WIDTH, y)], fill=grid_color, width=2)

        for col in range(cols + 1):
            x = col * cell_width
            draw.line([(x, 0), (x, TABLE_HEIGHT)], fill=grid_color, width=2)

        header = ["Present Simple", "Past Simple", "Past Participle", "Translation"]

        offset_y = 0
        for j in range(0, len(header)):
            word = header[j]
            x = 20 + j * cell_width
            y = 20 + offset_y
            draw.text((x, y), word, font=header_font, fill=header_text_color)

        offset_y += cell_height
        for j in range(i, i + rows):
            if j == len(verbs):
                break
            offset_x = 0
            for k in range(1, cols + 1):
                text = verbs[j][k].capitalize()
                x = 20 + offset_x
                y = 20 + offset_y
                if k == cols:
                    draw.text((x, y), text, font=text_font, fill=last_word_color)
                else:
                    draw.text((x, y), text, font=text_font, fill=text_color)
                offset_x += cell_width
            offset_y += cell_height

        file_path = os.path.join(IMAGE_PATH, f"table_{indx}.png")
        img.save(file_path)
        indx += 1
        print(f"Изображение таблицы сохранено в {file_path}\n")

def main():
    delete_cards()
    print("Карточки с неправильными глаголами были удаленны!\n\n")
    create_cards()
    print("Карточки с неправильными глаголами были созданы!\n\n")
    create_irregular_verbs_table()
    print("Таблица с неправильными глаголами была создана!\n\n")

if __name__ == "__main__":
    main()
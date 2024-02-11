from PIL import Image, ImageDraw, ImageFont
from remove import remove_background
from tinydb import TinyDB, Query, where
import json
import os
import unidecode
from video_maker import audio_maker, video_maker

SILENCE = 'sound_effect/silence.mp3'
PATH = 'C:/Users/yanis/Desktop/git/flashcards-maker/flashcards/'


# Liste des fichiers dans le dossier
folder_list = os.listdir(PATH)


# Liste des fichiers .png
png_file = [file for file in folder_list if file.endswith(".png")]


FRENCH_FONT = ImageFont.truetype(
    'fonts/noto_sans_french_medium.ttf', size=46, encoding='utf-8',)
FRENCH_BOLD_FONT = ImageFont.truetype(
    'fonts/noto_sans_french_bold.ttf', size=50, encoding='utf-8')
JAPANESE_FONT = ImageFont.truetype(
    'fonts/noto_sans_japanese_bold.ttf', size=60, encoding='utf-8')
ARABIC_FONT = ImageFont.truetype(
    'fonts/noto_sans_arabic_medium.ttf', size=46, encoding='utf-8')
KOREAN_FONT = ImageFont.truetype(
    'fonts/noto_sans_korean_bold.ttf', size=60, encoding='utf-8')

CHINESE_FONT = ImageFont.truetype(
    'fonts/noto_sans_chinese_bold.ttf', size=60, encoding='utf-8')


db = TinyDB('db.json', encoding='utf-8')
json_files = {
    "chinese": "chinese.json",
    "japanese": "japanese.json",
    "korean": "korean.json"
}
# Fonction pour charger les données depuis un fichier JSON et les insérer dans la base de données

TEMPLATES = ['templates/japanese_template.png','templates/chinese_template.png',
             'templates/korean_template.png']


def load_data_to_db(json_file, table_name, db):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    table = db.table(table_name)
    table.insert_multiple(data[table_name])


def make_image(image_path, icon_path):

    background = Image.open(image_path)

    cropped_icon = remove_background(icon_path)

    if icon_path == 'flashcards/2024-01-15/football.png':
        cropped_icon.thumbnail(
            (cropped_icon.width // 1.2, cropped_icon.height // 1.2))
        x_translated = (background.width - cropped_icon.width) // 2
        position = (x_translated-13, 1350)

    else:
        cropped_icon.thumbnail(
            (cropped_icon.width // 1.9, cropped_icon.height // 1.9))
        x_translated = (background.width - cropped_icon.width) // 2
        position = (x_translated, 1350)

    background.paste(cropped_icon, position, cropped_icon)

    return background


def image_center(image):
    xc_image = image.width / 2
    yc_image = image.height / 2
    return xc_image, yc_image


def text_dimension(text, half, font):
    draw = ImageDraw.Draw(image)
    # On créé la plus petite boite entourant le text mais pas au bon endroit car on souhaite juste récuperer la hauteur du texte
    bbox = draw.textbbox((0, 0), text=text, font=FRENCH_FONT)
    width_word = draw.textlength(text, font=font)
    height_word = bbox[3] - bbox[1]

    if half == True:
        return width_word/2, height_word
    else:
        return width_word, height_word


def translation(xc_image, yc_image, half_width, half_height):
    x_translated = xc_image - half_width
    y_translated = yc_image - half_height
    return x_translated, y_translated


def make_transcription(word):
    xc_image, yc_image = image_center(image)
    half_width, half_height = text_dimension(
        word, half=True, font=FRENCH_BOLD_FONT)
    x_translated, y_translated = translation(
        xc_image, yc_image, half_width, half_height)

    draw.text((x_translated, y_translated+160),
              word, font=FRENCH_BOLD_FONT, fill=(0, 0, 0))


def make_french_word(word):
    xc_image, yc_image = image_center(image)
    half_width, half_height = text_dimension(word, half=True, font=FRENCH_FONT)
    x_translated, y_translated = translation(
        xc_image, yc_image, half_width, half_height)

    draw.text((x_translated-255, y_translated-172),
              word, font=FRENCH_FONT, fill=(0, 0, 0))


def make_asian_word(word, font):
    xc_image, yc_image = image_center(image)
    half_width, half_height = text_dimension(
        word, half=True, font=font)
    x_translated, y_translated = translation(
        xc_image, yc_image, half_width, half_height)

    draw.text((x_translated, y_translated+50),
              word, font=font, fill=(0, 0, 0))


def make_arabic_word(word):
    xc_image, yc_image = image_center(image)
    half_width, half_height = text_dimension(word, half=True, font=ARABIC_FONT)
    x_translated, y_translated = translation(
        xc_image, yc_image, half_width, half_height)

    draw.text((x_translated+255, y_translated-196),
              word, font=ARABIC_FONT, fill=(0, 0, 0))


japanese_table = db.table('japanese')
chinese_table = db.table('chinese')
korean_table = db.table('korean')

table = Query()


for template in TEMPLATES:

    if template == 'templates/chinese_template.png':
        for folder_name in folder_list:
            results = chinese_table.get(where('date') == folder_name)
            lang = "zh"
            folder = f'{PATH}/{folder_name}'
            png = os.listdir(folder)
            image = make_image(
                template, f"{PATH}/{folder_name}/{unidecode.unidecode(results['français']).lower()+'.png'}")
            draw = ImageDraw.Draw(image)
            width, height = image.size
            arabic_value = results['arabe']
            french_value = results['français']
            chinese_value = results['chinois']
            transcription_value = results['transcription']
            make_french_word(french_value)
            make_arabic_word(arabic_value)
            make_asian_word(chinese_value, CHINESE_FONT)
            make_transcription(transcription_value)

            image.save(
                f'{PATH}{folder_name}/2-{unidecode.unidecode(french_value.lower())}_chinese.png')
            print(f'{french_value.lower()} Crée chinois')

            audio_maker(chinese_value, "zh", f'{PATH}{folder_name}')
            video_maker(f'{PATH}{folder_name}/2-{unidecode.unidecode(french_value.lower())}_chinese.png',
                        f'{PATH}{folder_name}/zh.mp3', f'{PATH}{folder_name}/video_ch.mp4')
    elif template == 'templates/japanese_template.png':
        for folder_name in folder_list:
            results = japanese_table.get(where('date') == folder_name)

            folder = f'{PATH}/{folder_name}'
            png = os.listdir(folder)
            image = make_image(
                template, f"{PATH}/{folder_name}/{unidecode.unidecode(results['français']).lower()+'.png'}")
            draw = ImageDraw.Draw(image)
            width, height = image.size
            arabic_value = results['arabe']
            french_value = results['français']
            japanese_value = results['japonais']
            date = results['date']
            transcription_value = results['transcription']
            make_french_word(french_value)
            make_arabic_word(arabic_value)
            make_asian_word(japanese_value, JAPANESE_FONT)
            make_transcription(transcription_value)

            image.save(
                f'{PATH}{folder_name}/1-{unidecode.unidecode(french_value.lower())}_japanese.png')
            print(f'{french_value.lower()} Crée japonais')
            audio_maker(japanese_value, "ja", f'{PATH}{folder_name}')
            video_maker(f'{PATH}{folder_name}/1-{unidecode.unidecode(french_value.lower())}_japanese.png',
                        f'{PATH}{folder_name}/ja.mp3', f'{PATH}{folder_name}/video_jp.mp4')

    elif template == 'templates/korean_template.png':
        for folder_name in folder_list:
            results = korean_table.get(where('date') == folder_name)
            folder = f'{PATH}/{folder_name}'
            png = os.listdir(folder)
            lang = "ko"
            image = make_image(
                template, f"{PATH}/{folder_name}/{unidecode.unidecode(results['français']).lower()+'.png'}")
            draw = ImageDraw.Draw(image)
            width, height = image.size
            arabic_value = results['arabe']
            french_value = results['français']
            korean_value = results['coreen']
            transcription_value = results['transcription']
            make_french_word(french_value)
            make_arabic_word(arabic_value)
            make_asian_word(korean_value, KOREAN_FONT)
            make_transcription(transcription_value)
            image.save(
                f'{PATH}{folder_name}/3-{unidecode.unidecode(french_value.lower())}_korean.png')

            audio_maker(korean_value, "ko", f'{PATH}{folder_name}')
            video_maker(f'{PATH}{folder_name}/3-{unidecode.unidecode(french_value.lower())}_korean.png',
                        f'{PATH}{folder_name}/ko.mp3', f'{PATH}{folder_name}/video_cor.mp4')

            print(f'{french_value.lower()} Crée coréen')


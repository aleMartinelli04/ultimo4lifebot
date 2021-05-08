import io
import os
from PIL import Image, ImageEnhance
from random import randint
import random
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

PREFIXES = ["Ultimo ", "ultimo "]

KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Color", callback_data="color"),
        InlineKeyboardButton("Contrast", callback_data="contrast")
    ],
    [
        InlineKeyboardButton("Brightness", callback_data="brightness"),
        InlineKeyboardButton("Sharpness", callback_data="sharpness")
    ],
    [
        InlineKeyboardButton("End", callback_data="end")
    ]
])


@Client.on_message(filters.command("editor", prefixes=PREFIXES))
async def on_editor(client, message):
    if message.from_user.id != 511831945:
        await message.reply_text("No")
        return

    global filepath
    try:
        if message.reply_to_message:
            filepath = await message.reply_to_message.download()

        else:
            user = await client.get_users(message.command[1])
            file_id = user.photo.big_file_id
            filepath = await client.download_media(file_id)

        image = Image.open(filepath)

        byte_arr = io.BytesIO()
        image.save(byte_arr, format='jpeg')
        byte_arr.name = 'edited<3.jpeg'

        await message.reply_photo(byte_arr, reply_markup=KEYBOARD)
        os.remove(filepath)

    except IndexError:
        await message.reply_text("Rispondi a una foto per editarla o tagga qualcuno per aprire l'editor con la sua pic")

    except ValueError:
        await message.reply_text("Il messaggio a cui hai risposto non contiene nessun media")

    except AttributeError:
        await message.reply_text("L'utente taggato non ha una pic")

    except OSError:
        await message.reply_text("Immagine in un formato non supportato")
        os.remove(filepath)


@Client.on_callback_query(filters.regex("^color$"))
async def color(_, callback):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(emoji.MINUS, callback_data="color_minus"),
            InlineKeyboardButton(emoji.PLUS, callback_data="color_plus")
        ],
        [InlineKeyboardButton(emoji.BACK_ARROW + " indietro", callback_data="back")]
    ])
    await callback.edit_message_reply_markup(keyboard)


@Client.on_callback_query(filters.regex("^color_minus$"))
async def color_minus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Color(image).enhance(-2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^color_plus$"))
async def color_plus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Color(image).enhance(2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^contrast$"))
async def contrast(_, callback):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(emoji.MINUS, callback_data="contrast_minus"),
            InlineKeyboardButton(emoji.PLUS, callback_data="contrast_plus")
        ],
        [InlineKeyboardButton(emoji.BACK_ARROW + " indietro", callback_data="back")]
    ])
    await callback.edit_message_reply_markup(keyboard)


@Client.on_callback_query(filters.regex("^contrast_minus$"))
async def contrast_minus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Contrast(image).enhance(-2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^contrast_plus$"))
async def contrast_plus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Contrast(image).enhance(2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^brightness$"))
async def bright(_, callback):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(emoji.MINUS, callback_data="contrast_minus"),
            InlineKeyboardButton(emoji.PLUS, callback_data="contrast_plus")
        ],
        [InlineKeyboardButton(emoji.BACK_ARROW + " indietro", callback_data="back")]
    ])
    await callback.edit_message_reply_markup(keyboard)


@Client.on_callback_query(filters.regex("^bright_minus$"))
async def bright_minus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Brightness(image).enhance(-2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^bright_plus$"))
async def bright_plus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Brightness(image).enhance(2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^sharpness$"))
async def sharp(_, callback):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(emoji.MINUS, callback_data="contrast_minus"),
            InlineKeyboardButton(emoji.PLUS, callback_data="contrast_plus")
        ],
        [InlineKeyboardButton(emoji.BACK_ARROW + " indietro", callback_data="back")]
    ])
    await callback.edit_message_reply_markup(keyboard)


@Client.on_callback_query(filters.regex("^sharp_minus$"))
async def sharp_minus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Sharpness(image).enhance(-2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^sharp_plus$"))
async def sharp_plus(_, callback):
    await callback.edit_message_reply_markup("")
    file_path = await callback.message.download()
    image = Image.open(file_path)
    image = ImageEnhance.Sharpness(image).enhance(2)
    image.save(file_path)
    await callback.edit_message_media(media=InputMediaPhoto(file_path), reply_markup=KEYBOARD)
    os.remove(file_path)


@Client.on_callback_query(filters.regex("^back$"))
async def back(_, callback):
    await callback.edit_message_reply_markup(KEYBOARD)


@Client.on_callback_query(filters.regex("^end$"))
async def end(_, callback):
    await callback.edit_message_reply_markup("")


@Client.on_message(filters.command("jpeg", prefixes=PREFIXES))
async def on_jpeg(_, message):
    file_path = ""
    try:
        try:
            i = int(message.command[1])
            if i > 100:
                i = 100
        except IndexError:
            i = 1

        file_path = await message.reply_to_message.download()
        image = Image.open(file_path)

        for x in range(i):
            image = await jpeg_effect(image)

        byte_arr = io.BytesIO()
        image.save(byte_arr, format='jpeg')
        byte_arr.name = 'jpegged.jpeg'

        await message.reply_photo(byte_arr, reply_to_message_id=message.reply_to_message.message_id)
        os.remove(file_path)
    except Exception as e:
        await message.reply_text("C'è stato questo errore:\n<code>" + str(e) + "</code>")
        os.remove(file_path)


@Client.on_message(filters.command("jpegga", prefixes=PREFIXES))
async def on_jpeg_random(client, message):
    try:
        i = int(message.command[1])
        if i > 100:
            i = 100

        user = await client.get_users(message.command[2])

    except ValueError:
        i = 1

        user = await client.get_users(message.command[1])

    except IndexError:
        await message.reply_text("Tagga anche un utente")
        return

    try:
        file_id = user.photo.big_file_id
    except AttributeError:
        await message.reply_text("L'utente taggato non ha una pic")
        return

    file_path = await client.download_media(file_id)

    image = Image.open(file_path)

    byte_arr = io.BytesIO()

    for x in range(i):
        image = await jpeg_effect(image)

    image.save(byte_arr, format='jpeg')

    byte_arr.name = 'loll.jpeg'
    await message.reply_photo(byte_arr)
    os.remove(file_path)


async def jpeg_effect(image):
    level = random.uniform(0.1, 10)
    rand = randint(1, 4)

    if rand == 1:
        image = ImageEnhance.Color(image).enhance(level)
    elif rand == 2:
        image = ImageEnhance.Contrast(image).enhance(level)
    elif rand == 3:
        image = ImageEnhance.Brightness(image).enhance(level)
    elif rand == 4:
        image = ImageEnhance.Sharpness(image).enhance(level)
    return image

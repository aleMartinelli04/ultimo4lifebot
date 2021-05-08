from random import randint
from pyrogram import Client, filters, emoji
import requests

import config

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("gatto", prefixes=PREFIXES))
async def on_cat_api(_, message):
    message = message.reply_to_message or message

    r = requests.get('https://api.thecatapi.com/v1/images/search')

    cat = r.json()[0]["url"]

    try:
        await message.reply_photo(cat)
    except AttributeError:
        await message.reply_animation(cat)


@Client.on_message(filters.command("tenor", prefixes=PREFIXES))
async def on_tenor_gif(_, message):
    api_key = config.api_key
    limit = 10
    gif_to_search = ' '.join(message.command[1:])

    message = message.reply_to_message or message

    if gif_to_search == "":
        await message.reply_text("Che gif devo cercare?")
        return

    params = {"q": gif_to_search, "key": api_key, "limit": limit}

    r = requests.get("https://api.tenor.com/v1/search", params=params)

    if r.status_code == 200:
        try:
            url = r.json()["results"][randint(0, limit-1)]["url"]
            await message.reply_animation(url)
        except IndexError or KeyError:
            await message.reply_text(f"Nessuna gif trovata {emoji.FACE_WITH_MONOCLE}")

    else:
        await message.reply_text("Error 200: status_code")

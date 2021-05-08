import random
import requests
from pyrogram import Client, filters

import config
from plugins.superheroes import create_keyboard

PREFIXES = ["Ultimo ", "ultimo "]

image_not_found = "AgADBAADEbUxG5kUmVDI_s4Nf6bNrPuVfSddAAMBAAMCAANtAAP7iwQAARYE"

url = "https://imdb8.p.rapidapi.com/title/auto-complete"

headers = config.headers


@Client.on_callback_query(filters.regex("^imdb_"))
async def on_selected_movie(_, callback):
    movie_id = callback.data.split('_')[1]

    querystring = {"q": movie_id}

    data = requests.request("GET", url, headers=headers, params=querystring).json()["d"][0]

    try:
        img = data["i"]["imageUrl"]
    except KeyError:
        img = image_not_found

    error_string = "info non disponibile"
    try:
        name = data["l"]
    except KeyError:
        name = error_string
    try:
        series = data["q"]
    except KeyError:
        series = error_string
    try:
        actors = data["s"]
    except KeyError:
        actors = error_string
    try:
        years = data["yr"]
    except KeyError:
        years = error_string

    await callback.message.delete()

    await callback.message.reply_photo(img, caption=f"<b>Dettagli per</b>:\t{name}\n"
                                                    f"<b>Tipo</b>:\t{series}\n"
                                                    f"<b>Attori</b>:\t{actors}\n"
                                                    f"<b>Anno di produzione</b>:\t{years}")


@Client.on_message(filters.command("IMDb", prefixes=PREFIXES))
async def on_imd(_, message):
    film = ' '.join(message.command[1:])

    if film == "":
        await message.reply_text("Specifica il film o la serie tv")
        return

    querystring = {"q": film}

    r = requests.request("GET", url, headers=headers, params=querystring)

    try:
        data = r.json()["d"]
    except KeyError:
        await message.reply_text("Errore\nProva con altre parole chiave")
        return

    if len(data) > 1:
        film_infos = [[data[x]["id"], data[x]["l"]] for x in range(len(data))]

        if len(film_infos) > 20:
            reply = random.choice(["Seriamente?", "Usa più lettere la prossima volta"])
            await message.reply_text(reply)
            return

        keyboard = await create_keyboard(all_data=film_infos, callback_name="imdb", buttons_per_row=2)

        await message.reply_text("Film trovati: ", reply_markup=keyboard)
        return

    try:
        img = data["i"]["imageUrl"]
    except KeyError:
        img = image_not_found

    error_string = "info non disponibile"
    try:
        name = data["l"]
    except KeyError:
        name = error_string
    try:
        series = data["q"]
    except KeyError:
        series = error_string
    try:
        actors = data["s"]
    except KeyError:
        actors = error_string
    try:
        years = data["yr"]
    except KeyError:
        years = error_string

    await message.reply_photo(img,
                              caption=f"<b>Dettagli per</b>:\t{name}\n"
                                      f"<b>Tipo</b>:\t{series}\n"
                                      f"<b>Attori</b>:\t{actors}\n"
                                      f"<b>Anno di produzione</b>:\t{years}")

import random
import requests
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config

PREFIXES = ["Ultimo ", "ultimo "]

BACK_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(f"Indietro {emoji.BACK_ARROW}", callback_data="back_supdb")
    ]
])

KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(f"Biografia {emoji.CALENDAR}", callback_data="biography"),
        InlineKeyboardButton(f"Stats {emoji.FLEXED_BICEPS_LIGHT_SKIN_TONE}", callback_data="power_stats")
    ],
    [
        InlineKeyboardButton(f"Aspetto {emoji.MAN_WALKING_LIGHT_SKIN_TONE}", callback_data="appearance"),
        InlineKeyboardButton(f"Work {emoji.BAR_CHART}", callback_data="work")
    ],
    [
        InlineKeyboardButton(f"Collegamenti {emoji.LINK}", callback_data="connections"),
        InlineKeyboardButton(f"Altre info {emoji.ROUND_PUSHPIN}", callback_data="other_infos")
    ],
    [
        InlineKeyboardButton(f"Fine {emoji.STOP_BUTTON}", callback_data="end_supdb")
    ]
])

link = f"https://superheroapi.com/api/{config.id}/"

image_not_found = "AgADBAADEbUxG5kUmVDI_s4Nf6bNrPuVfSddAAMBAAMCAANtAAP7iwQAARYE"


async def create_keyboard(all_data, callback_name, buttons_per_row):
    keyboard = [
        []
    ]

    line = 0

    for data in all_data:
        single_id = data[0]
        single_name = data[1]

        button = InlineKeyboardButton(single_name, callback_data=f"{callback_name}_{single_id}")

        if len(keyboard[line]) == buttons_per_row:
            line += 1
            keyboard.append([])

        keyboard[line].append(button)

    keyboard = InlineKeyboardMarkup(keyboard)

    return keyboard


@Client.on_callback_query(filters.regex(f"^supdb_"))
async def on_selected_character(_, callback):
    char_id = int(callback.data.split('_')[1])

    data = requests.get(f"{link}/{char_id}").json()

    image = data["image"]["url"]

    pg_id = data["id"]
    pg_name = data["name"]

    description = f"<b>{pg_name}</b>\n\nId: {pg_id}"

    await callback.message.delete()

    try:
        await callback.message.reply_photo(image, caption=description, reply_markup=KEYBOARD)
    except:
        await callback.message.reply_photo(image_not_found, caption=description, reply_markup=KEYBOARD)


@Client.on_message(filters.command(["supereroe", "superheroes", "supdb"], prefixes=PREFIXES))
async def on_sup_db(_, message):
    hero = ' '.join(message.command[1:])

    if hero == "":
        await message.reply_text("Specifica un supereroe o un supercattivo")
        return

    r = requests.get(f"{link}search/{hero}")

    if r.json()["response"] == "error":
        await message.reply_text(f"{hero} non è stato trovato")
        return

    data = r.json()["results"]

    if len(data) > 1:
        char_infos = [[data[x]["id"], data[x]["name"]] for x in range(len(data))]

        if len(char_infos) > 20:
            reply = random.choice(["Seriamente?", "Usa più lettere la prossima volta"])
            await message.reply_text(reply)
            return

        keyboard = await create_keyboard(all_data=char_infos, callback_name="supdb", buttons_per_row=3)

        await message.reply_text("Personaggi trovati: ", reply_markup=keyboard)
        return

    data = data[0]

    image = data["image"]["url"]

    pg_id = data["id"]
    pg_name = data["name"]

    description = f"<b>{pg_name}</b>\n\nId: {pg_id}"

    try:
        await message.reply_photo(photo=image, caption=description, reply_markup=KEYBOARD)
    except:
        await message.reply_photo(image_not_found, caption=description, reply_markup=KEYBOARD)


@Client.on_callback_query(filters.regex("^biography$"))
async def on_biography_sup_db(_, callback):
    hero_id = callback.message.caption.split("\n\n")[1].split(": ")[1]

    data = requests.get(f"{link}/{hero_id}").json()["biography"]

    name = data["full-name"]
    alter_egos = data["alter-egos"]
    aliases = ', '.join(data["aliases"][:3])
    birth_place = data["place-of-birth"]
    appearance = data["first-appearance"]
    publisher = data["publisher"]
    alignment = data["alignment"]

    response = f"Vero nome: {name}\n" \
               f"Alter ego: {alter_egos}\n" \
               f"Soprannomi: {aliases}\n" \
               f"Luogo di nascita: {birth_place}\n" \
               f"Prima apparizione: {appearance}\n" \
               f"Pubblicatore: {publisher}\n" \
               f"Allineamento: {alignment}"

    await callback.edit_message_caption(f"{callback.message.caption}\n\n{response}")
    await callback.edit_message_reply_markup(BACK_KEYBOARD)


@Client.on_callback_query(filters.regex("^power_stats$"))
async def on_power_stats_sup_db(_, callback):
    hero_id = callback.message.caption.split("\n\n")[1].split(": ")[1]

    data = requests.get(f"{link}/{hero_id}").json()["powerstats"]

    response = '\n'.join(f"{key}: {value}" for key, value in data.items())

    await callback.edit_message_caption(f"{callback.message.caption}\n\n{response}")
    await callback.edit_message_reply_markup(BACK_KEYBOARD)


@Client.on_callback_query(filters.regex("^appearance$"))
async def on_appearance_sup_db(_, callback):
    hero_id = callback.message.caption.split("\n\n")[1].split(": ")[1]

    data = requests.get(f"{link}/{hero_id}").json()["appearance"]

    gender = data["gender"]
    race = data["race"]
    height = data["height"][1]
    weight = data["weight"][1]
    eyes = data["eye-color"]
    hair = data["hair-color"]

    response = f"Genere: {gender}\n" \
               f"Razza: {race}\n" \
               f"Altezza: {height}\n" \
               f"Peso: {weight}\n" \
               f"Colore degli occhi: {eyes}\n" \
               f"Colore dei capelli: {hair}"

    await callback.edit_message_caption(f"{callback.message.caption}\n\n{response}")
    await callback.edit_message_reply_markup(BACK_KEYBOARD)


@Client.on_callback_query(filters.regex("^work$"))
async def on_work_sup_db(_, callback):
    hero_id = callback.message.caption.split("\n\n")[1].split(": ")[1]

    data = requests.get(f"{link}/{hero_id}").json()["work"]

    occupation = data["occupation"]
    base = '; '.join(data["base"].split('; ')[:2])

    response = f"Lavoro: {occupation}\n" \
               f"Base: {base}"

    await callback.edit_message_caption(f"{callback.message.caption}\n\n{response}")
    await callback.edit_message_reply_markup(BACK_KEYBOARD)


@Client.on_callback_query(filters.regex("^connections$"))
async def on_connections_sup_db(_, callback):
    hero_id = callback.message.caption.split("\n\n")[1].split(": ")[1]

    data = requests.get(f"{link}/{hero_id}").json()["connections"]

    group_affiliation = '; '.join(data["group-affiliation"].split('; ')[:2])
    relatives = '; '.join(data["relatives"].split('; ')[:3])

    response = f"Gruppi e squadre: {group_affiliation}\n" \
               f"Parenti: {relatives}"

    await callback.edit_message_caption(f"{callback.message.caption}\n\n{response}")
    await callback.edit_message_reply_markup(BACK_KEYBOARD)


@Client.on_callback_query(filters.regex("^other_infos$"))
async def on_other_infos_sup_db(_, callback):
    hero_id = callback.message.caption.split("\n\n")[1].split(": ")[1]

    data = requests.get(f"{link}/{hero_id}")

    img_url = data.json()["image"]["url"]

    credit = "superheroapi.com"

    response = f"Puoi trovare l'immagine al seguente url:\n{img_url}\n\n" \
               f"Fonte: {credit}"

    await callback.edit_message_caption(f"{callback.message.caption}\n\n{response}")
    await callback.edit_message_reply_markup(BACK_KEYBOARD)


@Client.on_callback_query(filters.regex("^back_supdb$"))
async def on_back_sup_db(_, callback):
    text = '\n\n'.join(callback.message.caption.split("\n\n")[:2])

    await callback.edit_message_caption(text)
    await callback.edit_message_reply_markup(KEYBOARD)


@Client.on_callback_query(filters.regex("^end_supdb$"))
async def on_end_sup_db(_, callback):
    hero = callback.message.caption.split("\n\n")[0]

    await callback.edit_message_caption(hero)

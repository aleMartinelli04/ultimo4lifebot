import io
import sys
from _datetime import datetime
from pyrogram import Client, filters, emoji
import string
import json

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("aiuto", prefixes=PREFIXES) | filters.command("start"))
async def on_help(_, message):
    commands = [
        "ciao", "ti spengo", "dimmi qualcosa di te",

        "aiuto", "ora e data", "id messaggio", "id", "calcola", "esegui", "auguri",

        "elimina", "fissa", "unpinna", "rinomina @usr", "promuovi @usr", "retrocedi @usr",

        "editor @usr", "jpeg", "jpegga @usr",

        "canzone", "numero casuale", "cringeometro", "bugia", "scegli", "prevedi",
        "domanda", "cosa ne pensi di @usr",

        "canta come @Fumaz", "di", "uccidi @usr", "A VICENSA", "aiscoffi", "reversa", "elefanti", "codifica",
        "spelling",

        "IMDb", "tenor", "gatto", "supDB"
    ]

    with open("data.json", "r") as x:
        data = json.load(x)

    for key in data.keys():
        commands.append(key)

    reply = ""

    for thing in commands:
        reply += f"\n» <code>{thing}</code>"

    await message.reply_text(f"Ciao, per ora posso fare:\n{reply}\n\nAttualmente ho {len(commands)} comandi!")


@Client.on_message(filters.regex("^Ultimo$") | filters.regex("^ultimo$"))
async def on_main(_, message):
    await message.reply_text("Hey ciao, sono Ultimo")


@Client.on_message(filters.command(["ora e data", "data e ora"], prefixes=PREFIXES))
async def on_date_time(client, message):
    await on_time(client, message)
    await on_date(client, message)


@Client.on_message(filters.command("ora", prefixes=PREFIXES))
async def on_time(_, message):
    await message.reply_text(f"{emoji.THREE_O_CLOCK} Ora attuale: "
                             f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")


@Client.on_message(filters.command("data", prefixes=PREFIXES))
async def on_date(_, message):
    await message.reply_text(
        f"{emoji.CALENDAR} Data attuale: {datetime.now().day}/{datetime.now().month}/{datetime.now().year}")


@Client.on_message(filters.command("id messaggio", prefixes=PREFIXES))
async def on_message_id(_, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id

        await message.reply_to_message.reply_text(f"Id del messaggio: <code>{message_id}</code>")
        return

    await message.reply_text("Rispondi a un messaggio per sapere l'id")


@Client.on_message(filters.command("id", prefixes=PREFIXES))
async def on_id(_, message):
    try:
        media = message.reply_to_message.animation or \
                message.reply_to_message.sticker or \
                message.reply_to_message.photo

        file_id = media.file_id
        await message.reply_text(f"<code>{file_id}</code>")

    except AttributeError:
        await message.reply_text("Rispondi a una gif, a uno sticker o a un'immagine per sapere l'ID")


@Client.on_message(filters.command("calcola", prefixes=PREFIXES))
async def on_calculate(_, message):
    if ''.join(message.command[1:]) == '7+3':
        await message.reply_audio("CQADBAADEAgAArdhqFIAAdUM_iczH2oWBA")
        return

    if message.from_user.id == 306980878:
        await message.reply_text("No")
        return

    allowed = string.digits + string.punctuation
    expr = ''.join(message.command[1:])

    if expr == "":
        await message.reply_text("Dimmi cosa devo calcolare")
        return

    for char in expr:
        if char not in allowed:
            await message.reply_text("Non posso calcolare questa cosa")
            return

    calc = eval(expr)
    await message.reply_text(
        f"{emoji.ORANGE_BOOK}  Espressione: \n<code>{expr}</code>\n"
        f"{emoji.OPEN_BOOK} Risultato:\n<code>{str(calc)}</code>")


# noinspection PyUnusedLocal
@Client.on_message(filters.command("esegui", prefixes=PREFIXES))
def on_exec(client, message):
    user_id = message.from_user.id

    if user_id == 511831945:
        expression = message.text[len('ultimo esegui '):]

        old_stdout = sys.stdout
        redirected = sys.stdout = io.StringIO()

        try:
            exec(expression)

            sys.stdout = old_stdout
            output = redirected.getvalue() or None

        except Exception as e:
            output = str(e)

        message.reply_text(
            f"<b>Espressione:</b>\n<code>{expression}</code>\n\n<b>Output:</b>\n<code>{output}</code>")

    else:
        message.reply_text("Eseguo solo il codice di @nonvoglioluser")


@Client.on_message(filters.command("auguri", prefixes=PREFIXES))
async def on_birthday(_, message):
    try:
        birth = message.command[1]

        if int(message.command[2]) <= 0:
            await message.reply_text("Anni inseriti non validi:\n<code> " + message.command[2] + " <= 0 ")

        else:
            age = message.command[2]
            for x in range(1, 3):
                await message.reply_text("Tanti auguri a te")
            await message.reply_text(f"Tanti auguri a {birth}")
            await message.reply_text("Tanti auguri a te!")
            await message.reply_text(
                f"Oggi, {datetime.now().day} {await what_month()} {datetime.now().year}, compi {age} anni!")

    except IndexError:
        await message.reply_text("C'è stato un errore. Scrivi ad esempio:"
                                 "<code> Ultimo auguri 'festeggiato' 'anni' </code>")


async def what_month():
    month = {
        1: " gennaio ",
        2: " febbraio ",
        3: " marzo ",
        4: " aprile ",
        5: " maggio ",
        6: " giugno ",
        7: " luglio ",
        8: " agosto ",
        9: " settembre ",
        10: " ottobre ",
        11: " novembre ",
        12: " dicembre "
    }
    month_key = datetime.now().month
    return month.get(month_key)


@Client.on_message(filters.command("chiama", prefixes=PREFIXES))
async def on_call(_, message):
    if message.from_user.id == 306980878:
        await message.reply_text("Hey @Fumaz non lo faccio per te")
        return

    try:
        usr = message.command[1]
    except IndexError:
        await message.reply_text("Chi devo chiamare?")
        return

    try:
        n_times = int(message.command[2])
        if n_times <= 0:
            raise Exception
    except:
        n_times = 5

    for x in range(n_times):
        await message.reply_text(usr)

import random
from random import randint
from pyrogram import Client, filters, emoji

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command(["dimmi una canzone", "canzone", "song"], prefixes=PREFIXES))
async def on_song(_, message):
    phrases = ["Mi piacerebbe che tu ascoltassi ",
               "Vorrei che tu ascoltassi ",
               "Ascoltati ",
               "Una delle mie preferite è ",
               "Ti consiglio ",
               "Se vuoi emozionarti ascolta "]

    songs = {"7 + 3": "https://www.youtube.com/watch?v=t0EhTL660oU",
             "Rondini Al Guinzaglio": "https://www.youtube.com/watch?v=dIHWHuy0moY",
             "Pianeti": "https://www.youtube.com/watch?v=QdaO4l7a3c4",
             "Tutto Questo Sei Tu": "https://www.youtube.com/watch?v=iDinXwBsQDM",
             "I Tuoi Particolari": "https://www.youtube.com/watch?v=q2izsbwDEsk",
             "Cascare Nei Tuoi Occhi": "https://www.youtube.com/watch?v=BhKjcaWbJXQ",
             "Sogni Appesi": "https://www.youtube.com/watch?v=WI54tFj3lmw",
             "Ti Dedico Il Silenzio": "https://www.youtube.com/watch?v=fjcJuhlyzxM",
             "22 Settembre": "https://www.youtube.com/watch?v=xAvPkZ99Jfo",
             "Poesia Senza Veli": "https://www.youtube.com/watch?v=uKOR4-eOe_c",
             "Il Ballo Delle Incertezze": "https://www.youtube.com/watch?v=EyZir4O5pu4",
             "Poesia Per Roma": "https://www.youtube.com/watch?v=xeg8TkotMSQ",
             "Piccola Stella": "https://www.youtube.com/watch?v=WovUGbBlzqA",
             "Quando Fuori Piove": "https://www.youtube.com/watch?v=s3GePraYXc0",
             "Ipocondria": "https://www.youtube.com/watch?v=0YM1cs4mA8s",
             "Ovunque Tu Sia": "https://www.youtube.com/watch?v=WOOTF1Sy4jw",
             "Sabbia": "https://www.youtube.com/watch?v=thPjTBQQ5Hk",
             "Farfalla Bianca": "https://www.youtube.com/watch?v=t4Gn_neQ_mY",
             "L'Unica Forza che Ho": "https://www.youtube.com/watch?v=mcG7eow7UFc",
             "Fateme Cantà": "https://www.youtube.com/watch?v=B_QoSCiRvtY",
             "Giusy": "https://www.youtube.com/watch?v=hAemDovxVb8",
             "Stasera": "https://www.youtube.com/watch?v=rAMbVnwh5bM",
             "Chiave": "https://www.youtube.com/watch?v=ZRODlP_joWk&list=PLXQjjeN_leJ_aj4p3vzMfw-xyykHy_CCF&index=46"}
    song, link = random.choice(list(songs.items()))
    phrase = random.choice(phrases)
    await message.reply_text(phrase + song)
    await message.reply_text(link)


@Client.on_message(filters.command("numero casuale", prefixes=PREFIXES))
async def on_casual_number(_, message):
    try:
        init = int(message.command[2])
        final = int(message.command[4])

        if init > final:
            init, final = final, init

        rand = randint(init, final)
        await message.reply_text(f"Numero generato: {rand}")

    except IndexError:
        await message.reply_text("Non hai inserito il range di numeri da prendere in considerazione")

    except BaseException:
        await message.reply_text("Non hai inserito due numeri")


@Client.on_message(filters.command(["cringeometro", "cringe"], prefixes=PREFIXES))
async def on_cringe(_, message):
    level = str(randint(0, 100))

    if message.reply_to_message:
        await message.reply_to_message.reply_text(
            f"{emoji.AMBULANCE} Questo messaggio è cringe al{await what_letter(level)} <b>{level}%</b>")

    else:
        await message.reply_text("Rispondi a un messaggio per usare il cringeometro")


@Client.on_message(filters.command("bugia", prefixes=PREFIXES))
async def on_liar(_, message):
    level = str(randint(0, 100))

    if message.reply_to_message:
        await message.reply_text(
            f"{emoji.BABY_ANGEL} Questo messaggio è una bugia al{await what_letter(level)} <b>{level}%</b>")

    else:
        await message.reply_text("Rispondi a un messaggio per misurare la bugia")


async def what_letter(level):
    if level[0] == "8" or level == "1" or level == "11":
        return "l'"
    elif level == "0":
        return "lo "
    else:
        return " "


@Client.on_message(filters.command("scegli", prefixes=PREFIXES))
async def on_choose(_, message):
    try:
        times = int(message.command[1])
        options = message.command[2:]

    except BaseException:
        times = 1
        options = message.command[1:]

    options = ' '.join(options)
    options = options.split(' o ')

    choice = ""
    for x in range(times):
        if x not in [0, times]:
            choice += "</b>, <b>"
        choice += random.choice(options)

    if choice == "":
        await message.reply_text("Non hai inserito le scelte...")
        return

    await message.reply_text(f"Ho scelto <b>{choice}!</b>")


@Client.on_message(filters.command("prevedi", prefixes=PREFIXES))
async def on_preview(_, message):
    message = message.reply_to_message or message
    replies = ["di si", "di no", "che forse dovresti", "che devi fare quello che vuoi",
               "che devi andare contro la tua volontà", "che per stavolta non risponderò",
               "che tu sappia già la risposta", "che non ne avrai l'occasione", "di non sapere a cosa ti riferisci",
               "che tu mi stia chiedendo qualcosa di inutile", "che in ogni caso succederà qualcosa che per te va bene",
               "che dovresti stare tranquillo", "che ti andrà male in ogni caso", "che @Fumaz sia stupido :p"]

    await message.reply_text(f"Penso {random.choice(replies)}!")


@Client.on_message(filters.command("domanda", prefixes=PREFIXES))
async def on_question(_, message):
    message = message.reply_to_message or message
    replies = ["si", "no", "forse", "boh", "certamente", "ovvio", "per nulla", "assolutamente no", "non saprei"]
    await message.reply_text(random.choice(replies))


@Client.on_message(filters.command("cosa ne pensi", prefixes=PREFIXES))
async def on_think(_, message):
    try:
        user = message.command[2]
        await message.reply_text(f"Secondo me {user} è {await what_think(user)}")

    except IndexError:
        await message.reply_text("Mmh... cosa penso di nessuno? Niente")


async def what_think(user):
    if user in ["Nelli", "nelli", "@nonvoglioluser"]:
        return "il mio best fan"
    elif user in ["ultimo", "Ultimo", "@ultimo4lifebot"]:
        return "figo"
    else:
        replies = ["stronzo", "troio", "scemo", "brutto", "bello", "intelligente", "gentile", "simpatico"]
        return random.choice(replies)

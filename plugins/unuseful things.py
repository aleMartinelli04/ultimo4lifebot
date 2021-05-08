from time import sleep
from pyrogram import Client, filters, emoji
from pyrogram.errors import MessageEmpty

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("canta come @Fumaz", prefixes=PREFIXES))
async def on_sing(_, message):
    await message.reply_text("Ora canto come @Fumaz!")

    for x in range(5):
        await message.reply_text("AIAIAI IM YOUR LITTLE BUTTERFLY\n")


@Client.on_message(filters.command("di", prefixes=PREFIXES))
async def on_say(_, message):
    try:
        reply = ' '.join(message.command[1:])
        await message.reply_text(reply)

    except IndexError:
        await message.reply_text("Non hai inserito quello che devo dire...")


@Client.on_message(filters.command("uccidi", prefixes=PREFIXES))
async def on_kill(_, message):
    try:
        user = message.command[1]

        if user == "@nonvoglioluser":
            await message.reply_text("Non posso uccidere il mio fan")
        elif user == "@ultimo4lifebot":
            await message.reply_text("Sono contrario ai suicidi. Mi spiace ma non ti aiuto")
        else:
            await message.reply_text("Ok lo uccido volentieri ahah *IRONIA*")

    except IndexError:
        await message.reply_text("Chi devo uccidere?")


@Client.on_message(filters.command("A VICENSA", prefixes=PREFIXES))
async def on_vicenza(_, message):
    things_to_say = [
        "DI BELLO C'E'",
        "LE LUCII",
        "I SASSII",
        "BABBO NATAAALEEE",
        "EH PERO' NON SI PUO' ANDARE DA PADOVA A VICENSA",
        "E' LONTANO L'ISLANDA E'VICINO A PADOVA L'ISLANDA"
    ]

    for thing in things_to_say:
        await message.reply_text(thing)

    await message.reply_animation("CgADBAADFAIAAhQkjVIhhlIGhytn6RYE")


@Client.on_message(filters.command("aiscoffi", prefixes=PREFIXES))
async def on_coffee(_, message):
    await message.reply_text("E' solo caffè col ghiaccio")
    await message.reply_text("Te lo posso fare pure io senza che tu vada a Stairbucks")


@Client.on_message(filters.command("reversa", prefixes=PREFIXES))
async def on_reverse(_, message):
    try:
        reverse = message.reply_to_message.text if message.reply_to_message else ' '.join(message.command[1:])
        exchanged = reverse[::-1]

        if ("dio" and ("cane" or "porco")) in exchanged:
            await message.reply_text("Non reverso questo porcone!")
        else:
            await message.reply_text(exchanged)

    except MessageEmpty:
        await message.reply_text("Che cosa devo reversare?")

    except TypeError:
        await message.reply_to_message.reply_text("Non posso reversare questo...")


@Client.on_message(filters.command("elefanti", prefixes=PREFIXES))
async def on_elephants(_, message):
    try:
        n_times = int(message.command[1])

        if n_times < 0:
            await message.reply_text(f"Beh io non so contare {n_times} elefanti. Insegnamelo perfavore")
            return

        for x in reversed(range(1, n_times + 1)):
            await message.reply_text(
                f"{x} elefant{'i' if x != 1 else 'e'} saltava{'no' if x != 1 else ''} sul letto "
                f"{'uno ' if x != 1 else ''}cadde giù e si ruppe il cervelletto "
                f"la mamma chiama il dottore il dottore ha detto niente più elefanti che saltano sul letto")
        await message.reply_text("Niente più elefanti che saltano sul letto!")

    except IndexError:
        await message.reply_text(
            "Non posso contare gli elefanti se non mi dici quante contarne " + emoji.SAD_BUT_RELIEVED_FACE)


@Client.on_message(filters.command("codifica", prefixes=PREFIXES))
async def on_encode(_, message):
    try:
        codified = message.reply_to_message.text if message.reply_to_message else ' '.join(message.command[1:])

        await message.reply_text(f"<code>{codified}</code>")

    except MessageEmpty:
        message.reply_text("Scrivi qualcosa da codificare o rispondi a un messaggio")


@Client.on_message(filters.command("spelling", prefixes=PREFIXES))
async def on_spelling(client, message):
    try:
        if message.reply_to_message:
            spelling = '_'.join(message.reply_to_message.text.split(' '))
        else:
            spelling = '_'.join(message.command[1:])

        message = await message.reply_text(spelling[0])
        chat_id = message.chat.id
        message_id = message.message_id

        for x in range(1, len(spelling)):
            sleep(0.25)

            message.text += spelling[x]
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=message.text)

    except IndexError:
        await message.reply_text("Spelling de che?")


@Client.on_message(filters.regex("non c'è$"))
async def on_laura_is_not_here(_, message):
    name = message.text[:len(message.text) - len("non c'è")]

    await message.reply_text("è andata via")
    await message.reply_text(f"{name}non è più cosa mia")


@Client.on_message(filters.regex("se n'è andato e non ritorna più$"))
async def on_marco_has_gone_and_will_not_return(_, message):
    name = message.text[:len(message.text) - len("se n'è andato e non ritorna più")]

    await message.reply_text("il treno delle 7 parte senza te")

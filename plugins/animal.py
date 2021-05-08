import json
import random
from pyrogram import Client, filters
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("add", prefixes=PREFIXES))
async def on_add_animal(_, message):
    try:
        key = message.command[1]
        things = message.command[2:]

        if len(things) == 0:
            await message.reply_text(f"Inserisci almeno un {key}")
            return

        with open("animals.json", "r") as x:
            data = json.load(x)

        new = [thing for thing in things if thing not in data[key]]
        already_in = [thing for thing in things if thing in data[key]]

        for thing in new:
            data[key].append(thing)

        with open("animals.json", "w") as x:
            json.dump(data, x, indent=4)

        await message.reply_text(f"{key} nuovi: \n » {new}\n"
                                 f"{key} già presenti: \n » {already_in}")

    except IndexError:
        await message.reply_text("Specifica key e oggetto")

    except KeyError:
        await message.reply_text("Usa animals o noun")


@Client.on_message(filters.command("remove", prefixes=PREFIXES))
async def on_remove_animal(_, message):
    try:
        key = message.command[1]
        things = message.command[2:]

        if len(things) == 0:
            await message.reply_text(f"Inserisci almeno un {key}")
            return

        with open("animals.json", "r") as x:
            data = json.load(x)

        to_remove = [thing for thing in things if thing in data[key]]
        not_in = [thing for thing in things if thing not in data[key]]

        for thing in to_remove:
            data[key].remove(thing)

        with open("animals.json", "w") as x:
            json.dump(data, x, indent=4)

        await message.reply_text(f"{key} nuovi: \n » {to_remove}\n"
                                 f"{key} già presenti: \n » {not_in}")

    except IndexError:
        await message.reply_text("Specifica key e oggetto")

    except KeyError:
        await message.reply_text("Usa animals o noun")


@Client.on_message(filters.command("nome scemo per", prefixes=PREFIXES))
async def on_silly_name(client, message):
    try:
        usr = message.command[1]
        usr_id = await client.get_users(usr)
        usr_id = f"{usr_id.id}"
    except IndexError:
        await message.reply_text("Inserisci un username")
        return
    except UsernameInvalid:
        await message.reply_text("Inserisci un username valido")
        return

    with open("animals.json", "r") as x:
        data = json.load(x)

    if usr_id in data.keys():
        await message.reply_text(f"Nome scemo per {usr}: {data[usr_id]}")
        return

    animal = random.choice(data["animals"])
    noun = random.choice(data["nouns"])

    data.update({usr_id: f"{animal} {noun}"})

    with open("animals.json", "w") as x:
        json.dump(data, x, indent=4)

    await message.reply_text(f"Nome scemo per {usr}: {data[usr_id]}")


@Client.on_message(filters.command("togli nome scemo per", prefixes=PREFIXES) |
                   filters.command("toji nome scemo per", prefixes=PREFIXES))
async def on_delete_silly_noun(client, message):
    try:
        usr = message.command[1]
        usr_id = await client.get_users(usr)
        usr_id = f"{usr_id.id}"
    except IndexError:
        await message.reply_text("Inserisci un username")
        return
    except UsernameInvalid:
        await message.reply_text("Inserisci un username valido")
        return
    except UsernameNotOccupied:
        await message.reply_text("L'username che hai inserito non è utilizzato da nessuno")
        return

    with open("animals.json", "r") as x:
        data = json.load(x)

    if usr_id not in data.keys():
        await message.reply_text(f"{usr} non ha ancora un nome scemo")
        return

    data.pop(usr_id)

    with open("animals.json", "w") as x:
        json.dump(data, x, indent=4)

    await message.reply_text(f"Nome scemo per {usr} eliminato")

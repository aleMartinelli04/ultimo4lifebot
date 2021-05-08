import random
import json
from pyrogram.errors.exceptions import forbidden_403
from pyrogram import Client, filters, emoji

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("aggiungi", prefixes=PREFIXES))
async def on_add_something(_, message):
    if message.from_user.id != 511831945:
        await message.reply_text("Operazione negata")
        return

    if message.reply_to_message:
        media = message.reply_to_message.sticker \
                or message.reply_to_message.photo \
                or message.reply_to_message.animation \
                or message.reply_to_message.video

        key = ' '.join(message.command[1:])

        try:
            file_id = media.file_id

        except AttributeError:
            await message.reply_text(f"Rispondi a un {key}")
            return

        with open("data.json", "r") as x:
            data = json.load(x)

        if key not in data.keys():
            data.update({key: [file_id]})
            await message.reply_text(f"Creata nuova chiave: <code>{key}</code>")

            with open("data.json", "w") as write_file:
                json.dump(data, write_file, indent=4)

            await message.reply_to_message.reply_text(f"Aggiunto a <code>{key}</code>!")
            return

        if file_id in data[key]:
            await message.reply_to_message.reply_text(f"C'è già in <code>{key}</code>")
            return

        data[key].append(file_id)

        with open("data.json", "w+") as write_file:
            json.dump(data, write_file, indent=4)

        await message.reply_to_message.reply_text(f"Aggiunto a <code>{key}</code>!")

    else:
        await message.reply_text("Rispondi a uno sticker, una gif o un'immagine")


@Client.on_message(filters.command("rimuovi", prefixes=PREFIXES))
async def on_remove_something(_, message):
    if message.from_user.id != 511831945:
        await message.reply_text("Operazione negata")
        return

    if message.reply_to_message:
        media = message.reply_to_message.sticker \
                or message.reply_to_message.photo \
                or message.reply_to_message.animation \
                or message.reply_to_message.video

        key = ' '.join(message.command[1:])

        try:
            file_id = media.file_id

        except AttributeError:
            await message.reply_text(f"Rispondi a un {key}")
            return

        with open("data.json", "r") as x:
            data = json.load(x)

        if key not in data.keys():
            await message.reply_text(f"La chiave <code>{key}</code> non esiste")
            return

        if file_id not in data[key]:
            await message.reply_to_message.reply_text(f"Non c'è in {key}")
            return

        data.get(key).remove(file_id)

        with open("data.json", "w+") as write_file:
            json.dump(data, write_file, indent=4)

        await message.reply_to_message.reply_text(f"Rimosso da <code>{key}</code>!")

    else:
        await message.reply_text("Rispondi a una gif, uno sticker o un'immagine")


@Client.on_message(filters.command("keys", prefixes=PREFIXES))
async def on_keys(_, message):
    with open("data.json", "r") as x:
        data = json.load(x)

    key_list = "\n\t» ".join(
        [str(key) + ": " + (str(len(value)) + "  " + emoji.WARNING if len(value) == 0 else str(len(value)))
         for key, value in data.items()]
    )

    await message.reply_text(f"Lista delle chiavi: \n\t» {key_list}")


@Client.on_message(filters.command("pop", prefixes=PREFIXES))
async def on_pop(_, message):
    if message.from_user.id != 511831945:
        await message.reply_text("Operazione negata")
        return

    try:
        with open("data.json", "r") as x:
            data = json.load(x)

        if message.command[1] == "all":
            deleted_keys = [key for key, value in data.items() if len(value) == 0]

            for key in deleted_keys:
                data.pop(key)

            with open("data.json", "w+") as write_file:
                json.dump(data, write_file, indent=4)

            await message.reply_text("Nessuna chiave eliminata" if len(deleted_keys) == 0 else
                                     "Chiavi eliminate: \n\t» " + '\n\t» '.join(deleted_keys))
            return

        delete_key = ' '.join(message.command[1:])

        data.pop(delete_key)

        with open("data.json", "w+") as write_file:
            json.dump(data, write_file, indent=4)

        await message.reply_text(f"Chiave eliminata: <code>{delete_key}</code>")

    except IndexError:
        await message.reply_text("Usa <code>all</code> se vuoi eliminare tutte le keys vuote, "
                                 "altrimenti specifica il nome della key")

    except KeyError:
        await message.reply_text("Key inesistente")


@Client.on_message(filters.command("send", prefixes=PREFIXES))
async def on_send_all(_, message):
    try:
        key = ' '.join(message.command[1:])

        with open("data.json", "r") as x:
            data = json.load(x)

        if key == "all":
            selected = []
            for key in data.keys():
                for value in data[key]:
                    selected.append(value)
            await message.reply_text("Elementi presenti in <code>data.json</code>")

        else:
            selected = data[key]

            await message.reply_text(f"Elementi nella key <code>{key}</code>")

        for thing in selected:
            try:
                await message.reply_photo(thing)
                continue
            except ValueError:
                try:
                    await message.reply_sticker(thing)
                except ValueError:
                    try:
                        await message.reply_animation(thing)
                    except ValueError:
                        await message.reply_video(thing)

    except KeyError:
        await message.reply_text("La key specificata non esiste")


@Client.on_message()
async def on_send(_, message):
    with open("data.json", "r") as list_all:
        data = json.load(list_all)

    key_list = data.keys()

    if message.text in key_list:
        choices = data[message.text]

        selected = random.choice(choices)

        message = message.reply_to_message or message

        try:
            await message.reply_sticker(selected)
        except ValueError:
            try:
                await message.reply_photo(selected)
            except ValueError:
                try:
                    await message.reply_animation(selected)
                except ValueError:
                    await message.reply_video(selected)

from pyrogram import Client, filters, emoji
from pyrogram.errors import MessageDeleteForbidden

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("ciao", prefixes=PREFIXES))
async def on_hello(_, message):
    await message.reply_text("Ciao a te!")


@Client.on_message(filters.command("ti spengo", prefixes=PREFIXES))
async def on_turn_off(_, message):
    await message.reply_text("Ok, a domani!")


@Client.on_message(filters.command("dimmi qualcosa di te", prefixes=PREFIXES))
async def on_tell_something(_, message):
    await message.reply_text(
        "Mi chiamo Niccolò Moriconi, sono nato il 27 gennaio 1996, sono romano de Roma " + emoji.SMILING_FACE)


bad_names = ["di merda", "schifo", "merda", "brutto", "suka", "cacca", "taci"]


@Client.on_message(filters.command(bad_names, prefixes=PREFIXES))
async def on_bad_name(_, message):
    try:
        await message.reply_text("Come ti permetti!?")
        await message.delete()

    except MessageDeleteForbidden:
        await message.reply_text("Te la faccio passare liscia solo perché non ho le autorizzazioni...")

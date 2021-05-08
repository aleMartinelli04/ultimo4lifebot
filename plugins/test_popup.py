from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex("^prova$"))
async def popup(_, callback):
    await callback.answer(text=callback.from_user.username, show_alert=True)


@Client.on_message(filters.command("test"))
async def test(_, message):

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("prova", callback_data="prova")]
    ])

    await message.reply_text("lollo", reply_markup=keyboard)

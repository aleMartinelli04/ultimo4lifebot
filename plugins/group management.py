from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired

PREFIXES = ["Ultimo ", "ultimo "]


@Client.on_message(filters.command("elimina", prefixes=PREFIXES))
async def on_delete(_, message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.delete()
            await message.delete()
        except ChatAdminRequired:
            await message.reply_text("Non ho i permessi per eliminare messaggi")

    else:
        await message.reply_text("Rispondi a un messaggio per eliminarlo")


@Client.on_message(filters.command("fissa", prefixes=PREFIXES))
async def on_pin(_, message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.pin()
            await message.reply_to_message.reply_text("Messaggio fissato!")

        except ChatAdminRequired:
            await message.reply_text("Non ho i permessi per fissare i messaggi")

    else:
        await message.reply_text("Rispondi a un messaggio per fissarlo")


@Client.on_message(filters.command("unpinna", prefixes=PREFIXES))
async def on_unpin(client, message):
    if message.reply_to_message:
        try:
            chat_id = message.chat.id

            await client.unpin_chat_message(chat_id=chat_id)
            await message.reply_to_message.reply_text("Messaggio tolto dai messaggi fissati")

        except ChatAdminRequired:
            await message.reply_text("Non ho i permessi per togliere un messaggio fissato")

    else:
        await message.reply_text("Rispondi a un messaggio fissato per toglierlo")


@Client.on_message(filters.command("rinomina", prefixes=PREFIXES))
def on_name(client, message):
    try:
        chat_member = message.command[1]
        user_id = client.get_users(chat_member).id
        chat_id = message.chat.id
        new_name = ' '.join(message.command[2:])
        client.set_administrator_title(chat_id, user_id, new_name)
        message.reply_text(f"Rinominato {chat_member} come {new_name}!")

    except ChatAdminRequired:
        message.reply_text("A quanto pare non ho i permessi per fare queste cose...")

    except IndexError:
        message.reply_text(
            "Controlla quello che hai scritto. C'è qualcosa di sbagliato.\n"
            "Scrivi per esempio <code>Ultimo rinomina @username nome</code>!")


@Client.on_message(filters.command("promuovi", prefixes=PREFIXES))
async def on_promote(client, message):
    try:
        chat_id = message.chat.id
        user = message.command[1]
        await client.promote_chat_member(chat_id, user)
        await message.reply_text(f"Congratulazioni {message.command[1]}, ora sei un admin!")

    except ChatAdminRequired:
        await message.reply_text("A quanto pare non ho i permessi per fare queste cose...")

    except IndexError:
        await message.reply_text("Chi devo promuovere?")


@Client.on_message(filters.command("retrocedi", prefixes=PREFIXES))
async def on_downgrade(client, message):
    try:

        chat_id = message.chat.id
        user = message.command[1]
        user_id = client.get_users(user).id

        await client.promote_chat_member(chat_id,
                                         user_id,
                                         can_change_info=False,
                                         can_restrict_members=False,
                                         can_delete_messages=True,
                                         can_promote_members=False,
                                         can_edit_messages=True,
                                         can_invite_users=False,
                                         can_pin_messages=True,
                                         can_post_messages=True)

        await message.reply_text(f"Mi spiace {message.command[1]}, ora non sei più un admin...")

    except ChatAdminRequired:
        await message.reply_text("A quanto pare non ho i permessi per fare queste cose...")

    except IndexError:
        await message.reply_text("Chi non deve più fare l'admin?")

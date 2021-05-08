from pyrogram import Client

import config

appClient = Client(session_name=config.session_name,
                   api_id=config.api_id,
                   api_hash=config.api_hash,
                   bot_token=config.bot_token)


if __name__ == '__main__':
    appClient.run()

"""
SML Bot — DigitalOcean VPS Manager
Dev: @codeninjaxd | Brand: SML The Unknown
"""
import json
import sys
from os import environ


def parse_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        environ['bot_name']   = config['BOT']['NAME']
        environ['bot_token']  = config['BOT']['TOKEN']
        environ['bot_admins'] = json.dumps(config['BOT']['ADMINS'])
    except FileNotFoundError:
        print('[ERROR] config.json not found. Run the start script first.')
        sys.exit(1)
    except KeyError as e:
        print(f'[ERROR] Missing key in config.json: {e}')
        sys.exit(1)


def start_bot():
    from bot import bot
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('  🔥 SML Bot — DigitalOcean VPS Manager')
    print('  Dev: @codeninjaxd | SML The Unknown')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print(f'  Bot Name : {environ.get("bot_name")}')
    print(f'  Admins   : {environ.get("bot_admins")}')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('  ✅ Bot is running...')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    bot.infinity_polling(logger_level=20)


if __name__ == '__main__':
    parse_config()
    start_bot()

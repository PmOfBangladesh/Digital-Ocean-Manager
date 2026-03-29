import json
import logging
import traceback
from os import environ
from typing import Union
import urllib.parse as urlparse
from urllib.parse import parse_qs

import telebot
from telebot.types import CallbackQuery, Message
from _bot import bot
from modules import *

bot_admins = json.loads(environ.get('bot_admins', '[]'))

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

COMMAND_MAP = {
    '/start':    'start',
    '/add_do':   'add_account',
    '/sett_do':  'manage_accounts',
    '/bath_do':  'batch_test_accounts',
    '/add_vps':  'create_droplet',
    '/sett_vps': 'manage_droplets',
    '/ping':     'ping',
}


def _is_admin(user_id: int) -> bool:
    return user_id in bot_admins


@bot.message_handler(content_types=['text'])
def text_handler(m: Message):
    try:
        logger.info(m)
        if not _is_admin(m.from_user.id):
            bot.send_message(
                chat_id=m.from_user.id,
                text=(
                    '🔒 <b>Access Denied</b>\n'
                    '━━━━━━━━━━━━━━━━━━━━\n'
                    'You are not authorized to use this bot.\n'
                    '<i>@codeninjaxd | SML The Unknown</i>'
                ),
                parse_mode='HTML'
            )
            return
        func_name = COMMAND_MAP.get(m.text)
        if func_name and func_name in globals():
            globals()[func_name](m)
    except Exception as e:
        traceback.print_exc()
        _handle_exception(m, e)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    try:
        logger.info(call)
        if not _is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, '🔒 Access denied.')
            return

        # Handle JSON-encoded callbacks (legacy batch_test_delete)
        if call.data.startswith('{'):
            try:
                payload = json.loads(call.data)
                func_name = payload.get('t')
                if func_name and func_name in globals():
                    globals()[func_name](call)
                return
            except json.JSONDecodeError:
                pass

        parsed = urlparse.urlparse(call.data)
        func_name = parsed.path
        data = parse_qs(parsed.query)

        if func_name in globals():
            args = [call]
            if data:
                args.append(data)
            globals()[func_name](*args)
        else:
            bot.answer_callback_query(call.id, f'Unknown action: {func_name}')

    except Exception as e:
        traceback.print_exc()
        _handle_exception(call, e)


def _handle_exception(d: Union[Message, CallbackQuery], e: Exception):
    chat_id = d.from_user.id
    bot.send_message(
        chat_id=chat_id,
        text=(
            f'⚠️ <b>An error occurred</b>\n'
            f'━━━━━━━━━━━━━━━━━━━━\n'
            f'<code>{str(e)}</code>\n'
            f'<i>@codeninjaxd | SML The Unknown</i>'
        ),
        parse_mode='HTML'
    )

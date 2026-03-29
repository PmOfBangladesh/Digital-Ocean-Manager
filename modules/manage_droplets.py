from typing import Union
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def manage_droplets(d: Union[Message, CallbackQuery]):
    accounts = AccountsDB().all()
    markup = InlineKeyboardMarkup()
    t = f'🖥 <b>VPS Manager</b>\n{DIVIDER}\n'

    if not accounts:
        t += '❌ No accounts found. Add a DigitalOcean account first.'
        markup.row(InlineKeyboardButton('➕ Add Account', callback_data='add_account'))
        markup.row(InlineKeyboardButton('🔙 Back',        callback_data='back_to_start'))
    else:
        t += '🔽 <b>Select an account to view its VPS:</b>'
        for acc in accounts:
            markup.row(InlineKeyboardButton(
                f'👤 {acc["email"]}',
                callback_data=f'list_droplets?doc_id={acc.doc_id}'
            ))
        markup.row(InlineKeyboardButton('🔙 Back', callback_data='back_to_start'))

    _send_or_edit(d, t, markup)


def _send_or_edit(d, text, markup):
    from telebot.types import CallbackQuery
    if isinstance(d, CallbackQuery):
        bot.edit_message_text(text=text, chat_id=d.from_user.id,
                              message_id=d.message.message_id,
                              parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(text=text, chat_id=d.from_user.id,
                         parse_mode='HTML', reply_markup=markup)

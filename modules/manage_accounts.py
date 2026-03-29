from typing import Union
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def manage_accounts(d: Union[Message, CallbackQuery]):
    accounts = AccountsDB().all()
    markup = InlineKeyboardMarkup()
    t = f'⚙️ <b>Account Manager</b>\n{DIVIDER}\n'

    if not accounts:
        t += '❌ No accounts linked yet.'
        markup.row(InlineKeyboardButton('➕ Add Account',    callback_data='add_account'))
        markup.row(InlineKeyboardButton('🔙 Back to Menu',  callback_data='back_to_start'))
        _send_or_edit(d, t, markup)
        return

    t += f'💳 Total accounts: <code>{len(accounts)}</code>\n{DIVIDER}\n'
    markup.row(InlineKeyboardButton('🧪 Batch Test All', callback_data='batch_test_accounts'))
    markup.row(InlineKeyboardButton('➕ Add Account',    callback_data='add_account'))
    for acc in accounts:
        label = f'👤 {acc.get("email","unknown")}'
        if acc.get('remarks'):
            label += f' [{acc["remarks"]}]'
        markup.row(InlineKeyboardButton(label, callback_data=f'account_detail?doc_id={acc.doc_id}'))
    markup.row(InlineKeyboardButton('🔙 Back to Menu', callback_data='back_to_start'))

    _send_or_edit(d, t, markup)


def _send_or_edit(d, text, markup):
    from telebot.types import CallbackQuery
    if isinstance(d, CallbackQuery):
        bot.edit_message_text(
            text=text, chat_id=d.from_user.id,
            message_id=d.message.message_id,
            parse_mode='HTML', reply_markup=markup
        )
    else:
        bot.send_message(
            text=text, chat_id=d.from_user.id,
            parse_mode='HTML', reply_markup=markup
        )

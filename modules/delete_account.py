from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER


def delete_account(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]

    # Confirm step
    if data.get('confirm', ['0'])[0] != '1':
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton('✅ Yes, Delete', callback_data=f'delete_account?doc_id={doc_id}&confirm=1'),
            InlineKeyboardButton('❌ Cancel',      callback_data=f'account_detail?doc_id={doc_id}'),
        )
        bot.edit_message_text(
            text=f'{call.message.html_text}\n\n⚠️ <b>Are you sure you want to delete this account?</b>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
        return

    try:
        AccountsDB().remove(doc_id=doc_id)
    except Exception as e:
        bot.edit_message_text(
            text=f'{call.message.html_text}\n\n❌ <b>Error deleting account:</b> <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('⚙️ Manage Accounts', callback_data='manage_accounts'),
        InlineKeyboardButton('🔙 Main Menu',        callback_data='back_to_start'),
    )
    bot.edit_message_text(
        text=(
            f'🗑 <b>Account Deleted</b>\n'
            f'{DIVIDER}\n'
            f'✅ The account has been removed successfully.'
        ),
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from digitalocean import DataReadError
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def batch_test_delete_accounts(call: CallbackQuery):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Deleting invalid accounts...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    db = AccountsDB()
    accounts = db.all()
    deleted, errors = [], []

    for account in accounts:
        try:
            digitalocean.Balance().get_object(api_token=account['token'])
        except DataReadError:
            try:
                db.remove(doc_id=account.doc_id)
                deleted.append(account['email'])
            except Exception as e:
                errors.append(f'{account["email"]}: {str(e)}')

    t = (
        f'🗑 <b>Cleanup Complete</b>\n'
        f'{DIVIDER}\n'
        f'✅ Deleted: <code>{len(deleted)}</code> accounts\n'
    )
    if deleted:
        for d_ in deleted:
            t += f'  • <code>{d_}</code>\n'
    if errors:
        t += f'\n❌ Errors ({len(errors)}):\n'
        for e_ in errors:
            t += f'  • <code>{e_}</code>\n'

    t += f'{DIVIDER}\n<i>{BOT_TAG}</i>'

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('⚙️ Manage Accounts', callback_data='manage_accounts'),
        InlineKeyboardButton('🔙 Main Menu',        callback_data='back_to_start'),
    )
    bot.edit_message_text(
        text=t,
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

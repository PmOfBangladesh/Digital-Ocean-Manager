from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from digitalocean import DataReadError
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def account_detail(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    account = AccountsDB().get(doc_id=doc_id)

    msg = bot.send_message(
        text=f'📋 <b>Account Info</b>\n{DIVIDER}\n⏳ Fetching details...',
        chat_id=call.from_user.id,
        parse_mode='HTML'
    )

    t = (
        f'📋 <b>Account Info</b>\n'
        f'{DIVIDER}\n'
        f'📧 <b>Email:</b> <code>{account["email"]}</code>\n'
        f'📝 <b>Remark:</b> <code>{account.get("remarks") or "—"}</code>\n'
        f'📅 <b>Added:</b> <code>{account["date"]}</code>\n'
        f'🔑 <b>Token:</b> <code>{account["token"][:20]}...</code>\n'
        f'{DIVIDER}\n'
    )

    try:
        bal = digitalocean.Balance().get_object(api_token=account['token'])
        t += (
            f'💰 <b>Balance:</b> <code>${bal.account_balance}</code>\n'
            f'📆 <b>Month Usage:</b> <code>${bal.month_to_date_usage}</code>\n'
            f'🕐 <b>Billed at:</b> <code>{bal.generated_at.split("T")[0]}</code>\n'
        )
    except DataReadError:
        t += '⚠️ <b>Token is invalid or expired.</b>\n'
    except Exception as e:
        t += f'❌ <b>Error fetching balance:</b> <code>{str(e)}</code>\n'

    t += f'{DIVIDER}\n<i>{BOT_TAG}</i>'

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('🗑 Delete Account', callback_data=f'delete_account?doc_id={account.doc_id}')
    )
    markup.row(
        InlineKeyboardButton('🖥 View Droplets',  callback_data=f'list_droplets?doc_id={account.doc_id}'),
        InlineKeyboardButton('🔙 Back',           callback_data='manage_accounts'),
    )
    bot.edit_message_text(
        text=t,
        chat_id=call.from_user.id,
        message_id=msg.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

import json
from typing import Union
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from digitalocean import DataReadError
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def batch_test_accounts(d: Union[Message, CallbackQuery]):
    msg = bot.send_message(
        text=f'🧪 <b>Batch Account Test</b>\n{DIVIDER}\n⏳ Testing all accounts...',
        chat_id=d.from_user.id,
        parse_mode='HTML'
    )

    accounts = AccountsDB().all()
    if not accounts:
        bot.edit_message_text(
            text=f'🧪 <b>Batch Account Test</b>\n{DIVIDER}\n❌ No accounts found.',
            chat_id=d.from_user.id,
            message_id=msg.message_id,
            parse_mode='HTML'
        )
        return

    passed, failed = [], []

    for account in accounts:
        try:
            bal = digitalocean.Balance().get_object(api_token=account['token'])
            passed.append({
                'email': account['email'],
                'balance': bal.account_balance,
                'usage': bal.month_to_date_usage,
            })
        except DataReadError:
            failed.append(account['email'])
        except Exception as e:
            bot.edit_message_text(
                text=f'❌ Error: <code>{str(e)}</code>',
                chat_id=d.from_user.id,
                message_id=msg.message_id,
                parse_mode='HTML'
            )
            return

    t = (
        f'🧪 <b>Batch Test Results</b>\n'
        f'{DIVIDER}\n'
        f'📊 Total: <code>{len(accounts)}</code> | '
        f'✅ OK: <code>{len(passed)}</code> | '
        f'❌ Fail: <code>{len(failed)}</code>\n'
        f'{DIVIDER}\n'
    )

    if passed:
        t += f'✅ <b>Valid Accounts ({len(passed)}):</b>\n'
        for p in passed:
            t += f'  • <code>{p["email"]}</code>\n'
            t += f'    💰 Balance: <code>${p["balance"]}</code> | Usage: <code>${p["usage"]}</code>\n'
        t += '\n'

    if failed:
        t += f'❌ <b>Invalid Accounts ({len(failed)}):</b>\n'
        for f_ in failed:
            t += f'  • <code>{f_}</code>\n'

    t += f'{DIVIDER}\n<i>{BOT_TAG}</i>'

    markup = InlineKeyboardMarkup()
    if failed:
        markup.row(InlineKeyboardButton(
            '🗑 Delete All Failed',
            callback_data=json.dumps({'t': 'batch_test_delete_accounts'})
        ))
    markup.row(
        InlineKeyboardButton('🔄 Re-Test',       callback_data='batch_test_accounts'),
        InlineKeyboardButton('🔙 Back',           callback_data='manage_accounts'),
    )

    bot.edit_message_text(
        text=t,
        chat_id=d.from_user.id,
        message_id=msg.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

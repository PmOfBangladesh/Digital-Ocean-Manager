from typing import Union
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from digitalocean import DataReadError
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def add_account(d: Union[Message, CallbackQuery]):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('❌ Cancel', callback_data='back_to_start'))
    t = (
        f'➕ <b>Add DigitalOcean Account</b>\n'
        f'{DIVIDER}\n'
        f'Send your DO API token(s) below.\n'
        f'Get your token: <a href="https://cloud.digitalocean.com/account/api/tokens">Click Here</a>\n\n'
        f'<b>Format (one per line):</b>\n'
        f'<code>token123</code> — token only\n'
        f'<code>token123:MyNote</code> — token with remark\n\n'
        f'You can paste <b>multiple tokens</b> at once.\n\n'
        f'/cancel — Cancel\n'
        f'{DIVIDER}\n'
        f'<i>{BOT_TAG}</i>'
    )
    msg = bot.send_message(
        text=t,
        chat_id=d.from_user.id,
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, _add_account_handler)


def _add_account_handler(m: Message):
    from modules.start import start
    if m.text and m.text.strip() == '/cancel':
        start(m)
        return

    msg = bot.send_message(
        text='⏳ <b>Processing accounts...</b>',
        chat_id=m.from_user.id,
        parse_mode='HTML'
    )

    lines = [l.strip() for l in m.text.strip().split('\n') if l.strip()]
    added, failed, duplicate = [], [], []

    for line in lines:
        if ':' in line:
            token, remarks = line.split(':', 1)
        else:
            token, remarks = line, ''
        token = token.strip()
        try:
            email = digitalocean.Account().get_object(api_token=token).email
            AccountsDB().save(email=email, token=token, remarks=remarks.strip())
            added.append(email)
        except DataReadError:
            failed.append(token[:20] + '...')
        except Exception as e:
            if 'already exists' in str(e).lower():
                duplicate.append(token[:20] + '...')
            else:
                bot.edit_message_text(
                    text=f'❌ <b>Unexpected error:</b>\n<code>{str(e)}</code>',
                    chat_id=m.from_user.id,
                    message_id=msg.message_id,
                    parse_mode='HTML'
                )
                return

    t = f'📋 <b>Account Import Result</b>\n{DIVIDER}\n'
    t += f'Total submitted: <code>{len(lines)}</code>\n\n'

    if added:
        t += f'✅ Added ({len(added)}):\n'
        for a in added:
            t += f'  • <code>{a}</code>\n'
        t += '\n'
    if duplicate:
        t += f'⚠️ Duplicate ({len(duplicate)}):\n'
        for d in duplicate:
            t += f'  • <code>{d}</code>\n'
        t += '\n'
    if failed:
        t += f'❌ Invalid token ({len(failed)}):\n'
        for f_ in failed:
            t += f'  • <code>{f_}</code>\n'

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('➕ Add More', callback_data='add_account'),
        InlineKeyboardButton('🔙 Menu',     callback_data='back_to_start'),
    )
    bot.edit_message_text(
        text=t,
        chat_id=m.from_user.id,
        message_id=msg.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

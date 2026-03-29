from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from _bot import bot
from utils.db import AccountsDB
from utils.localizer import localize_region
from utils.helpers import DIVIDER, BOT_TAG


def droplet_detail(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    droplet_id = data['droplet_id'][0]

    try:
        account = AccountsDB().get(doc_id=doc_id)
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error fetching account:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'📋 <b>Server Info</b>\n{DIVIDER}\n⏳ Loading instance data...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        droplet = digitalocean.Droplet().get_object(
            api_token=account['token'],
            droplet_id=droplet_id
        )
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error fetching droplet:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    status_icon = {'active': '🟢 Active', 'off': '🔴 Off', 'archive': '⚫ Archived'}
    status = status_icon.get(droplet.status, f'🟡 {droplet.status}')

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('🗑 Delete', callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=delete'))

    if droplet.status == 'active':
        markup.row(
            InlineKeyboardButton('🔴 Shutdown',      callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=shutdown'),
            InlineKeyboardButton('🔄 Reboot',        callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=reboot'),
        )
        markup.row(
            InlineKeyboardButton('🔧 Rebuild',       callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=rebuild'),
            InlineKeyboardButton('🔑 Reset Password', callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=reset_password'),
        )
    else:
        markup.row(InlineKeyboardButton('🟢 Power On', callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=power_on'))

    markup.row(
        InlineKeyboardButton('🔃 Refresh', callback_data=f'droplet_detail?doc_id={doc_id}&droplet_id={droplet_id}'),
        InlineKeyboardButton('🔙 Back',    callback_data=f'list_droplets?doc_id={doc_id}'),
    )

    bot.edit_message_text(
        text=(
            f'📋 <b>Server Info</b>\n'
            f'{DIVIDER}\n'
            f'👤 Account:   <code>{account["email"]}</code>\n'
            f'🏷 Name:      <code>{droplet.name}</code>\n'
            f'📦 Size:      <code>{droplet.size_slug}</code>\n'
            f'🌍 Region:    <code>{localize_region(droplet.region["slug"])}</code>\n'
            f'🖥 OS:        <code>{droplet.image["distribution"]} {droplet.image["name"]}</code>\n'
            f'💾 Disk:      <code>{droplet.disk} GB</code>\n'
            f'🌐 Public IP: <code>{droplet.ip_address}</code>\n'
            f'🔒 Priv IP:   <code>{droplet.private_ip_address or "—"}</code>\n'
            f'⚡ Status:    {status}\n'
            f'📅 Created:   <code>{droplet.created_at.split("T")[0]}</code>\n'
            f'{DIVIDER}\n'
            f'<b>SSH:</b> <code>ssh root@{droplet.ip_address}</code>\n'
            f'{DIVIDER}\n'
            f'<i>{BOT_TAG}</i>'
        ),
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from _bot import bot
from utils.db import AccountsDB
from utils.localizer import localize_region
from utils.helpers import DIVIDER, BOT_TAG


def list_droplets(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    t = f'🖥 <b>VPS List</b>\n{DIVIDER}\n'

    try:
        account = AccountsDB().get(doc_id=doc_id)
    except Exception as e:
        bot.edit_message_text(
            text=f'{t}❌ Error fetching account:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'{t}👤 Account: <code>{account["email"]}</code>\n\n⏳ Fetching VPS list...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        droplets = digitalocean.Manager(token=account['token']).get_all_droplets()
    except Exception as e:
        bot.edit_message_text(
            text=f'{t}❌ Error fetching droplets:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    markup = InlineKeyboardMarkup()
    if not droplets:
        markup.row(InlineKeyboardButton(
            '➕ Create VPS',
            callback_data=f'create_droplet?nf=select_region&doc_id={account.doc_id}'
        ))
        markup.row(InlineKeyboardButton('🔙 Back', callback_data='manage_droplets'))
        bot.edit_message_text(
            text=f'{t}👤 Account: <code>{account["email"]}</code>\n\n❌ No VPS instances found.',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
        return

    status_icon = {'active': '🟢', 'off': '🔴', 'archive': '⚫'}
    for d_ in droplets:
        icon = status_icon.get(d_.status, '🟡')
        markup.row(InlineKeyboardButton(
            f'{icon} {d_.name} | {localize_region(d_.region["slug"])} | {d_.size_slug}',
            callback_data=f'droplet_detail?doc_id={account.doc_id}&droplet_id={d_.id}'
        ))

    markup.row(
        InlineKeyboardButton('➕ New VPS',  callback_data=f'create_droplet?nf=select_region&doc_id={account.doc_id}'),
        InlineKeyboardButton('🔙 Back',     callback_data='manage_droplets'),
    )

    bot.edit_message_text(
        text=(
            f'{t}'
            f'👤 Account: <code>{account["email"]}</code>\n'
            f'🖥 Instances: <code>{len(droplets)}</code>\n'
            f'{DIVIDER}\n'
            f'🔽 Select a VPS to manage:'
        ),
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

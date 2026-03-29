from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG


def droplet_actions(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    droplet_id = data['droplet_id'][0]
    action = data['a'][0]

    # Confirm before destructive actions
    if action == 'delete' and data.get('confirm', ['0'])[0] != '1':
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton(
                '✅ Yes, Delete',
                callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=delete&confirm=1'
            ),
            InlineKeyboardButton(
                '❌ Cancel',
                callback_data=f'droplet_detail?doc_id={doc_id}&droplet_id={droplet_id}'
            ),
        )
        bot.edit_message_text(
            text=f'{call.message.html_text}\n\n⚠️ <b>Are you sure you want to DELETE this VPS?\nThis action is irreversible.</b>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
        return

    try:
        account = AccountsDB().get(doc_id=doc_id)
        droplet = digitalocean.Droplet(token=account['token'], id=droplet_id)
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error loading droplet:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    handler = {
        'delete':         _delete,
        'shutdown':       _shutdown,
        'reboot':         _reboot,
        'power_on':       _power_on,
        'rebuild':        _rebuild,
        'reset_password': _reset_password,
    }.get(action)

    if handler:
        handler(call, droplet, doc_id)
    else:
        bot.edit_message_text(
            text=f'❌ Unknown action: <code>{action}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )


def _back_btn(doc_id, droplet_id):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        '🔍 View Droplet',
        callback_data=f'droplet_detail?doc_id={doc_id}&droplet_id={droplet_id}'
    ))
    markup.row(InlineKeyboardButton('🔙 VPS List', callback_data=f'list_droplets?doc_id={doc_id}'))
    return markup


def _delete(call: CallbackQuery, droplet: digitalocean.Droplet, doc_id: str):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Deleting VPS...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
    try:
        droplet.load()
        droplet.destroy()
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error deleting VPS:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('🖥 VPS List',   callback_data=f'list_droplets?doc_id={doc_id}'),
        InlineKeyboardButton('🔙 Main Menu',  callback_data='back_to_start'),
    )
    bot.edit_message_text(
        text=(
            f'🗑 <b>VPS Deleted</b>\n'
            f'{DIVIDER}\n'
            f'✅ The droplet has been permanently destroyed.\n'
            f'{DIVIDER}\n'
            f'<i>{BOT_TAG}</i>'
        ),
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


def _shutdown(call: CallbackQuery, droplet: digitalocean.Droplet, doc_id: str):
    droplet_id = droplet.id
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Shutting down VPS...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=call.message.reply_markup
    )
    try:
        droplet.load()
        droplet.shutdown()
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error shutting down:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n🔴 <b>Shutdown command sent.</b>\nRefresh to see updated status.',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=_back_btn(doc_id, droplet_id)
    )


def _reboot(call: CallbackQuery, droplet: digitalocean.Droplet, doc_id: str):
    droplet_id = droplet.id
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Rebooting VPS...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=call.message.reply_markup
    )
    try:
        droplet.load()
        droplet.reboot()
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error rebooting:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n🔄 <b>Reboot command sent.</b>\nRefresh to see updated status.',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=_back_btn(doc_id, droplet_id)
    )


def _power_on(call: CallbackQuery, droplet: digitalocean.Droplet, doc_id: str):
    droplet_id = droplet.id
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Powering on VPS...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=call.message.reply_markup
    )
    try:
        droplet.load()
        droplet.power_on()
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error powering on:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n🟢 <b>Power on command sent.</b>\nRefresh to see updated status.',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=_back_btn(doc_id, droplet_id)
    )


def _rebuild(call: CallbackQuery, droplet: digitalocean.Droplet, doc_id: str):
    droplet_id = droplet.id
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Rebuilding VPS...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=call.message.reply_markup
    )
    try:
        droplet.load()
        droplet.rebuild()
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error rebuilding:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return
    bot.edit_message_text(
        text=(
            f'{call.message.html_text}\n\n'
            f'🔧 <b>Rebuild command sent.</b>\n'
            f'📧 New password will be sent to your DO email.\n'
            f'Refresh to see updated status.'
        ),
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=_back_btn(doc_id, droplet_id)
    )


def _reset_password(call: CallbackQuery, droplet: digitalocean.Droplet, doc_id: str):
    droplet_id = droplet.id
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n⏳ <b>Resetting root password...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=call.message.reply_markup
    )
    try:
        droplet.load()
        droplet.reset_root_password()
    except Exception as e:
        bot.edit_message_text(
            text=f'❌ Error resetting password:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return
    bot.edit_message_text(
        text=(
            f'{call.message.html_text}\n\n'
            f'🔑 <b>Password reset command sent.</b>\n'
            f'📧 New password will be sent to your DO email.'
        ),
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=_back_btn(doc_id, droplet_id)
    )

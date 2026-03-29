from os import environ
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from _bot import bot
from utils.db import AccountsDB
from utils.helpers import DIVIDER, BOT_TAG, BOT_BRAND, fmt_time

bot_name = environ.get('bot_name', 'SML Bot')


def start(d: Message):
    account_count = AccountsDB().count()
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('➕ Add Account',    callback_data='add_account'),
        InlineKeyboardButton('⚙️ Manage Accounts', callback_data='manage_accounts'),
        InlineKeyboardButton('🌐 Create VPS',      callback_data='create_droplet'),
        InlineKeyboardButton('🖥 Manage VPS',      callback_data='manage_droplets'),
    )
    markup.row(
        InlineKeyboardButton('🧪 Batch Test',  callback_data='batch_test_accounts'),
        InlineKeyboardButton('📊 My Stats',    callback_data='stats'),
    )
    markup.row(
        InlineKeyboardButton('ℹ️ About',        callback_data='about'),
    )

    t = (
        f'🔥 <b>Welcome to {bot_name}</b>\n'
        f'{DIVIDER}\n'
        f'👤 <b>Dev:</b> {BOT_TAG}\n'
        f'🏷 <b>Brand:</b> {BOT_BRAND}\n'
        f'{DIVIDER}\n'
        f'💳 <b>Linked Accounts:</b> <code>{account_count}</code>\n'
        f'🕐 <b>Time:</b> <code>{fmt_time()}</code>\n'
        f'{DIVIDER}\n'
        f'<b>Quick Commands:</b>\n'
        f'/start — Main menu\n'
        f'/add_do — Add DO account\n'
        f'/sett_do — Manage accounts\n'
        f'/bath_do — Batch test accounts\n'
        f'/add_vps — Create VPS\n'
        f'/sett_vps — Manage VPS\n'
        f'/ping — Check bot status\n'
    )
    bot.send_message(
        text=t,
        chat_id=d.from_user.id,
        parse_mode='HTML',
        reply_markup=markup
    )


def about(call):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('🔙 Back to Menu', callback_data='back_to_start'))
    t = (
        f'🔥 <b>SML Bot — DigitalOcean VPS Manager</b>\n'
        f'{DIVIDER}\n'
        f'<b>Version:</b> <code>2.0.0</code>\n'
        f'<b>Developer:</b> {BOT_TAG}\n'
        f'<b>Brand:</b> {BOT_BRAND}\n'
        f'{DIVIDER}\n'
        f'<b>Features:</b>\n'
        f'• Add & manage multiple DO accounts\n'
        f'• Create VPS with server presets\n'
        f'• Full droplet control (start/stop/reboot/rebuild)\n'
        f'• Reset root password\n'
        f'• Batch account testing & cleanup\n'
        f'• Live account balance checking\n'
        f'• Fast inline-keyboard navigation\n'
        f'{DIVIDER}\n'
        f'<i>Built with ❤️ by {BOT_BRAND}</i>\n'
    )
    bot.edit_message_text(
        text=t,
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


def back_to_start(call):
    start(call)


def stats(call):
    from utils.db import AccountsDB
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('🔙 Back to Menu', callback_data='back_to_start'))
    account_count = AccountsDB().count()
    t = (
        f'📊 <b>Bot Statistics</b>\n'
        f'{DIVIDER}\n'
        f'💳 Linked Accounts: <code>{account_count}</code>\n'
        f'🕐 Checked at: <code>{fmt_time()}</code>\n'
        f'{DIVIDER}\n'
        f'<i>{BOT_TAG} | {BOT_BRAND}</i>\n'
    )
    bot.edit_message_text(
        text=t,
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


def ping(d: Message):
    import time
    start_time = time.time()
    msg = bot.send_message(
        text='🏓 Pinging...',
        chat_id=d.from_user.id
    )
    elapsed = round((time.time() - start_time) * 1000)
    bot.edit_message_text(
        text=(
            f'🏓 <b>Pong!</b>\n'
            f'{DIVIDER}\n'
            f'⚡ Response: <code>{elapsed}ms</code>\n'
            f'✅ Bot is online\n'
            f'🕐 <code>{fmt_time()}</code>\n'
        ),
        chat_id=d.from_user.id,
        message_id=msg.message_id,
        parse_mode='HTML'
    )

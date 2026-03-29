from typing import Union
from time import sleep
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import digitalocean
from _bot import bot
from utils.db import AccountsDB
from utils.localizer import localize_region
from utils.set_root_password_script import set_root_password_script
from utils.password_generator import password_generator
from utils.helpers import DIVIDER, BOT_TAG

# ─── Server Presets ───────────────────────────────────────────────────────────
SERVER_PRESETS = [
    {
        'name': '🥉 Starter',
        'description': '1 vCPU / 1GB RAM / 25GB SSD',
        'slug': 's-1vcpu-1gb',
    },
    {
        'name': '🥈 Basic',
        'description': '1 vCPU / 2GB RAM / 50GB SSD',
        'slug': 's-1vcpu-2gb',
    },
    {
        'name': '🥇 Standard',
        'description': '2 vCPU / 2GB RAM / 60GB SSD',
        'slug': 's-2vcpu-2gb',
    },
    {
        'name': '💎 Pro',
        'description': '2 vCPU / 4GB RAM / 80GB SSD',
        'slug': 's-2vcpu-4gb',
    },
    {
        'name': '🚀 Power',
        'description': '4 vCPU / 8GB RAM / 160GB SSD',
        'slug': 's-4vcpu-8gb',
    },
    {
        'name': '⚡ Ultra',
        'description': '8 vCPU / 16GB RAM / 320GB SSD',
        'slug': 's-8vcpu-16gb',
    },
    {
        'name': '🔧 Custom',
        'description': 'Browse all available sizes',
        'slug': '__custom__',
    },
]

# ─── Per-user state ───────────────────────────────────────────────────────────
user_dict = {}

T = '🌐 <b>Create VPS</b>\n'


def _header(uid: int) -> str:
    u = user_dict.get(uid, {})
    lines = [T, DIVIDER]
    if u.get('account'):
        lines.append(f'👤 Account: <code>{u["account"]["email"]}</code>')
    if u.get('region_slug'):
        lines.append(f'🌍 Region:  <code>{localize_region(u["region_slug"])}</code>')
    if u.get('size_slug'):
        lines.append(f'📦 Size:    <code>{u["size_slug"]}</code>')
    if u.get('image_slug'):
        lines.append(f'🖥 OS:      <code>{u["image_slug"]}</code>')
    lines.append(DIVIDER)
    return '\n'.join(lines) + '\n'


# ─── Entry point ─────────────────────────────────────────────────────────────
def create_droplet(d: Union[Message, CallbackQuery], data: dict = None):
    data = data or {}
    next_func = data.get('nf', ['select_account'])[0]
    if next_func in globals():
        data.pop('nf', None)
        args = [d] + ([data] if data else [])
        globals()[next_func](*args)


# ─── Step 1: Select Account ───────────────────────────────────────────────────
def select_account(d: Union[Message, CallbackQuery]):
    accounts = AccountsDB().all()
    markup = InlineKeyboardMarkup()

    if not accounts:
        markup.row(InlineKeyboardButton('➕ Add Account', callback_data='add_account'))
        markup.row(InlineKeyboardButton('🔙 Back',        callback_data='back_to_start'))
        text = f'{T}{DIVIDER}\n❌ No accounts found. Add one first.\n{DIVIDER}\n<i>{BOT_TAG}</i>'
        _send_or_edit(d, text, markup)
        return

    for acc in accounts:
        markup.add(InlineKeyboardButton(
            f'👤 {acc["email"]}',
            callback_data=f'create_droplet?nf=select_region&doc_id={acc.doc_id}'
        ))
    markup.row(InlineKeyboardButton('🔙 Back', callback_data='back_to_start'))

    text = f'{T}{DIVIDER}\n🔽 <b>Select Account</b>\n{DIVIDER}\n<i>{BOT_TAG}</i>'
    _send_or_edit(d, text, markup)


# ─── Step 2: Select Region ────────────────────────────────────────────────────
def select_region(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    account = AccountsDB().get(doc_id=doc_id)
    user_dict[call.from_user.id] = {'account': account}

    bot.edit_message_text(
        text=f'{_header(call.from_user.id)}⏳ Fetching regions...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        regions = digitalocean.Manager(token=account['token']).get_all_regions()
    except Exception as e:
        bot.edit_message_text(
            text=f'{_header(call.from_user.id)}❌ Error fetching regions:\n<code>{e}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            localize_region(r.slug),
            callback_data=f'create_droplet?nf=select_server_preset&region={r.slug}'
        )
        for r in regions if r.available
    ]
    markup.add(*buttons)
    markup.row(InlineKeyboardButton('🔙 Back', callback_data='create_droplet'))

    bot.edit_message_text(
        text=f'{_header(call.from_user.id)}🌍 <b>Select Region</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


# ─── Step 3: Server Preset ────────────────────────────────────────────────────
def select_server_preset(call: CallbackQuery, data: dict):
    region_slug = data['region'][0]
    user_dict[call.from_user.id].update({'region_slug': region_slug})

    markup = InlineKeyboardMarkup()
    for preset in SERVER_PRESETS:
        label = f'{preset["name"]}  —  {preset["description"]}'
        if preset['slug'] == '__custom__':
            cb = f'create_droplet?nf=select_size_custom&region={region_slug}'
        else:
            cb = f'create_droplet?nf=select_os&size={preset["slug"]}'
        markup.row(InlineKeyboardButton(label, callback_data=cb))
    markup.row(InlineKeyboardButton(
        '🔙 Back',
        callback_data=f'create_droplet?nf=select_region&doc_id={user_dict[call.from_user.id]["account"].doc_id}'
    ))

    bot.edit_message_text(
        text=f'{_header(call.from_user.id)}📦 <b>Choose Server Size</b>\nPick a preset or browse custom sizes:',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


# ─── Step 3b: Custom Size (browse all) ───────────────────────────────────────
def select_size_custom(call: CallbackQuery, data: dict):
    uid = call.from_user.id
    if uid not in user_dict:
        user_dict[uid] = {}
    region_slug = data.get('region', [user_dict[uid].get('region_slug')])[0]
    user_dict[uid].update({'region_slug': region_slug})

    bot.edit_message_text(
        text=f'{_header(uid)}⏳ Fetching available sizes...',
        chat_id=uid,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        sizes = digitalocean.Manager(
            token=user_dict[uid]['account']['token']
        ).get_all_sizes()
    except Exception as e:
        bot.edit_message_text(
            text=f'{_header(uid)}❌ Error fetching sizes:\n<code>{e}</code>',
            chat_id=uid,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            f'{s.slug} (${s.price_monthly}/mo)',
            callback_data=f'create_droplet?nf=select_os&size={s.slug}'
        )
        for s in sizes if region_slug in s.regions
    ]
    markup.add(*buttons)
    markup.row(InlineKeyboardButton(
        '🔙 Back to Presets',
        callback_data=f'create_droplet?nf=select_server_preset&region={region_slug}'
    ))

    bot.edit_message_text(
        text=f'{_header(uid)}📦 <b>Select Custom Size</b>',
        chat_id=uid,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


# ─── Step 4: Select OS ───────────────────────────────────────────────────────
def select_os(d: Union[Message, CallbackQuery], data: dict):
    size_slug = data['size'][0]
    user_dict[d.from_user.id].update({'size_slug': size_slug})

    uid = d.from_user.id
    region_slug = user_dict[uid]['region_slug']

    def fetch_markup():
        try:
            images = digitalocean.Manager(
                token=user_dict[uid]['account']['token']
            ).get_distro_images()
        except Exception as e:
            return None, str(e)

        markup = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton(
                f'{img.distribution} {img.name}',
                callback_data=f'create_droplet?nf=get_name&image={img.slug}'
            )
            for img in images
            if img.distribution in ['Ubuntu', 'CentOS', 'Debian', 'Fedora']
            and img.public
            and img.status == 'available'
            and region_slug in img.regions
        ]
        markup.add(*buttons)
        markup.row(InlineKeyboardButton(
            '🔙 Back to Presets',
            callback_data=f'create_droplet?nf=select_server_preset&region={region_slug}'
        ))
        return markup, None

    loading_text = f'{_header(uid)}⏳ Fetching OS list...'
    if isinstance(d, Message):
        msg = bot.send_message(text=loading_text, chat_id=uid, parse_mode='HTML')
        markup, err = fetch_markup()
        mid = msg.message_id
    else:
        bot.edit_message_text(text=loading_text, chat_id=uid,
                              message_id=d.message.message_id, parse_mode='HTML')
        markup, err = fetch_markup()
        mid = d.message.message_id

    if err:
        bot.edit_message_text(text=f'{_header(uid)}❌ Error fetching OS:\n<code>{err}</code>',
                              chat_id=uid, message_id=mid, parse_mode='HTML')
        return

    bot.edit_message_text(
        text=f'{_header(uid)}🖥 <b>Select Operating System</b>',
        chat_id=uid, message_id=mid,
        parse_mode='HTML', reply_markup=markup
    )


# ─── Step 5: Get Name ────────────────────────────────────────────────────────
def get_name(call: CallbackQuery, data: dict):
    image_slug = data['image'][0]
    user_dict[call.from_user.id].update({'image_slug': image_slug})
    uid = call.from_user.id

    msg = bot.edit_message_text(
        text=(
            f'{_header(uid)}'
            f'📝 <b>Enter Instance Name</b>\n'
            f'Example: <code>SMLServer-01</code>\n\n'
            f'/back — Go back'
        ),
        chat_id=uid,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg, ask_create)


# ─── Step 6: Confirm ─────────────────────────────────────────────────────────
def ask_create(m: Message):
    uid = m.from_user.id
    if m.text == '/back':
        select_os(m, data={'size': [user_dict[uid]['size_slug']]})
        return

    droplet_name = m.text.strip()
    user_dict[uid]['droplet_name'] = droplet_name

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('✅ Confirm & Create', callback_data=f'create_droplet?nf=confirm_create&name={droplet_name}'),
    )
    markup.row(
        InlineKeyboardButton('⬅️ Back',  callback_data=f'create_droplet?nf=get_name&image={user_dict[uid]["image_slug"]}'),
        InlineKeyboardButton('❌ Cancel', callback_data='create_droplet?nf=cancel_create'),
    )

    bot.send_message(
        text=(
            f'{_header(uid)}'
            f'🏷 Name: <code>{droplet_name}</code>\n\n'
            f'Ready to create your VPS. Confirm?'
        ),
        chat_id=uid,
        parse_mode='HTML',
        reply_markup=markup
    )


def cancel_create(call: CallbackQuery):
    uid = call.from_user.id
    user_dict.pop(uid, None)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('🔙 Main Menu', callback_data='back_to_start'))
    bot.edit_message_text(
        text=f'❌ <b>VPS creation cancelled.</b>',
        chat_id=uid,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


# ─── Step 7: Create ──────────────────────────────────────────────────────────
def confirm_create(call: CallbackQuery, data: dict):
    uid = call.from_user.id
    droplet_name = data['name'][0]
    password = password_generator()

    bot.edit_message_text(
        text=f'{_header(uid)}⏳ <b>Creating VPS, please wait...</b>\nThis may take 1–2 minutes.',
        chat_id=uid,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        droplet = digitalocean.Droplet(
            token=user_dict[uid]['account']['token'],
            name=droplet_name,
            region=user_dict[uid]['region_slug'],
            image=user_dict[uid]['image_slug'],
            size_slug=user_dict[uid]['size_slug'],
            user_data=set_root_password_script(password)
        )
        droplet.create()

        for action in droplet.get_actions():
            while action.status != 'completed':
                sleep(3)
                action.load()

        droplet.load()
        while not droplet.ip_address:
            sleep(3)
            droplet.load()

    except Exception as e:
        bot.edit_message_text(
            text=f'{_header(uid)}❌ <b>Error creating VPS:</b>\n<code>{e}</code>',
            chat_id=uid,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        user_dict.pop(uid, None)
        return

    doc_id = user_dict[uid]['account'].doc_id
    user_dict.pop(uid, None)

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        '🔍 View Details',
        callback_data=f'droplet_detail?doc_id={doc_id}&droplet_id={droplet.id}'
    ))
    markup.row(InlineKeyboardButton('🔙 Main Menu', callback_data='back_to_start'))

    bot.edit_message_text(
        text=(
            f'✅ <b>VPS Created Successfully!</b>\n'
            f'{DIVIDER}\n'
            f'🏷 Name:     <code>{droplet.name}</code>\n'
            f'🌐 IP:       <code>{droplet.ip_address}</code>\n'
            f'🔑 Password: <code>{password}</code>\n'
            f'📦 Size:     <code>{droplet.size_slug}</code>\n'
            f'🌍 Region:   <code>{localize_region(droplet.region["slug"])}</code>\n'
            f'🖥 OS:       <code>{droplet.image["distribution"]} {droplet.image["name"]}</code>\n'
            f'{DIVIDER}\n'
            f'<b>SSH:</b> <code>ssh root@{droplet.ip_address}</code>\n'
            f'{DIVIDER}\n'
            f'<i>{BOT_TAG}</i>'
        ),
        chat_id=uid,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


# ─── Helper ───────────────────────────────────────────────────────────────────
def _send_or_edit(d, text, markup):
    if isinstance(d, CallbackQuery):
        bot.edit_message_text(text=text, chat_id=d.from_user.id,
                              message_id=d.message.message_id,
                              parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(text=text, chat_id=d.from_user.id,
                         parse_mode='HTML', reply_markup=markup)

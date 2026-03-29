<div align="center">

# 🔥 SML Bot — DigitalOcean VPS Manager

**A Telegram bot to manage your DigitalOcean VPS instances — right from your phone.**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://python.org)
[![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-3.8.2-blue?style=flat-square)](https://github.com/eternnoir/pyTelegramBotAPI)
[![DigitalOcean](https://img.shields.io/badge/DigitalOcean-API-0080FF?style=flat-square&logo=digitalocean)](https://digitalocean.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📌 Credits & Attribution

> **Original bot logic, architecture, and core implementation by:**
> **[FighterTunnel](https://github.com/FighterTunnel/DigitalOcean-TeleBot)** — all credit goes to him for the original work. 🙏
>
> This fork is a **community contribution** by **[SML The Unknown (@codeninjaxd)](https://t.me/codeninjaxd)**.
> My contribution was purely:
> - 🌐 **Translating** the entire codebase from Indonesian → English
> - 🔤 **Internationalizing** all UI text, button labels, status messages, and error strings
> - 🏷 **Rebranding** to SML Bot cosmetics (icons, dividers, consistent formatting)
> - ✨ **Adding a few QoL features** (server presets, confirm dialogs, ping command, about panel)
> - 📝 **Writing this README** because the original didn't have one in English 😄
>
> If you find this useful, go star the **original repo** first. That's where the real work happened.

---

## 🤔 What Is This?

A Telegram bot that acts as a full control panel for your [DigitalOcean](https://digitalocean.com) account. No web browser needed — create VPS servers, manage them, check balances, reset passwords, all from Telegram inline keyboards.

Think of it as a lightweight CLI for DigitalOcean, but your mom could use it.

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 💳 | Multi-Account | Link multiple DigitalOcean accounts |
| 🌐 | Create VPS | Wizard with **Server Presets** or full custom size browser |
| 🖥 | Manage VPS | Start, stop, reboot, rebuild, delete — all inline |
| 🔑 | Reset Password | Reset root password on any droplet |
| 🧪 | Batch Test | Test all accounts in one tap, auto-clean invalid tokens |
| 💰 | Balance Check | Live balance & monthly usage per account |
| 🔒 | Admin Lock | Bot restricted to whitelisted Telegram user IDs |
| ⚡ | /ping | Check bot response latency |
| 📊 | Stats Panel | Quick overview from the main menu |
| 🗑 | Safe Delete | Confirm dialogs before any destructive action |

---

## 📦 Server Presets

When creating a VPS you can pick a preset or browse every available size on your account:

| Preset | Spec | Typical Use |
|---|---|---|
| 🥉 Starter | 1 vCPU / 1 GB RAM / 25 GB SSD | Light proxies, tunnels |
| 🥈 Basic | 1 vCPU / 2 GB RAM / 50 GB SSD | Small apps |
| 🥇 Standard | 2 vCPU / 2 GB RAM / 60 GB SSD | Medium workloads |
| 💎 Pro | 2 vCPU / 4 GB RAM / 80 GB SSD | Production apps |
| 🚀 Power | 4 vCPU / 8 GB RAM / 160 GB SSD | Heavy workloads |
| ⚡ Ultra | 8 vCPU / 16 GB RAM / 320 GB SSD | Serious stuff |
| 🔧 Custom | All available sizes | You know what you're doing |

---

## 🚀 Deploy Guide

### Option A — One-liner install (recommended for VPS)

SSH into your server and run:

```bash
bash <(curl -s https://raw.githubusercontent.com/codeninjaxd/SML-Bot/main/start)
```

It will ask for your bot token, admin Telegram ID, and store name — then handle everything else automatically.

---

### Option B — Manual install

**Step 1 — Clone the repo**

```bash
git clone https://github.com/codeninjaxd/SML-Bot.git
cd SML-Bot
```

**Step 2 — Install dependencies**

```bash
pip3 install -r requirements.txt
```

**Step 3 — Configure the bot**

Edit `config.json`:

```json
{
  "BOT": {
    "NAME": "My Store",
    "TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
    "ADMINS": [123456789]
  }
}
```

| Key | Description |
|---|---|
| `NAME` | Bot display name shown in the welcome message |
| `TOKEN` | Get from [@BotFather](https://t.me/BotFather) on Telegram |
| `ADMINS` | Array of Telegram user IDs allowed to use the bot |

> Don't know your Telegram user ID? Message [@userinfobot](https://t.me/userinfobot).

**Step 4 — Run it**

```bash
python3 main.py
```

---

### Option C — Run as a systemd service (so it survives reboots)

The `start` script does this automatically, but if you set it up manually:

```bash
# Create the service file
nano /etc/systemd/system/smlbot.service
```

Paste this:

```ini
[Unit]
Description=SML Bot — DigitalOcean VPS Manager
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/SML-Bot/main.py
WorkingDirectory=/root/SML-Bot
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
```

Then enable and start:

```bash
systemctl daemon-reload
systemctl enable smlbot
systemctl start smlbot
```

---

## 🛠 Useful Commands (after systemd install)

```bash
# Live logs
journalctl -u smlbot -f

# Check status
systemctl status smlbot

# Restart
systemctl restart smlbot

# Stop
systemctl stop smlbot
```

---

## 📋 Requirements

- Python 3.7+
- Linux — Ubuntu / Debian / CentOS / AlmaLinux (Windows untested, probably fine)
- A Telegram Bot Token → [@BotFather](https://t.me/BotFather)
- A DigitalOcean API Token → [Generate here](https://cloud.digitalocean.com/account/api/tokens)

---

## 📁 Project Structure

```
SML-Bot/
├── main.py                           # Entry point — loads config, starts polling
├── bot.py                            # Message & callback query router
├── _bot.py                           # Telebot instance singleton
├── config.json                       # Your bot token, admin IDs, display name
├── requirements.txt
├── start                             # One-click install + systemd setup script
│
├── modules/
│   ├── start.py                      # /start menu, /ping, stats, about
│   ├── add_account.py                # Add DO accounts (bulk paste supported)
│   ├── manage_accounts.py            # Account list
│   ├── account_detail.py             # Account info + live balance
│   ├── delete_account.py             # Delete account (with confirm step)
│   ├── batch_test_accounts.py        # Test all accounts at once
│   ├── batch_test_delete_accounts.py # Auto-remove invalid accounts
│   ├── manage_droplets.py            # VPS manager entry screen
│   ├── create_droplet.py             # Full VPS creation wizard + presets
│   ├── list_droplets.py              # Droplet list per account
│   ├── droplet_detail.py             # Full droplet info panel
│   └── droplet_actions.py            # Delete / shutdown / reboot / rebuild / etc.
│
└── utils/
    ├── db.py                         # TinyDB wrapper (AccountsDB)
    ├── localizer.py                  # Region slugs → readable names + flags
    ├── password_generator.py         # Strong random password generator
    ├── set_root_password_script.py   # Cloud-init script to enable root SSH
    └── helpers.py                    # Shared branding constants & formatters
```

---

## 💬 Bot Commands

| Command | What it does |
|---|---|
| `/start` | Open main menu |
| `/add_do` | Add a DigitalOcean account |
| `/sett_do` | Manage linked accounts |
| `/bath_do` | Batch test all accounts |
| `/add_vps` | Create a new VPS |
| `/sett_vps` | Manage existing VPS |
| `/ping` | Check bot response time |

---

## ⚠️ Disclaimer

This is an unofficial tool. It is not affiliated with or endorsed by DigitalOcean.
Use at your own risk. Don't deploy this on a public server without proper access controls.

---

<div align="center">

**Original work by [FighterTunnel](https://github.com/FighterTunnel/DigitalOcean-TeleBot)** — go give that repo a ⭐

**Translated & contributed by [@codeninjaxd](https://t.me/codeninjaxd) — SML The Unknown**

</div>

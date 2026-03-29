<div align="center">

# 🔥 Digital Ocean Manager Bot

**Manage your DigitalOcean VPS instances directly from Telegram.**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://python.org)
[![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-3.8.2-blue?style=flat-square)](https://github.com/eternnoir/pyTelegramBotAPI)
[![DigitalOcean](https://img.shields.io/badge/DigitalOcean-API-0080FF?style=flat-square&logo=digitalocean)](https://digitalocean.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 🙏 Original Author

> **All core logic, architecture, and original implementation belongs to:**
>
> ### [FighterTunnel](https://github.com/FighterTunnel/DigitalOcean-TeleBot) ⭐
>
> Please go **star his repository** — that's where the real work was done.
> This repo would not exist without him.

---

## 👋 About This Fork

This is a community fork maintained by **[PmOfBangladesh](https://github.com/PmOfBangladesh)** — also known as **SML The Unknown** (`@codeninjaxd` on Telegram).

My contributions to this fork:

- 🌐 **Translated** the entire codebase from Indonesian → English
- 🔤 **Internationalized** all UI text, button labels, status messages and error strings
- ✨ **Added QoL features** — server presets, confirm dialogs before destructive actions, `/ping` command, about panel, stats screen
- 🏷 **Consistent formatting** — icons, dividers, branding throughout all screens
- 📝 **Wrote this README** because the original didn't have one in English 😄

I didn't reinvent the wheel — I just made it readable for the rest of the world.

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 💳 | Multi-Account | Link multiple DigitalOcean accounts |
| 🌐 | Create VPS | Wizard with **Server Presets** or full custom size browser |
| 🖥 | Manage VPS | Start, stop, reboot, rebuild, delete — all from inline keyboard |
| 🔑 | Reset Password | Reset root password on any droplet |
| 🧪 | Batch Test | Test all accounts in one tap, auto-clean invalid tokens |
| 💰 | Balance Check | Live balance & monthly usage per account |
| 🔒 | Admin Lock | Bot restricted to whitelisted Telegram user IDs |
| ⚡ | /ping | Check bot response latency |
| 📊 | Stats Panel | Quick overview from the main menu |
| 🗑 | Safe Delete | Confirm dialogs before any destructive action |

---

## 📦 Server Presets

| Preset | Spec |
|---|---|
| 🥉 Starter | 1 vCPU / 1 GB RAM / 25 GB SSD |
| 🥈 Basic | 1 vCPU / 2 GB RAM / 50 GB SSD |
| 🥇 Standard | 2 vCPU / 2 GB RAM / 60 GB SSD |
| 💎 Pro | 2 vCPU / 4 GB RAM / 80 GB SSD |
| 🚀 Power | 4 vCPU / 8 GB RAM / 160 GB SSD |
| ⚡ Ultra | 8 vCPU / 16 GB RAM / 320 GB SSD |
| 🔧 Custom | Browse all available sizes on your account |

---

## 🚀 Deploy Guide

### Option A — One-liner (recommended)

SSH into your Linux server and run:

```bash
bash <(curl -s https://raw.githubusercontent.com/PmOfBangladesh/Digital-Ocean-Manager/main/start)
```

The script will prompt for your bot token, admin Telegram ID, and store name — then handle everything automatically including systemd setup.

---

### Option B — Manual

**1. Clone**

```bash
git clone https://github.com/PmOfBangladesh/Digital-Ocean-Manager.git
cd Digital-Ocean-Manager
```

**2. Install dependencies**

```bash
pip3 install -r requirements.txt
```

**3. Configure**

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
| `NAME` | Display name shown in the welcome message |
| `TOKEN` | Get from [@BotFather](https://t.me/BotFather) |
| `ADMINS` | Your Telegram user ID — get it from [@userinfobot](https://t.me/userinfobot) |

**4. Run**

```bash
python3 main.py
```

---

### Option C — Systemd Service (run on boot, auto-restart)

```bash
nano /etc/systemd/system/smlbot.service
```

Paste:

```ini
[Unit]
Description=Digital Ocean Manager Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/Digital-Ocean-Manager/main.py
WorkingDirectory=/root/Digital-Ocean-Manager
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl daemon-reload
systemctl enable smlbot
systemctl start smlbot
```

**Useful commands:**

```bash
journalctl -u smlbot -f       # Live logs
systemctl status smlbot        # Check status
systemctl restart smlbot       # Restart
systemctl stop smlbot          # Stop
```

---

## 💬 Bot Commands

| Command | Description |
|---|---|
| `/start` | Open main menu |
| `/add_do` | Add a DigitalOcean account |
| `/sett_do` | Manage linked accounts |
| `/bath_do` | Batch test all accounts |
| `/add_vps` | Create a new VPS |
| `/sett_vps` | Manage existing VPS |
| `/ping` | Check bot response time |

---

## 📋 Requirements

- Python 3.7+
- Linux — Ubuntu / Debian / CentOS / AlmaLinux
- Telegram Bot Token → [@BotFather](https://t.me/BotFather)
- DigitalOcean API Token → [Generate here](https://cloud.digitalocean.com/account/api/tokens)

---

## ⚠️ Disclaimer

Unofficial tool. Not affiliated with or endorsed by DigitalOcean in any way.

---

<div align="center">

### Original work by [FighterTunnel](https://github.com/FighterTunnel/DigitalOcean-TeleBot) — please go ⭐ his repo

Translated & maintained by [PmOfBangladesh](https://github.com/PmOfBangladesh) · SML The Unknown · [@codeninjaxd](https://t.me/codeninjaxd)

</div>

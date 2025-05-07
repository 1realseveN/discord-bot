# main.py

import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# === .env-Datei laden ===
load_dotenv()

# === Webserver für UptimeRobot ===
app = Flask('')


@app.route('/')
def home():
    return "✅ Bot ist aktiv!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    thread = Thread(target=run)
    thread.start()


# === Discord-Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === ENV Variablen ===
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
IMAGE_URL = os.getenv("IMAGE_URL")
IMAGE_URL_2 = os.getenv("IMAGE_URL_2")

# === Scheduler: jeden Freitag 12:00 Uhr (Berlin-Zeit)
scheduler = AsyncIOScheduler()


@bot.event
async def on_ready():
    print(f"✅ Eingeloggt als {bot.user}")
    scheduler.add_job(send_friday_image,
                      'cron',
                      day_of_week='fri',
                      hour=12,
                      minute=0,
                      timezone='Europe/Berlin')
    scheduler.add_job(send_monday_image,
                      'cron',
                      day_of_week='mon',
                      hour=12,
                      minute=0,
                      timezone='Europe/Berlin')
    scheduler.start()


@bot.command()
async def freitag(ctx):
    await ctx.send(IMAGE_URL)

@bot.command()
async def montag(ctx):
    await ctx.send(IMAGE_URL_2)


async def send_friday_image():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(IMAGE_URL)
    else:
        print("⚠️ Channel nicht gefunden.")

async def send_monday_image():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(IMAGE_URL_2)
    else:
        print("⚠️ Channel nicht gefunden.")


# === Bot starten
keep_alive()
bot.run(TOKEN)

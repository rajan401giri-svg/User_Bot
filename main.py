from pyrogram import Client, filters
import json
import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

DB_FILE = "settings.json"

DEFAULT = {
    "offline": False,
    "message": "Antidote abhi offline hai.\nhttps://antidote69.lovable.app"
}

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump(DEFAULT, f)

def load_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

app = Client(
    "antidote",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

@app.on_message(filters.me & filters.command("off"))
async def off_cmd(_, message):
    data = load_data()
    data["offline"] = True
    save_data(data)
    await message.edit("✅ Offline Mode ON")

@app.on_message(filters.me & filters.command("on"))
async def on_cmd(_, message):
    data = load_data()
    data["offline"] = False
    save_data(data)
    await message.edit("✅ Offline Mode OFF")

@app.on_message(filters.me & filters.command("setoff"))
async def setoff_cmd(_, message):
    parts = message.text.split(None, 1)

    if len(parts) < 2:
        return await message.edit("Usage: /setoff your message")

    data = load_data()
    data["message"] = parts[1]
    save_data(data)

    await message.edit("✅ Offline message updated")

@app.on_message(filters.me & filters.command("cmd"))
async def cmd_cmd(_, message):
    await message.edit(
        "📋 Commands\n\n"
        "/off\n"
        "/on\n"
        "/setoff <message>\n"
        "/id\n"
        "/cmd"
    )

@app.on_message(filters.me & filters.command("id"))
async def id_cmd(_, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
        await message.reply_text(
            f"👤 Name: {user.first_name}\n🆔 ID: `{user.id}`"
        )
    else:
        await message.reply_text(
            f"🆔 Your ID: `{message.from_user.id}`"
        )

@app.on_message(filters.private & ~filters.me)
async def private_auto_reply(_, message):
    data = load_data()

    if data["offline"]:
        await message.reply_text(data["message"])

@app.on_message(filters.group & ~filters.me)
async def group_auto_reply(_, message):
    data = load_data()

    if not data["offline"]:
        return

    if (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.is_self
    ):
        await message.reply_text(data["message"])

app.run()

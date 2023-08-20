from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Poll,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)


api_id: int = 23918516
api_hash: str = "44394f47035ffb390840eb9e3c807751"
token: str = "6305195627:AAGfDKooO2HpySalgVwCSjErY6OGV43h23k"


app = Client('viewcounterbot', in_memory=True, api_id=api_id, api_hash=api_hash, bot_token=token)

non_anonymous_poll = filters.create(
    lambda *_: _[2].poll is not None and not _[2].poll.is_anonymous
)

forwardchannel = -1000000000000
startmsg: str = """
start message
"""


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply(
        startmsg,
    )


@app.on_message(
    ~filters.service
    & ~filters.game
    & ~filters.channel
    & ~filters.linked_channel
    & ~non_anonymous_poll
)
async def viewcounter(client, message):
    forward = await message.forward(forwardchannel)
    await forward.forward(message.chat.id)
    await forward.delete()


@app.on_message(
    (filters.service | filters.game | filters.channel | non_anonymous_poll)
)
async def notsupported(client, message):
    await message.reply(
        "sorry but this type of message not supported (non anonymous polls or games (like @gamebot or @gamee) or message from channels or service messages)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("delete this message", "deleterrormessage")]]
        ),
    )


@app.on_callback_query(filters.regex("^deleterrormessage"))
async def delerrmsg(client: app, cquery: CallbackQuery):
    await cquery.message.delete()


app.run()

from telethon.tl.types import MessageMediaWebPage
from config import bot, auth_users
from telethon import events, Button
from telethon.tl.types import MessageMediaPhoto

ad = "NULL"
link_preview = False
bs = []
media = None

@bot.on(events.InlineQuery)
async def handler(event):
    if event.chat_id not in auth_users:
        return
    builder = event.builder
    options = []
    if media == None or type(media) == MessageMediaWebPage:
        options.append(
            builder.article(
                title = ad, 
                text = ad, 
                link_preview = link_preview,
                buttons=bs
            )
        )
    elif type(media) == MessageMediaPhoto:
        options.append(
            builder.photo(
                text = ad, 
                link_preview = link_preview,
                file = media,
                buttons=bs
            )
        )
    else:
        options.append(
            builder.document(
                title = ad, 
                text = ad, 
                link_preview = link_preview,
                file = media,
                buttons=bs
            )
        )
    await event.answer(options)

@bot.on(events.NewMessage(pattern="/setadd"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    reply = await event.get_reply_message()
    global ad
    global media
    ad = reply.text
    media = reply.media
    await reply.reply("set as current ad")

@bot.on(events.NewMessage(pattern="/link_preview"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    global link_preview
    link_preview = True if "true" in event.text or "True" in event.text else False
    await event.reply(f"Link Preview is set to: {link_preview}")

@bot.on(events.NewMessage(pattern="/setbutton"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    global bs
    try:
        b1 = event.text.split("|")[1]
        b2 = event.text.split("|")[2]
        bs = [[Button.url(text=b1, url=b2)]]
        await event.reply(f"Button Text: {b1}\nButton URL: {b2}")
    except:
        bs = []
        await event.reply(f"Button Removed")

@bot.on(events.NewMessage(pattern="/addbutton"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    global bs
    try:
        b1 = event.text.split("|")[1]
        b2 = event.text.split("|")[2]
        bs.append([Button.url(text=b1, url=b2)])
        await event.reply(f"Button Text: {b1}\nButton URL: {b2}")

    except:
        await event.reply("Error, check format")


@bot.on(events.NewMessage(pattern="/resetad"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    global ad, bs, link_preview, media
    ad = "NULL"
    link_preview = False
    bs = None
    media = None
    await event.reply("Reset Successful")

bot.start()

bot.run_until_disconnected()

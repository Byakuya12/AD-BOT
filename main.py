from config import bot, auth_users
from telethon import events, Button

ad = "NULL"
link_preview = False
bs = None

@bot.on(events.InlineQuery)
async def handler(event):
    if event.chat_id not in auth_users:
        return
    builder = event.builder
    options = []
    if bs == None:
        options.append(
            builder.article(
                title = ad, 
                text = ad, 
                link_preview = link_preview,
            )
        )
    else:
        options.append(
            builder.article(
                title = ad, 
                text = ad, 
                link_preview = link_preview,
                buttons=Button.url(
                    text=bs[0], 
                    url=bs[1]
                )
            )
        )
    await event.answer(options)

@bot.on(events.NewMessage(pattern="/setadd"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    reply = await event.get_reply_message()
    global ad
    ad = reply.text
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
        bs = [event.text.split("|")[1], event.text.split("|")[2]]
        await event.reply(f"Button Text: {bs[0]}\nButton URL: {bs[1]}")
    except:
        bs = None
        await event.reply(f"Button Removed")

@bot.on(events.NewMessage(pattern="/resetad"))
async def _(event):
    if event.sender_id not in auth_users:
        return
    global ad, bs, link_preview
    ad = "NULL"
    link_preview = False
    bs = None
    await event.reply("Reset Successful")

bot.start()

bot.run_until_disconnected()

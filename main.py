from pyrogram import Client, Filters
import os, shutil
from creds import my
from telegraph import upload_file

TGraph = Client(
    "Image upload bot",
    bot_token = my.BOT_TOKEN,
    api_id = my.API_ID,
    api_hash = my.API_HASH
)


@TGraph.on_message(Filters.command("start"))
async def start(client, message):
    await message.reply_text(f"Hello {message.from_user.first_name},\nI'm telegram to telegra.ph image uploader bot by @filimhouseadmin \n Press /help for assistance", True)
    
@TGraph.on_message(Filters.command("channel"))
async def start(client, message):
    await message.reply_text(f"These are our channels under @filimhouse: \n@FH_SOUTH\n@FH_HEVC\n@FH_OLD\n@FH_NEW\n@FH_DUBBED\n@FH_WORLD", True)
    
@TGraph.on_message(Filters.command("help"))
async def start(client, message):
    await message.reply_text(f"Just send me any photos here , and i will upload it to telegra.ph and forwards you its corresponding link \nEnjoy!!", True)
    
@TGraph.on_message(Filters.photo)
async def getimage(client, message):
    tmp = os.path.join("downloads",str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    imgdir = tmp + "/" + str(message.message_id) +".jpg"
    dwn = await message.reply_text("Downloading...", True)          
    await client.download_media(
            message=message,
            file_name=imgdir
        )
    await dwn.edit_text("Uploading...")
    try:
        response = upload_file(imgdir)
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(f"https://telegra.ph{response[0]}")
    shutil.rmtree(tmp,ignore_errors=True)


TGraph.run()

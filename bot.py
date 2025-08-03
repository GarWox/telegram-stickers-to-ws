#!/usr/bin/env python3

import os
import re
import asyncio
import logging
import zipfile
import time
from dotenv import load_dotenv
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName, InputStickerSetID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
allowed_extensions = ["webp", "jpg", "png", "tgs"]

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "", name)
 
# Download every sticker from the pack
async def download_sticker(sticker, folder, pack_name, index):
    try:
        await asyncio.sleep(0.5)
        await client.download_media(sticker, file=os.path.join(folder, f"{pack_name}{index+1}.webp"))
    except Exception as e:
        raise e

async def get_thumb(sticker, folder, pack_name):
    try: 
        await client.download_media(sticker, file=os.path.join(folder, f"{pack_name}.png"))
    except:
        pass

async def sticker_handler(update: Update, context):
    sticker = update.message.sticker

    pack_name = sanitize_filename(sticker.set_name.replace(" ", "_"))
    folder = f"stickers/{pack_name}"
    os.makedirs(folder, exist_ok=True)
 
    print(f"Downloading: {pack_name}...")

    try:    
        sticker_set = await client(GetStickerSetRequest(stickerset=InputStickerSetShortName(short_name=sticker.set_name), hash=0))
        process = [download_sticker(sticker, folder, pack_name, i) for i, sticker in enumerate(sticker_set.documents)]
        await asyncio.gather(*process)
        await get_thumb(sticker_set.documents[0], folder, pack_name)
        print("Successful download")
    except Exception as e:
        print(f"Error downloading: {e}")
    
    # Resizing images
    try:
        image=os.path.join(folder,f"{pack_name}.png")
        resized_image = Image.open(image).convert("RGBA")
        resized_image = resized_image.resize((96,96))
        resized_image.save(image, "PNG")
    except:
        pass

    for i in range(len(sticker_set.documents)):
        for ext in allowed_extensions:
            try:
                image=os.path.join(folder, f"{i+1}.{ext}")
                resized_image = Image.open(image).convert("RGBA")
                resized_image = resized_image.resize((512,512))
                resized_image.save(image, "WEBP")
            except Exception as e:
                pass
    
    # Creating .wastickers files
    i = 0
    while i <= 120:

        sticker = os.path.join(folder, f"{pack_name}{i+1}.webp") or os.path.join(folder, f"{pack_name}{i+1}.tgs")

        if os.path.isfile(sticker):
            try:
                arcname = os.path.basename(sticker)
                if i < 30:
                    with zipfile.ZipFile(f"{folder}/{pack_name}.wastickers", mode="a") as archive:
                        archive.write(sticker, arcname=arcname)    
                elif i < 60:
                    with zipfile.ZipFile(f"{folder}/{pack_name}_part2.wastickers", mode="a") as archive2:
                        archive2.write(sticker, arcname=arcname)
                elif i < 90:
                    with zipfile.ZipFile(f"{folder}/{pack_name}_part3.wastickers", mode="a") as archive3:
                        archive3.write(sticker, arcname=arcname)
                elif i < 120:
                    with zipfile.ZipFile(f"{folder}/{pack_name}_part4.wastickers", mode="a") as archive4:
                        archive4.write(sticker, arcname=arcname)
            except:
                pass
            
        else:
            print("All files zipped")
            break
        
        i += 1
 
    #title
    with open(f"{folder}/title.txt", "w", encoding="utf-8") as archive_title:
        archive_title.write(f"{pack_name}")

    #author
    with open(f"{folder}/author.txt", "w", encoding="utf-8") as archive_author:
        archive_author.write("yo")

    # Adding title, author, thumbnail to file.wastickers
    pack1 = os.path.join(folder, f"{pack_name}.wastickers")
    if os.path.isfile(pack1):

        with zipfile.ZipFile(pack1, mode="a") as archive:
            archive.write(f"{folder}/title.txt", arcname="title.txt")
            archive.write(f"{folder}/author.txt", arcname="author.txt")
            archive.write(f"{folder}/{pack_name}.png", arcname=f"{pack_name}.png")
        #sending file.wastickers
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(pack1, 'rb'))

    pack2 = os.path.join(folder, f"{pack_name}_part2.wastickers")
    if os.path.isfile(pack2): 

        with zipfile.ZipFile(pack2, mode="a") as archive:
            archive.write(f"{folder}/title.txt", arcname="title.txt")
            archive.write(f"{folder}/author.txt", arcname="author.txt")
            archive.write(f"{folder}/{pack_name}.png", arcname=f"{pack_name}.png")

        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(pack2, 'rb'))

    pack3 = os.path.join(folder, f"{pack_name}_part3.wastickers")
    if os.path.isfile(pack3):
        with zipfile.ZipFile(pack3, mode="a") as archive:
            archive.write(f"{folder}/title.txt", arcname="title.txt")
            archive.write(f"{folder}/author.txt", arcname="author.txt")
            archive.write(f"{folder}/{pack_name}.png", arcname=f"{pack_name}.png")

        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(pack3, 'rb'))

    pack4 = os.path.join(folder, f"{pack_name}_part4.wastickers")  
    if os.path.isfile(pack4):

        with zipfile.ZipFile(pack4, mode="a") as archive:
            archive.write(f"{folder}/title.txt", arcname="title.txt")
            archive.write(f"{folder}/author.txt", arcname="author.txt")
            archive.write(f"{folder}/{pack_name}.png", arcname=f"{pack_name}.png")

        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(pack4, 'rb'))

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    
    application.add_handler(MessageHandler(filters.Sticker.ALL, sticker_handler))
    application.run_polling(drop_pending_updates=True)






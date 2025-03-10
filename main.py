# (C) @CodeXBots

import os, time, math, json
import string, random, traceback
import asyncio, datetime, aiofiles
import requests, aiohttp
from random import choice 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import *
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from database import Database
from config import API_HASH, API_ID, BOT_TOKEN, UPDATE_CHANNEL, BOT_OWNER, DATABASE_URL, AUTH_CHANNEL
db = Database(DATABASE_URL, "mediatourl")

Bot = Client(
    "Media To Url Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH,
)

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=chat.invite_link)]) #✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇
        except Exception as e:
            pass
    return btn
	
START_TEXT = """**{},

ɪ ᴀᴍ ᴍᴇᴅɪᴀ ᴛᴏ ᴜʀʟ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ. 

ɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴀɴʏ ᴍᴇᴅɪᴀ (ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ) ᴜɴᴅᴇʀ 15ᴍʙ.

Dᴏɴ'ᴛ wᴏʀʀʏ Iғ ʏᴏᴜ wᴀɴᴛ ᴛᴏ lɪɴᴋ fɪʟᴇs fʀᴏᴍ 16 MB ᴛᴏ 5 GB ᴛʜᴇɴ ʏᴏᴜ cᴀɴ ᴜsᴇ ➠ <a href='https://t.me/File_To_Link_Prime_Bot'>Fɪʟᴇ Tᴏ Lɪɴᴋ Pʀɪᴍᴇ Bᴏᴛ 🔗</a>

<blockquote> 🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ  <a href='https://t.me/Prime_Botz'>ᴘʀɪᴍᴇ ʙᴏᴛz 🔥</a>**</blockquote>"""

ABOUT_TEXT = """**{},

🤖 ɪ ᴀᴍ [ᴍᴇᴅɪᴀ ᴛᴏ ᴜʀʟ ʙᴏᴛ](https://t.me/iMg_To_URL_Prime_Bot)
👨‍💻 ᴍʏ ᴄʀᴇᴀᴛᴏʀ : <a href="https://telegram.me/Prime_Nayem">ᴍʀ.ᴘʀɪᴍᴇ</a>
🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href="https://t.me/Prime_Botz">ᴘʀɪᴍᴇ ʙᴏᴛz</a>
⚙️ ᴄʜɪʟʟɪɴɢ ᴏɴ : <a href="https://www.heroku.com/">ʜᴇʀᴏᴋᴜ</a>
🍿 ʙʀᴀɪɴ ꜰᴜᴇʟᴇᴅ : <a href="https://www.mongodb.com/">ᴍᴏɴɢᴏ ᴅʙ</a>
😚 ᴄᴏᴅɪɴɢ ᴍᴜsᴄʟᴇs : <a href="https://www.python.org/">ᴘʏᴛʜᴏɴ 3</a>
😜 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : <a href="https://t.me/Prime_Bots_Support_RoBot">Cᴏɴɴᴇᴄᴛ Oᴡɴᴇʀ</a>**"""

DONATE_TXT = """<blockquote>❤️‍🔥 𝐓𝐡𝐚𝐧𝐤𝐬 𝐟𝐨𝐫 𝐬𝐡𝐨𝐰𝐢𝐧𝐠 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭 𝐢𝐧 𝐃𝐨𝐧𝐚𝐭𝐢𝐨𝐧</blockquote>

<b><i>💞  ɪꜰ ʏᴏᴜ ʟɪᴋᴇ ᴏᴜʀ ʙᴏᴛ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴅᴏɴᴀᴛᴇ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ₹𝟷𝟶, ₹𝟸𝟶, ₹𝟻𝟶, ₹𝟷𝟶𝟶, ᴇᴛᴄ.</i></b>

❣️ 𝐷𝑜𝑛𝑎𝑡𝑖𝑜𝑛𝑠 𝑎𝑟𝑒 𝑟𝑒𝑎𝑙𝑙𝑦 𝑎𝑝𝑝𝑟𝑒𝑐𝑖𝑎𝑡𝑒𝑑 𝑖𝑡 ℎ𝑒𝑙𝑝𝑠 𝑖𝑛 𝑏𝑜𝑡 𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑚𝑒𝑛𝑡

💵 𝗔𝗡𝗬 𝗖𝗢𝗨𝗡𝗧𝗥𝗬 𝗔𝗟𝗟 𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗠𝗘𝗧𝗛𝗢𝗗 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘. যদি বিকাশ বা 𝗤𝗥 কোড ছাড়া অথবা অন্য কিছু মাধ্যমে
 পেমেন্ট করতে চাইলে অথবা আরো কিছু জানার থাকলে
𝗖𝗢𝗡𝗡𝗘𝗖𝗧 𝗔𝗗𝗠𝗜𝗡 ➠ <a href="https://t.me/Prime_Admin_Support_ProBot">𝐌𝐑.𝐏𝐑𝐈𝐌𝐄</a> 
"""

FORCE_SUBSCRIBE_TEXT = """ 
<i><b>🙁 ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴜʀʟ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.

ᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇</b></i>"""

START_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('💬 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/Prime_Botz_Support'),
        InlineKeyboardButton('🦋‌ ᴀʙᴏᴜᴛ 🦋', callback_data='about')
    ],[
        InlineKeyboardButton('⍟ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ⍟', url='https://t.me/Prime_Botz')
    ],[
        InlineKeyboardButton('☆ 💫 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 💫 ☆', url='https://t.me/Prime_Nayem')    
    ]]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⍟ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ⍟', url='https://t.me/Prime_Botz'),
        InlineKeyboardButton('👨‍💻 ᴏᴡɴᴇʀ 👨‍💻', url='https://telegram.me/Prime_Nayem')
	],[
        InlineKeyboardButton('🤝 ᴘʀɪᴍᴇ ʙᴏᴛᴢ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 💬', url='https://t.me/Prime_Botz_Support')	
	],[
        InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='home')
        ]]
    )


async def send_msg(user_id, message):
	try:
		await message.copy(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : deactivated\n"
	except UserIsBlocked:
		return 400, f"{user_id} : user is blocked\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : user id invalid\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"

@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        ) 
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format(update.from_user.mention),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    client = bot
    message = update

    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn:
                username = (await client.get_me()).username
                if len(message.command) > 1:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
                else:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])

                await message.reply_photo(
                    photo="https://envs.sh/KgA.jpg",  # Replace with your image link
                    caption=(
                        f"<b>👋 Hello {message.from_user.mention},\n\n"
                        "ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ʏᴏᴜ ᴍᴜꜱᴛ ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ. "
                        "ᴄʟɪᴄᴋ ᴏɴ \"✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇\" ʙᴜᴛᴛᴏɴ.ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ \"ʀᴇǫᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ\" ʙᴜᴛᴛᴏɴ. "
                        "ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴏɴ \"ᴛʀʏ ᴀɢᴀɪɴ\" ʙᴜᴛᴛᴏɴ.</b>"
                    ),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
        except Exception as e:
            print(e)

    # যদি নতুন ইউজার হয়, ডাটাবেসে এন্ট্রি যোগ করুন
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    # স্টার্ট মেসেজে টেক্সট, বাটন, এবং পিকচার পাঠানো
    await update.reply_photo(
        photo="https://envs.sh/LxR.jpg",  # পিকচারের লিঙ্ক দিন
        caption=START_TEXT.format(update.from_user.mention),  # মেসেজ টেক্সট
        reply_markup=START_BUTTONS  # বাটন
    )

@Bot.on_message(filters.private & filters.command(["donate"]))
async def donation(bot, message):
    btn = [[
        InlineKeyboardButton(text="❌  ᴄʟᴏsᴇ  ❌", callback_data="close")
    ]]
    yt=await message.reply_photo(photo='https://envs.sh/AR9.jpg', caption=DONATE_TXT, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

def upload_image_requests(image_path):
    upload_url = "https://envs.sh"

    try:
        with open(image_path, 'rb') as file:
            files = {'file': file} 
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                return response.text.strip() 
            else:
                raise Exception(f"Upload failed with status code {response.status_code}")

    except Exception as e:
        print(f"Error during upload: {e}")
        return None

@Bot.on_message(filters.media & filters.private)
async def upload(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)

    if UPDATE_CHANNEL:
        try:
            user = await client.get_chat_member(UPDATE_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await message.reply_text(text="You are banned!")
                return
        except UserNotParticipant:
            await message.reply_photo(
                photo="https://envs.sh/Lwa.jpg",  # ছবির লিংক
                caption="Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ ғɪʀꜱᴛ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ Jᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.\n\nғɪʀꜱᴛ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '✇ Jᴏɪɴ Oᴜʀ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇' ʙᴜᴛᴛᴏɴ, ᴛʜᴇɴ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ 'ʀᴇᴏᴜᴇꜱᴛ ᴛᴏ Jᴏɪɴ' ʙᴜᴛᴛᴏɴ.\n\nᴀғᴛᴇʀ ᴛʜᴀᴛ ᴄᴏᴍᴇ ʜᴇʀᴇ ᴀɢᴀɪɴ ᴀɴᴅ ꜱᴇɴᴅ ʏᴏᴜʀ ғɪʟᴇ.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="✇ Jᴏɪɴ Oᴜʀ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇", url=f"https://telegram.me/{UPDATE_CHANNEL}")]]
                )
            )
            return
        except Exception as error:
            print(error)
            await message.reply_text(text="<b>ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ...</b>", disable_web_page_preview=True)
            return

    file_size_limit = 15 * 1024 * 1024  # 50 MB in bytes 
    if message.document and message.document.file_size > file_size_limit:
        await message.reply_text("<b>⚠️ ꜱᴇɴᴅ ᴀ ᴍᴇᴅɪᴀ ᴜɴᴅᴇʀ 15 ᴍʙ</b>")
        return
    elif message.photo and message.photo.file_size > file_size_limit:
        await message.reply_text("<b>⚠️ ꜱᴇɴᴅ ᴀ ᴍᴇᴅɪᴀ ᴜɴᴅᴇʀ 15 ᴍʙ</b>")
        return

    path = await message.download()

    uploading_message = await message.reply_text("<code>ᴜᴘʟᴏᴀᴅɪɴɢ...</code>")

    try:
        image_url = upload_image_requests(path)
        if not image_url:
            raise Exception("Failed to upload file.")
    except Exception as error:
        await uploading_message.edit_text(f"Upload failed: {error}")
        return

    try:
        os.remove(path)
    except Exception as error:
        print(f"Error removing file: {error}")
	    
    await uploading_message.delete()
    codexbots=await message.reply_photo(
        photo=f'{image_url}',
        caption=f"<b>ʏᴏᴜʀ ᴄʟᴏᴜᴅ ʟɪɴᴋ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.Cʟɪᴄᴋ Tᴏ Cᴏᴘʏ 👇</b>\n\n🔗 𝑳𝒊𝒏𝒌 :- <code>{image_url}</code> \n\n<b> Pᴏᴡᴇʀᴇᴅ ʙʏ ➠ <a href='https://t.me/Prime_Botz'>⍟ Pʀɪᴍᴇ Bᴏᴛᴢ ⍟</a></b>",
        #disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="•🔗 ᴏᴘᴇɴ ʟɪɴᴋ 🔗•", url=image_url),
            InlineKeyboardButton(text="•🖇️ sʜᴀʀᴇ ʟɪɴᴋ 🖇️•", url=f"https://telegram.me/share/url?url={image_url}")
        ], [
            InlineKeyboardButton(text="❌   ᴄʟᴏsᴇ   ❌", callback_data="close_data")
        ]])
   )
    
@Bot.on_message(filters.private & filters.command("users") & filters.user(BOT_OWNER))
async def users(bot, update):
    total_users = await db.total_users_count()
    text = "Bot Status\n"
    text += f"\nTotal Users: {total_users}"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
	broadcast_ids = {}
	all_users = await db.get_all_users()
	broadcast_msg = update.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
	else:
	    await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
	os.remove('broadcast.txt')


Bot.run()

import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


#config#

bot = Client(
    'moonBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı

@bot.on_message(filters.command(['start']))
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgQAAxkBAAI8bmKIvgnlJyCrq9HIxSvCZCbm5CEjAAIaEAACpvFxHg-Z648-SCRWJAQ")
    await message.reply_text(
    f"""● **Salam 👋** {message.from_user.mention}\n\n**» Mən Mahnı Yükləmə botuyam isdədiyin mahnını yükləyə bilərəm**\n\n**✅ kömək üçün** /komek **komutuna bas**""",
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🇦🇿 MƏni Qrupa Əlavə Et 🇹🇷', url=f'http://t.me/azesongBot?startgroup=new}'),
                  ],[
                    InlineKeyboardButton('✅ Dəsdək ', url=f'https://t.me/{Config.GROUP}'),
                    InlineKeyboardButton('⏳ 𝖪𝖺𝗇𝖺𝗅 ', url=f'https://t.me/{Config.PLAYLIST_NAME}')
                  ],[
                    InlineKeyboardButton('🧑🏻‍💻 Developer 🧑🏻‍💻', url=f'https://t.me/Thagiyevvvv')
                ]
            ]
        )
    )
    
#yardım mesajı

@bot.on_message(filters.command(['komek']))
def help(client, message):
    helptext = f'• **Mahnı Yükləmək üçün /mahni komutunu işlədə bilərsən .**\n\n**Məs.** :\n•> /mahni `Mir Yusif - Ağ təyyarə.`'
    message.reply_text(
        text=helptext, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🇦🇿 MƏni Qrupa Əlavə Et 🇹🇷', url=f'http://t.me/azesongBot?startgroup=new}'),
                  ],[
                    InlineKeyboardButton('✅ Dəsdək', url=f'https://t.me/{Config.GROUP}'),
                    InlineKeyboardButton('⏳ 𝖪𝖺𝗇𝖺𝗅', url=f'https://t.me/{Config.PLAYLIST_NAME}')
                  ],[
                    InlineKeyboardButton('🧑🏻‍💻 Developer 🧑🏻‍💻', url=f'https://t.me/Thagiyevvvv')
                ]
            ]
        )
    )
#alive mesaji#

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`Salam Sahib Bəy, 🐊👑`')
    
#musik indirme#

@bot.on_message(filters.command("mahni") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b>• **Mahnın Axtarılır** ...</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("<b>⛔ **Bağışla mahnı tapılmadı.\n\n xahiş başka mahnı adş yazın.**</b>")
        print(str(e))
        return
    m.edit("<b>•> **Yükləmə Başladı...**</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎵 𝐘𝐮̈𝐤𝐥𝐞𝐝𝐢 [Aze song](https://t.me/{Config.BOT_USERNAME})"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("•> **Yükleniyor**...")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="@mutsuz_panda")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=rep, performer="@mutsuz_panda", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit("<b>⛔ **Xətanın düzəlməsini gözləyin** .</b>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()

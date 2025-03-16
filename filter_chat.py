from telethon import TelegramClient, events,Button
import json
import ctypes
import asyncio

api_id = 28068111  
api_hash = "44f284f6677586bed96e4c1573e1487f"  
session_name = "userbot"

BOT_USERNAME = -1002292353387
admins_id = [5427845145]
chat_id1 = [
    -1001739925049, -1001514104584, -1001651340967, -1002198131306,
    -1002229609632, -1002235062051, -1001847706166, -1001915295049,
    -1001900765328, -1001926112461, -1002041693546, -1002115089076,
]



FILENAME = 'ban_user.json'
bot_token = "8195836711:AAG7pFZsoPucddc38jU6LVsMjHKz1r8sWCw"


client = TelegramClient(session_name, api_id, api_hash)
bot = TelegramClient('bot',api_hash=api_hash,api_id=api_id).start(bot_token=bot_token)




def json_to_set():
    try:
        with open(FILENAME, "r") as f:
            return set(json.load(f))  # JSON ro'yxatni set ga aylantirish
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def set_to_json(users):
    with open(FILENAME, "w") as f:
        json.dump(list(users), f) 

def add_user_to_json(user_id):
    try:
        with open(FILENAME, "r+") as f:
            users = json.load(f)  # JSON faylni o‘qish
            if user_id not in users:  # Agar ID yo'q bo'lsa, qo'shish
                users.append(user_id)
                f.seek(0)  # Fayl boshiga qaytish
                json.dump(users, f)  # Yangilangan ro‘yxatni yozish
                f.truncate()  # Keraksiz ma'lumotlarni o‘chirish
            else:
                pass
    except (FileNotFoundError, json.JSONDecodeError):
        # Agar fayl mavjud bo‘lmasa yoki buzilgan bo‘lsa, yangisini yaratish
        with open(FILENAME, "w") as f:
            json.dump([user_id], f)
        

ban_user = json_to_set()
count1 = len(ban_user)

keys = [
    'C O B A L T', 'COBALT', 'JENTRA', 'Jentra', 'KAM', 'Kam', 'OLAMIZ', 'Olaman', 'Onix', 
    'Trekir', 'YURAMAN', 'YURAMIZ', 'Yuramiz', 'Yuramiz', 'YURАMZ', 'Yuramiz', 'YURAMAN', 
    'ЮРАМАН', 'ЮРАМИЗ', 'ЮРAМАН', 'ЮРAМИЗ', 'ЙУРАМАН', 'ЙУРАМИЗ', 'йураман', 'йурамиз', 
    'ЖЕНТРА', 'ЖЕНТРА', 'жентра', 'жентрa', 'КAМ', 'КАМ', 'Кобилт', 'Кобалт', 'КОБАЛЬТ', 
    'КОБЛТ', 'КОБОЛТ', 'Коблт', 'ҚОБАЛТ', 'қобалт', 'малуби', 'месяц', 'на', 'ОЛАМИЗ', 
    'ОЛАМАН', 'ОЛАМАН', 'ОЛАМЗ', 'оламан', 'оламиз', 'оламз', 'ОЛАМИЗ', 'ОЛAМИЗ','USDT',
    'OLAMIZ', 'OLAMIZ', 'olamiz', 'olаmiz', 'Olamiz', 'Olamiz', 'Оламиз', 'опкетамиз', 
    'сotilad', 'sotiladi', 'sotilad', 'sotiladi', 'ТУХТАМИМИЗ', '𝗞𝗢𝗕𝗔𝗟𝗧', '✔️', '✅', 
    '🚕', '🚖', '🚘', '🚫', '📊', '🔤', '☎️', '😎', '🇺🇿', 'хурматли','olamz','💋','Kredit',
    'НЕХСИЯ','Windows'
]

keys = [i.lower() for i in keys]


@client.on(events.NewMessage(chats=chat_id1))
async def forward_message(event):
    global count1

    text = event.message.text
    user_id = event.sender_id

    lib = ctypes.CDLL("./is_shopir.so")
    lib.is_shopir.restype = ctypes.c_int
    c_blocked_words = (ctypes.c_char_p * len(keys))(*[s.encode('utf-8') for s in keys])
    c_message = ctypes.c_char_p(event.message.text.lower().encode('utf-8'))
    result = lib.is_shopir(c_message, c_blocked_words, len(keys))

    if result:
        if user_id not in ban_user:
            ban_user.add(user_id)
            add_user_to_json(user_id=user_id)
            count1 += 1
          

    else:
        if user_id not in ban_user:
            if len(text) >10 :

                formatted_text = (
                f"🆔 <b>ID:</b> <a href='tg://openmessage?user_id={user_id}'>{user_id}</a>\n"
                f"🆔 <b>iOS ID :</b> <a href='https://t.me/@id{user_id}'>{user_id}</a>\n"
                f"📝 <b>Matn:\n</b> {text}\n \n"
                f"<b>Profilga o‘tish:</b> <a href='tg://openmessage?user_id={user_id}'> Bu yerga bosing</a>"


    )
                buttons = [[Button.url("Profilga o'tish", f"tg://user?id={user_id}")]]
    
                await bot.send_message(BOT_USERNAME,formatted_text,buttons=[[Button.url('Profilni o\'tish',url=f'tg://openmessage?user_id={user_id}')]],parse_mode='HTML')      

@bot.on(events.NewMessage(chats=admins_id,pattern=r"^/(add_group|add_word|add_admin)"))
async def handle_commands(event):
    if event.sender_id in admins_id:    
        parts = event.message.text.split(" ", maxsplit=2)

        if len(parts) < 2:
            return await event.reply("❌ Buyruq noto‘g‘ri yozilgan!")

        command = parts[0] 
        arg1 = parts[1]

        if command == "/add_group":
            if arg1.startswith("-100"):
                chat_id1.append(int(arg1))
                
                await event.reply(f"✅ Guruh qo‘shildi: {arg1}")
            else:
                await event.reply("❌ Guruh ID noto‘g‘ri!")

        elif command == "/add_word":
            if arg1.startswith('"') and arg1.endswith('"'):
                word = arg1[1:-1] 
                keys.append(str(word))
                await event.reply(f"✅ So‘z qo‘shildi: {word}")
            else:
                await event.reply("❌ So‘zni qo‘shtirnoq ichida yozing!")

        elif command == "/add_admin":
            if arg1.isdigit():
                admins_id.append(int(arg1))
                
                await event.reply(f"✅ Admin qo‘shildi: {arg1}")
            else:
                await event.reply("❌ Admin ID noto‘g‘ri!")
    else:
        await bot.send_message("siz admin emassiz va bu buyruqlarni faqat admin bera oladi ")

@client.on(events.NewMessage(chats=chat_id1))
async def message_handler(event):
    await asyncio.sleep(5)
    await client.send_read_acknowledge(event.chat_id)

try:
    client.start()
    client.run_until_disconnected()
except KeyboardInterrupt:
    set_to_json(users=ban_user)


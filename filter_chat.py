from telethon import TelegramClient, events, Button
import json
import ctypes
import asyncio

# Configuration
api_id = 28068111  
api_hash = "44f284f6677586bed96e4c1573e1487f"  
session_name = "userbot"
BOT_USERNAME = [-1002556088883]
bot_token = "8147699203:AAG-eiaOUsNSPn4kbSZzx678eiFYgrRu3rA"

# File names
BAN_USER_FILE = 'ban_user.json'
ADMINS_FILE = 'admins.json'
GROUPS_FILE = 'groups.json'
KEYWORDS_FILE = 'keywords.json'

# Initialize clients
client = TelegramClient(session_name, api_id, api_hash)
bot = TelegramClient('bot', api_hash=api_hash, api_id=api_id).start(bot_token=bot_token)

# Load data from files
def load_json_file(filename, default=[]):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_to_json_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

# Load initial data
ban_user = set(load_json_file(BAN_USER_FILE))
admins_id = load_json_file(ADMINS_FILE, [5427845145,7593793240,137289947])
chat_id1 = load_json_file(GROUPS_FILE, [
    -1001739925049, -1001514104584, -1001651340967, -1002198131306,
    -1002229609632, -1002235062051, -1001847706166, -1001915295049,
    -1001900765328, -1001926112461, -1002041693546, -1002115089076,
])
keys = load_json_file(KEYWORDS_FILE, [
    'C O B A L T', 'COBALT', 'JENTRA', 'Jentra', 'KAM', 'Kam', 'OLAMIZ', 'Olaman', 'Onix', 
    'Trekir', 'YURAMAN', 'YURAMIZ', 'Yuramiz', 'Yuramiz', 'YURАMZ', 'Yuramiz', 'YURAMAN', 
    'ЮРАМАН', 'ЮРАМИЗ', 'ЮРAМАН', 'ЮРAМИЗ', 'ЙУРАМАН', 'ЙУРАМИЗ', 'йураман', 'йурамиз', 
    'ЖЕНТРА', 'ЖЕНТРА', 'жентra', 'жентрa', 'КAМ', 'КАМ', 'Кобилт', 'Кобалт', 'КОБАЛЬТ', 
    'КОБЛТ', 'КОБОЛТ', 'Коблt', 'ҚОБАЛТ', 'қобалт', 'малуби', 'месяц', 'на', 'ОЛАМИЗ', 
    'ОЛАМАН', 'ОЛАМАН', 'ОЛАМЗ', 'оламан', 'оламиз', 'оламз', 'ОЛАМИЗ', 'ОЛAМИЗ','USDT',
    'OLAMIZ', 'OLAMIZ', 'olamiz', 'olаmiz', 'Olamiz', 'Olamiz', 'Оламиз', 'опкетамиз', 
    'сotilad', 'sotiladi', 'sotilad', 'sotiladi', 'ТУХТАМИМИЗ', '𝗞𝗢𝗕𝗔𝗟𝗧', '✔️', '✅', 
    '🚕', '🚖', '🚘', '🚫', '📊', '🔤', '☎️', '😎', '🇺🇿', 'хурматли','olamz','💋','Kredit',
    'НЕХСИЯ','Windows'
])

# Convert keys to lowercase
keys = [i.lower() for i in keys]

# Button layouts
def get_main_menu_buttons():
    return [
        [Button.inline("➕ Guruh qo'shish", b"add_group")],
        [Button.inline("➕ So'z qo'shish", b"add_word")],
        [Button.inline("➕ Admin qo'shish", b"add_admin")],
        [Button.inline("🚫 Bloklash", b"ban_user")],
        [Button.inline("📊 Statistika", b"stats")]
    ]

def get_cancel_button():
    return [[Button.inline("❌ Bekor qilish", b"cancel")]]

# Command handlers
@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.sender_id in admins_id:
        await event.reply(
            "👨‍💻 Admin panelga xush kelibsiz! Quyidagi menyudan tanlang:",
            buttons=get_main_menu_buttons()
        )
    else:
        await event.reply("⚠️ Sizga ruxsat yo'q!")

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    if event.sender_id not in admins_id:
        return await event.answer("⚠️ Sizga ruxsat yo'q!", alert=True)
    
    data = event.data.decode('utf-8')
    
    if data == "cancel":
        await event.edit("❌ Amal bekor qilindi.", buttons=None)
    
    elif data == "add_group":
        await event.edit(
            "➕ Guruh qo'shish uchun guruh ID sini yuboring (-100 bilan boshlansin):",
            buttons=get_cancel_button()
        )
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("Guruh ID sini kiriting:")
            try:
                group_id_msg = await conv.get_response(timeout=60)
                group_id = group_id_msg.text.strip()
                
                if group_id.startswith("-100") and group_id[4:].isdigit():
                    group_id = int(group_id)
                    if group_id not in chat_id1:
                        chat_id1.append(group_id)
                        save_to_json_file(GROUPS_FILE, chat_id1)
                        await conv.send_message(
                            f"✅ Guruh qo'shildi: {group_id}\nJami guruhlar soni: {len(chat_id1)}",
                            buttons=get_main_menu_buttons()
                        )
                    else:
                        await conv.send_message(
                            "⚠️ Bu guruh allaqachon ro'yxatda!",
                            buttons=get_main_menu_buttons()
                        )
                else:
                    await conv.send_message(
                        "❌ Noto'g'ri format! -100 bilan boshlanadigan raqam bo'lishi kerak.",
                        buttons=get_main_menu_buttons()
                    )
            except asyncio.TimeoutError:
                await event.edit("🕒 Vaqt tugadi!", buttons=get_main_menu_buttons())
    
    elif data == "add_word":
        await event.edit(
            "➕ So'z qo'shish uchun so'zni yuboring:",
            buttons=get_cancel_button()
        )
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("So'zni kiriting:")
            try:
                word_msg = await conv.get_response(timeout=60)
                word = word_msg.text.strip().lower()
                
                if word not in keys:
                    keys.append(word)
                    save_to_json_file(KEYWORDS_FILE, keys)
                    await conv.send_message(
                        f"✅ So'z qo'shildi: {word}\nJami so'zlar soni: {len(keys)}",
                        buttons=get_main_menu_buttons()
                    )
                else:
                    await conv.send_message(
                        "⚠️ Bu so'z allaqachon ro'yxatda!",
                        buttons=get_main_menu_buttons()
                    )
            except asyncio.TimeoutError:
                await event.edit("🕒 Vaqt tugadi!", buttons=get_main_menu_buttons())
    
    elif data == "add_admin":
        await event.edit(
            "➕ Admin qo'shish uchun foydalanuvchi ID sini yuboring:",
            buttons=get_cancel_button()
        )
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("Foydalanuvchi ID sini kiriting:")
            try:
                admin_id_msg = await conv.get_response(timeout=60)
                admin_id = admin_id_msg.text.strip()
                
                if admin_id.isdigit():
                    admin_id = int(admin_id)
                    if admin_id not in admins_id:
                        admins_id.append(admin_id)
                        save_to_json_file(ADMINS_FILE, admins_id)
                        await conv.send_message(
                            f"✅ Admin qo'shildi: {admin_id}\nJami adminlar soni: {len(admins_id)}",
                            buttons=get_main_menu_buttons()
                        )
                    else:
                        await conv.send_message(
                            "⚠️ Bu admin allaqachon ro'yxatda!",
                            buttons=get_main_menu_buttons()
                        )
                else:
                    await conv.send_message(
                        "❌ Noto'g'ri format! Faqat raqam bo'lishi kerak.",
                        buttons=get_main_menu_buttons()
                    )
            except asyncio.TimeoutError:
                await event.edit("🕒 Vaqt tugadi!", buttons=get_main_menu_buttons())
    
    elif data == "ban_user":
        await event.edit(
            "🚫 Foydalanuvchini bloklash uchun ID sini yuboring:",
            buttons=get_cancel_button()
        )
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("Foydalanuvchi ID sini kiriting:")
            try:
                user_id_msg = await conv.get_response(timeout=60)
                user_id = user_id_msg.text.strip()
                
                if user_id.isdigit():
                    user_id = int(user_id)
                    if user_id not in ban_user:
                        ban_user.add(user_id)
                        save_to_json_file(BAN_USER_FILE, list(ban_user))
                        await conv.send_message(
                            f"✅ Foydalanuvchi bloklandi: {user_id}\nJami bloklanganlar: {len(ban_user)}",
                            buttons=get_main_menu_buttons()
                        )
                    else:
                        await conv.send_message(
                            "⚠️ Bu foydalanuvchi allaqachon bloklangan!",
                            buttons=get_main_menu_buttons()
                        )
                else:
                    await conv.send_message(
                        "❌ Noto'g'ri format! Faqat raqam bo'lishi kerak.",
                        buttons=get_main_menu_buttons()
                    )
            except asyncio.TimeoutError:
                await event.edit("🕒 Vaqt tugadi!", buttons=get_main_menu_buttons())
    
    elif data == "stats":
        stats_text = (
            f"📊 Bot statistikasi:\n\n"
            f"👥 Guruhlar soni: {len(chat_id1)}\n"
            f"🛑 Bloklanganlar: {len(ban_user)}\n"
            f"🔑 Kalit so'zlar: {len(keys)}\n"
            f"👨‍💻 Adminlar soni: {len(admins_id)}"
        )
        await event.edit(stats_text, buttons=get_main_menu_buttons())

# Message forwarding logic (same as before)
@client.on(events.NewMessage(chats=chat_id1))
async def forward_message(event):
    global ban_user

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
            save_to_json_file(BAN_USER_FILE, list(ban_user))
          
    else:
        if user_id not in ban_user and len(text) > 10:
            formatted_text = (
                f"🆔 <b>ID:</b> <a href='tg://openmessage?user_id={user_id}'>{user_id}</a>\n"
                f"🆔 <b>iOS ID :</b> <a href='https://t.me/@id{user_id}'>{user_id}</a>\n"
                f"📝 <b>Matn:\n</b> {text}\n \n"
                f" "
            )
            for group in BOT_USERNAME:
                await bot.send_message(group,formatted_text,buttons=[[Button.url('Profilni o\'tish', url=f'tg://openmessage?user_id={user_id}')]],parse_mode='HTML')

@client.on(events.NewMessage(chats=chat_id1))
async def message_handler(event):
    await asyncio.sleep(5)
    await client.send_read_acknowledge(event.chat_id)

try:
    print("Bot ishga tushdi...")
    client.start()
    bot.start()
    client.run_until_disconnected()
except KeyboardInterrupt:
    save_to_json_file(BAN_USER_FILE, list(ban_user))
    print("Bot to'xtatildi. Ma'lumotlar saqlandi.")

from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 26033437
API_HASH = "bd0ba4e78bc139db5ac3179d99bfbe59"
BOT_TOKEN = "8138053640:AAFEoAZfbSyJ8mDII6aZPY9gjfYG_HUHwU8"

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

BAD_WORDS = ["کلمه‌بد", "فحش", "بد1", "بد2"]
WELCOME_TEXT = "👋 خوش آمدی به گروه {} عزیز!"

# ✅ خوش‌آمد و ضد تبچی در یک تابع
@bot.on_message(filters.new_chat_members)
def welcome_and_antitabc(client, message: Message):
    for member in message.new_chat_members:
        username = (member.username or "").lower()

        # خوش آمدگویی
        message.reply_text(WELCOME_TEXT.format(member.first_name))

        # حذف تبچی
        if "bot" in username or "تبچی" in username:
            try:
                client.kick_chat_member(message.chat.id, member.id)
                message.reply(f"❌ {member.first_name} از گروه حذف شد (تبچی)")
            except:
                pass

# ✅ حذف پیام‌های ناخواسته، فیلتر، لینک، پورن، هوش مصنوعی
@bot.on_message(filters.text & filters.group)
def filter_text(client, message: Message):
    text = message.text.lower()

    # ضد لینک
    if "http" in text or "t.me" in text or "@" in text:
        message.delete()
        return

    # فیلتر فحش
    for word in BAD_WORDS:
        if word in text:
            message.delete()
            return

    # ضد پورن
    if any(x in text for x in ["sex", "nude", "porn"]):
        message.delete()
        return

    # پاسخ هوشمند
    if "ربات" in text:
        message.reply("بله عزیزم، من اینجام! 🤖")

# ✅ حذف فوروارد، گیف، ویدیو
@bot.on_message(filters.forwarded | filters.video | filters.animation)
def block_media(client, message: Message):
    message.delete()

# ✅ جلوگیری از تغییر تنظیمات گروه
@bot.on_message(filters.group & filters.service)
def protect_group(client, message: Message):
    if message.new_chat_title or message.new_chat_photo or message.new_chat_invite_link:
        if not message.from_user or not message.from_user.is_self:
            message.delete()

print("✅ ربات با موفقیت اجرا شد و آماده‌ست.")
bot.run()
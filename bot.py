import os
import threading
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from keep_alive import run as run_web

# ══════════════════════════════════════
#          إعدادات البوت
# ══════════════════════════════════════

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# معرف القناة المصدر (مثال: -1001234567890)
SOURCE_CHANNEL = int(os.environ.get("SOURCE_CHANNEL", "0"))

# معرف قناتك الهدف (مثال: -1001987654321)
DEST_CHANNEL = int(os.environ.get("DEST_CHANNEL", "0"))

# ══════════════════════════════════════
#          إنشاء البوت
# ══════════════════════════════════════

bot = Client(
    name="forwarder_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True  # بدون ملف session محلي
)

# ══════════════════════════════════════
#    فلتر: توجيه الملفات فقط
# ══════════════════════════════════════

MEDIA_FILTER = (
    filters.document    # ملفات (PDF, ZIP, إلخ)
    | filters.video     # فيديوهات
    | filters.audio     # ملفات صوتية
    | filters.photo     # صور
    | filters.voice     # رسائل صوتية
    | filters.animation # صور متحركة GIF
    | filters.sticker   # ملصقات
)

# ══════════════════════════════════════
#     معالج الرسائل - توجيه الملفات
# ══════════════════════════════════════

@bot.on_message(filters.chat(SOURCE_CHANNEL) & MEDIA_FILTER)
async def forward_files(client, message):
    """إعادة توجيه الملفات من القناة المصدر إلى قناتك"""
    try:
        # copy = إرسال بدون علامة "Forwarded from"
        await message.copy(chat_id=DEST_CHANNEL)

        # طباعة تأكيد
        media_type = message.media.name if message.media else "unknown"
        print(f"✅ تم توجيه {media_type} | Message ID: {message.id}")

    except Exception as e:
        print(f"❌ خطأ في التوجيه: {e}")


# ══════════════════════════════════════
#  (اختياري) توجيه كل شيء بما فيه النصوص
# ══════════════════════════════════════

# إذا تريد توجيه كل الرسائل (نصوص + ملفات)
# أزل التعليق عن الكود التالي واحذف الدالة اللي فوق

# @bot.on_message(filters.chat(SOURCE_CHANNEL))
# async def forward_all(client, message):
#     try:
#         await message.copy(chat_id=DEST_CHANNEL)
#         print(f"✅ تم توجيه الرسالة: {message.id}")
#     except Exception as e:
#         print(f"❌ خطأ: {e}")


# ══════════════════════════════════════
#  (اختياري) توجيه مع الاحتفاظ بالمصدر
# ══════════════════════════════════════

# إذا تريد تظهر "Forwarded from..." استخدم forward بدل copy:

# @bot.on_message(filters.chat(SOURCE_CHANNEL) & MEDIA_FILTER)
# async def forward_with_source(client, message):
#     try:
#         await message.forward(chat_id=DEST_CHANNEL)
#         print(f"✅ تم التوجيه مع المصدر: {message.id}")
#     except Exception as e:
#         print(f"❌ خطأ: {e}")


# ══════════════════════════════════════
#              التشغيل
# ══════════════════════════════════════

if __name__ == "__main__":
    # تشغيل سيرفر الويب في thread منفصل (لـ Render)
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    print("🌐 Web server started...")

    # تشغيل البوت
    print("🤖 Bot is starting...")
    print(f"📥 Source Channel: {SOURCE_CHANNEL}")
    print(f"📤 Dest Channel:   {DEST_CHANNEL}")
    bot.run()

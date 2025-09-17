import telebot
from telebot import types

# ✅ توکن ربات
bot = telebot.TeleBot("8006975636:AAGluWU5welafL7CRHHMWBevSQdx9a5FmwM")

# ذخیره وضعیت دسترسی لكل مستخدم
user_access = {}

# -------------------------
# شناسه عددی کانال خصوصی (حتماً ربات ادمین باشه)
# -------------------------
CHANNEL_ID = -1003033519777  # این رو با آی‌دی واقعی کانال جایگزین کن

# -------------------------
# دیکشنری پیام‌ها (معلومات الطلاب - RAR) => message_id ها
# -------------------------
grade_files_msgid = {
    "براعم": 11,  # پیام‌های واقعی بعد از آپلود پر می‌شوند
    "5": 10,
    "6": 9,
    "7": 8,
    "8": 7,
    "9": 6,
    "10": 5,
    "11": 4,
    "12": 3
}

# -------------------------
# دیکشنری پیام‌ها (الحضور والغياب - Excel) => message_id ها
# -------------------------
attendance_files_msgid = {
    "براعم": None,
    "5": None,
    "6": None,
    "7": None,
    "8": None,
    "9": None,
    "10": None,
    "11": None,
    "12": None
}

# -------------------------
# /start
# -------------------------
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,
                     "👋 أهلاً بك في بوت مؤسسة الطليعة العلمية.\n"
                     "للوصول إلى اختيار السنة الدراسية، اكتب /year.\n\n"
                     "الأوامر المتاحة:\n"
                     "/info - معلومات عن المؤسسة\n"
                     "/departments - عرض المجموعات التعليمية\n"
                     "/contact - طرق التواصل")

# -------------------------
# /info
# -------------------------
@bot.message_handler(commands=['info'])
def info_command(message):
    bot.send_message(message.chat.id,
                     "📍خوزستان- اهواز-کمپلو شمالی- حي الزهراء (آهن افشار) - شارع بينا - بين زينب و غزنوي\n"
                     "🏛 مؤسسة الطليعة العلمية 🌿🌻")

# -------------------------
# /departments
# -------------------------
@bot.message_handler(commands=['departments'])
def departments_command(message):
    bot.send_message(message.chat.id,
                     "🏫 المجموعات التعليمية:\n- علوم\n- رياضيات\n- لغة عربية\n- لغة إنجليزية")

# -------------------------
# /contact
# -------------------------
@bot.message_handler(commands=['contact'])
def contact_command(message):
    bot.send_message(message.chat.id,
                     "📞 طرق التواصل:\n- الهاتف: 123456789\n- البريد الإلكتروني: info@tali3a.edu\n- موقع المؤسسة: www.tali3a.edu")

# -------------------------
# /year (مع كلمة مرور)
# -------------------------
@bot.message_handler(commands=['year'])
def year_command(message):
    msg = bot.send_message(message.chat.id, "🔑 الرجاء إدخال كلمة السر:")
    bot.register_next_step_handler(msg, check_password)

def check_password(message):
    if message.text.strip() == "T0@girl":
        user_access[message.chat.id] = None
        send_year_keyboard(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ كلمة السر غير صحيحة!")

# -------------------------
# كيبورد اختيار السنة
# -------------------------
def send_year_keyboard(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add("عام 1404-1405", "↩️ رجوع للبداية")
    bot.send_message(chat_id, "📚 الرجاء اختيار السنة الدراسية:", reply_markup=keyboard)

# -------------------------
# كيبورد اختيار الصف
# -------------------------
def send_grade_keyboard(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    grades = ["براعم", "5", "6", "7", "8", "9", "10", "11", "12"]
    keyboard.add(*grades)
    keyboard.add("↩️ رجوع لاختيار السنة")
    bot.send_message(chat_id, "📖 الرجاء اختيار الصف:", reply_markup=keyboard)

# -------------------------
# كيبورد خيارات الصف
# -------------------------
def send_class_options(chat_id, grade):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add("📋 إرسال كل معلومات الطلاب", "🕒 الحضور والغياب")
    keyboard.add("↩️ رجوع")
    bot.send_message(chat_id, f"✅ لقد اخترت الصف {grade}.\nاختر العملية:", reply_markup=keyboard)

# -------------------------
# هندلر آپلود فایل‌ها در کانال
# -------------------------
@bot.message_handler(content_types=['document'])
def handle_document(message):
    # فقط فایل‌هایی که در کانال آپلود می‌شوند
    if message.chat.id == CHANNEL_ID:
        file_name = message.document.file_name
        
        # دسته‌بندی فایل‌ها بر اساس پسوند
        if file_name.endswith(".rar"):
            # برای اطلاعات دانش‌آموزان
            for grade in grade_files_msgid:
                if grade in file_name:  # اگر اسم فایل شامل نام کلاس بود
                    grade_files_msgid[grade] = message.message_id
        elif file_name.endswith(".xlsx"):
            # برای حضور و غیاب
            for grade in attendance_files_msgid:
                if grade in file_name:
                    attendance_files_msgid[grade] = message.message_id

        print(f"✅ فایل ثبت شد: {file_name} - message_id: {message.message_id}")

# -------------------------
# هندلر عام برای انتخاب‌ها و ارسال فایل‌ها
# -------------------------
@bot.message_handler(func=lambda m: True)
def handle_selection(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_access:
        bot.send_message(chat_id, "❌ الرجاء إدخال كلمة السر أولاً. اكتب /year.")
        return

    if text == "عام 1404-1405":
        send_grade_keyboard(chat_id)
        return
    elif text == "↩️ رجوع للبداية":
        start_command(message)
        bot.send_message(chat_id, "↩️ تم الرجوع إلى البداية.", reply_markup=types.ReplyKeyboardRemove())
        return

    if text in grade_files_msgid:
        user_access[chat_id] = text
        send_class_options(chat_id, text)
        return
    elif text == "↩️ رجوع لاختيار السنة":
        send_year_keyboard(chat_id)
        return

    if text == "📋 إرسال كل معلومات الطلاب":
        grade = user_access.get(chat_id)
        if grade and grade_files_msgid.get(grade):
            bot.forward_message(chat_id, CHANNEL_ID, grade_files_msgid[grade])
        else:
            bot.send_message(chat_id, "❌ فایل موجود نیست یا هنوز آپلود نشده.")
        return

    if text == "🕒 الحضور والغياب":
        grade = user_access.get(chat_id)
        if grade and attendance_files_msgid.get(grade):
            bot.forward_message(chat_id, CHANNEL_ID, attendance_files_msgid[grade])
        else:
            bot.send_message(chat_id, "❌ فایل موجود نیست یا هنوز آپلود نشده.")
        return

    if text == "↩️ رجوع":
        send_grade_keyboard(chat_id)
        return

    bot.send_message(chat_id, "❌ خيار غير صالح. الرجاء اختيار من القائمة.")

# -------------------------
# اجرای ربات
# -------------------------
#bot.polling()

bot.infinity_polling(skip_pending=True)
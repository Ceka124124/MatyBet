import telebot
import re

BOT_TOKEN = '8189840347:AAE4-PmjNNoH89mke55VnAgJmsrK_4drYe4'
GROUP_TAG = '@pesinomreleriburda'  # Değiştir: hedef grubun kullanıcı adı (örn. @sohbetgrubu)

# Basit küfür filtresi (istenirse geliştirilebilir)
KUFUR_LISTESI = [
    'kötükelime1', 'kötükelime2', 'kufur1', 'kufur2', 'orospu', 'amk', 'aq'
]

bot = telebot.TeleBot(BOT_TOKEN)

def kufur_var_mi(metin):
    return any(re.search(rf'\b{kufur}\b', metin, re.IGNORECASE) for kufur in KUFUR_LISTESI)

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_message(message):
    if message.text.startswith("!ilet") or message.text.startswith("/ilet"):
        content = message.text.split(' ', 1)
        msg_body = content[1] if len(content) > 1 else ''
        if kufur_var_mi(msg_body):
            return  # Küfürlü mesaj engellenir
        user = message.from_user.first_name or "User"
        iletilecek = f"📨 {user}:\n{msg_body}"
        bot.send_message(GROUP_TAG, iletilecek)

bot.infinity_polling()

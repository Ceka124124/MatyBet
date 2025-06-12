import telebot

BOT_TOKEN = '8189840347:AAE4-PmjNNoH89mke55VnAgJmsrK_4drYe4'
TARGET_USER_ID = 5633974834  # Mesajları alacak kullanıcı ID'si

bot = telebot.TeleBot(BOT_TOKEN)

# Start komutu mesajı
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Salam Qaqaş Nə Problem varsa Video Şəkil Və Mesaj obşim Sübutları Və tagını göndər Kanalda Paylaşılacağ!")

# Her mesajı yakala (text dahil tüm türler)
@bot.message_handler(content_types=['text', 'photo', 'video', 'audio', 'voice', 'document', 'sticker'])
def forward_all(message):
    sender = message.from_user.first_name or "İstifadəçi"
    
    if message.content_type == 'text':
        caption = f"📩 {sender} adlı istifadəçidən MESAJ:\n{message.text}"
        bot.send_message(TARGET_USER_ID, caption)

    elif message.content_type == 'photo':
        caption = f"📩 {sender} adlı istifadəçidən ŞƏKİL:"
        bot.send_photo(TARGET_USER_ID, message.photo[-1].file_id, caption=caption)

    elif message.content_type == 'video':
        caption = f"📩 {sender} adlı istifadəçidən VİDEO:"
        bot.send_video(TARGET_USER_ID, message.video.file_id, caption=caption)

    elif message.content_type == 'audio':
        caption = f"📩 {sender} adlı istifadəçidən MUSİQİ:"
        bot.send_audio(TARGET_USER_ID, message.audio.file_id, caption=caption)

    elif message.content_type == 'voice':
        caption = f"📩 {sender} adlı istifadəçidən SƏS MESAJI:"
        bot.send_voice(TARGET_USER_ID, message.voice.file_id, caption=caption)

    elif message.content_type == 'document':
        caption = f"📩 {sender} adlı istifadəçidən SƏNƏD:"
        bot.send_document(TARGET_USER_ID, message.document.file_id, caption=caption)

    elif message.content_type == 'sticker':
        caption = f"📩 {sender} adlı istifadəçidən STİKER:"
        bot.send_sticker(TARGET_USER_ID, message.sticker.file_id)
        bot.send_message(TARGET_USER_ID, caption)

bot.infinity_polling() 

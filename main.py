import telebot

API_TOKEN = '8123445209:AAHWzZZbdBOyfVetkBJ8HM7QwhMj33UW_rc'
ADMIN_ID = 5276703930

bot = telebot.TeleBot(API_TOKEN)
reply_mapping = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "Bot Online")
    else:
        user_name = message.from_user.first_name
        reply_text = f"🙏 Welcome {user_name}\n\nAap yahan message bhej sakte ho.\nAdmin aapko isi bot par reply karega."
        bot.reply_to(message, reply_text)

@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'sticker', 'document'], func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
def admin_reply(message):
    try:
        replied_msg_id = message.reply_to_message.message_id
        user_id = reply_mapping.get(replied_msg_id)

        if not user_id and message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id

        if user_id:
            bot.copy_message(user_id, ADMIN_ID, message.message_id)
            bot.reply_to(message, "Sent")
        else:
            bot.reply_to(message, "Error: User ID not found")
    except Exception:
        pass

@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'sticker', 'document'], func=lambda m: m.chat.id != ADMIN_ID)
def forward_to_admin(message):
    forwarded_msg = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    reply_mapping[forwarded_msg.message_id] = message.chat.id

bot.remove_webhook()
bot.infinity_polling()

import telebot
import os
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv('TOKEN')
bot_name = os.getenv('BOT_NAME')
bot = telebot.TeleBot(Token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	print("Received message:", message.text)
	bot.send_message(message.chat.id, "Привет, я бот-диетолог " + bot_name + ". Я помогу тебе сбросить вес.")

@bot.message_handler(func=lambda m: True)
def echo(message):
	bot.reply_to(message, message.text)

print("Bot started...")
bot.infinity_polling()
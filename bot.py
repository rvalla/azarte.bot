from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, ParseMode
import traceback
import json as js
from assets import Assets
from text import Text

security = js.load(open("security.json"))
messages = js.load(open("messages_es.json"))
ass = Assets()
txt = Text()

def start(update, context):
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=messages["hello"])

def random_attractor(update, context):
	id = update.effective_chat.id
	file_name = ass.get_attractor()
	file = open(file_name, "rb")
	try:
		context.bot.send_photo(chat_id=id, photo=file)
		context.bot.send_message(chat_id=id, text=messages["attractor"])
	except:
		context.bot.send_message(chat_id=id, text=messages["error"])
		print(traceback.format_exc())
		print(file_name)

def poem(update, context):
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=txt.get_poem())

def print_help(update, context):
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=messages["help"])

def main():
	updater = Updater(security["token"])
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("attractor", random_attractor))
	dp.add_handler(CommandHandler("poem", poem))
	dp.add_handler(CommandHandler("help", print_help))
	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()

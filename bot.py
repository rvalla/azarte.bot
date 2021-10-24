from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, ParseMode
import traceback, logging
import json as js
from assets import Assets
from text import Text
from myrandom import MyRandom

logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
security = js.load(open("security.json"))
messages = js.load(open("messages_es.json"))
ass = Assets()
txt = Text()
mrd = MyRandom()

def start(update, context):
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=messages["hello"], parse_mode=ParseMode.HTML)

def random_attractor(update, context):
	id = update.effective_chat.id
	data = ass.get_attractor()
	logging.info("Uploading attractor to Telegram servers...")
	try:
		context.bot.send_message(chat_id=id, text=messages["attractor"], parse_mode=ParseMode.HTML)
		context.bot.send_photo(chat_id=id, photo=data)
		logging.info("The attractor was sent to " + update.message.chat.username)
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=messages["error"], parse_mode=ParseMode.HTML)

def poem(update, context):
	logging.info("Creating a random poem now...")
	logging.info("Ready to send the poem to " + update.message.chat.username)
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=messages["poem"], parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=txt.get_poem(), parse_mode=ParseMode.HTML)

def random_number(update, context):
	logging.info("Sending a random dice to " + update.message.chat.username)
	m = update.message.text.split(" ")
	try:
		faces = int(m[1])
		r = mrd.diceroll(faces)
	except:
		r = mrd.diceroll(6)
	m = messages["number"] + "<b>" + str(r) + "</b>"
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

def random_sequence(update, context):
	logging.info("Sending a random sequence to " + update.message.chat.username)
	m = update.message.text.split(" ")
	try:
		faces = int(m[1])
		count = int(m[2])
		r = mrd.dicerolls(count, faces)
	except:
		r = mrd.dicerolls(6, 5)
	m = messages["number"] + "<b>" + str(r) + "</b>"
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

def print_help(update, context):
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=messages["help"], parse_mode=ParseMode.HTML)

def main():
	updater = Updater(security["token"], request_kwargs={'read_timeout': 5, 'connect_timeout': 5})
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("attractor", random_attractor))
	dp.add_handler(CommandHandler("poem", poem))
	dp.add_handler(CommandHandler("number", random_number))
	dp.add_handler(CommandHandler("sequence", random_sequence))
	dp.add_handler(CommandHandler("help", print_help))
	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()

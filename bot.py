from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import traceback, logging
import json as js
from messages import Messages
from assets import Assets
from text import Text
from myrandom import MyRandom

security = js.load(open("security.json"))
en_users = set()
msg = Messages()
ass = Assets()
txt = Text()
mrd = MyRandom()

def start(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " started the bot...")
	context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

def random_attractor(update, context):
	id = update.effective_chat.id
	data = ass.get_attractor()
	logging.info("Uploading attractor to Telegram servers...")
	try:
		context.bot.send_message(chat_id=id, text=msg.get_message("attractor", get_language(id)), parse_mode=ParseMode.HTML)
		context.bot.send_photo(chat_id=id, photo=data)
		logging.info("The attractor was sent to " + str(id))
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

def poem(update, context):
	logging.info("Creating a random poem now...")
	id = update.effective_chat.id
	l = get_language(id)
	logging.info("Ready to send the poem to " + str(id))
	context.bot.send_message(chat_id=id, text=msg.get_message("poem", l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=txt.get_poem(l), parse_mode=ParseMode.HTML)

def random_number(update, context):
	m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		faces = int(m[1])
		r = mrd.diceroll(faces)
	except:
		r = mrd.diceroll(6)
	m = msg.get_message("number", get_language(id)) + "<b>" + str(r) + "</b>"
	logging.info("Sending a random dice to " + str(id))
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

def random_sequence(update, context):
	m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		faces = int(m[1])
		count = int(m[2])
		r = mrd.dicerolls(count, faces)
	except:
		r = mrd.dicerolls(6, 5)
	m = msg.get_message("number", get_language(id)) + "<b>" + str(r) + "</b>"
	logging.info("Sending a random sequence to " + str(id))
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

def random_choice(update, context):
	in_m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		r = mrd.diceroll(len(in_m)-1)
		out_m = msg.get_message("choice", get_language(id)) + "<b>" + in_m[r] + "</b>"
		logging.info("Sending a choice to " + str(id))
		context.bot.send_message(chat_id=id, text=out_m, parse_mode=ParseMode.HTML)
	except:
		logging.info("Error while processing a choice for " + str(id))
		context.bot.send_message(chat_id=id, text=msg.get_message("empty", get_language(id)), parse_mode=ParseMode.HTML)

def print_help(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " asked for help...")
	context.bot.send_message(chat_id=id, text=msg.get_message("help", get_language(id)), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=msg.get_message("help2", get_language(id)), parse_mode=ParseMode.HTML)

def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

def select_language(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

def set_language(update, context, query):
	id = update.effective_chat.id
	if query == "l_1":
		logging.info("English is the language selected by " + str(id))
		en_users.add(id)
		context.bot.send_message(chat_id=id, text=msg.get_message("language2", get_language(id)), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + str(id))
		en_users.discard(id)
	context.bot.send_message(chat_id=id, text=msg.get_message("language3", get_language(id)), parse_mode=ParseMode.HTML)

def button_click(update, context):
	query = update.callback_query
	query.answer()
	if query.data.startswith("l"):
		set_language(update, context, query.data)

def main():
	if security["logging"] == "persistent":
		logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
						format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	elif security["logging"] == "debugging":
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	else:
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	updater = Updater(security["token"], request_kwargs={'read_timeout': 5, 'connect_timeout': 5})
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("attractor", random_attractor))
	dp.add_handler(CommandHandler("poem", poem))
	dp.add_handler(CommandHandler("number", random_number))
	dp.add_handler(CommandHandler("sequence", random_sequence))
	dp.add_handler(CommandHandler("choice", random_choice))
	dp.add_handler(CommandHandler("language", select_language))
	dp.add_handler(CommandHandler("help", print_help))
	dp.add_handler(CallbackQueryHandler(button_click))
	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()

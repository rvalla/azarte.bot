from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import traceback, logging
import json as js
from messages import Messages
from assets import Assets
from text import Text
from image import Image
from myrandom import MyRandom

config = js.load(open("config.json"))
en_users = set()
msg = Messages()
ass = Assets()
txt = Text()
img = Image()
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

#Starting textual alternatives...
def text(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " enter text tricks menu...")
	b = []
	if get_language(id) == 1:
		b = ["Poem", "Abstract", "Microtale", "Definition"]
	else:
		b = ["Poema", "Resumen", "Microrelato", "Definición"]
	keyboard = [[InlineKeyboardButton(text=b[0], callback_data="t_0"),
				InlineKeyboardButton(text=b[1], callback_data="t_1")],
				[InlineKeyboardButton(text=b[2], callback_data="t_2"),
				InlineKeyboardButton(text=b[3], callback_data="t_3")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("text", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

#Asking Text() for a random poem for the user...
def poem(update, context):
	logging.info("Creating a random poem now...")
	id = update.effective_chat.id
	l = get_language(id)
	logging.info("Ready to send the poem to " + str(id))
	context.bot.send_message(chat_id=id, text=msg.get_message("poem", l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=txt.get_poem(l), parse_mode=ParseMode.HTML)

#Asking Text() for a random abstract for the user...
def abstract(update, context):
	logging.info("Creating a random abstract now...")
	id = update.effective_chat.id
	l = get_language(id)
	logging.info("Ready to send the abstract to " + str(id))
	context.bot.send_message(chat_id=id, text=msg.get_message("abstract", l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=txt.get_abstract(l), parse_mode=ParseMode.HTML)

def microtale(update, context):
	id = update.effective_chat.id
	l = get_language(id)
	logging.info("Sending a microtale to " + str(id))
	context.bot.send_message(chat_id=id, text=msg.get_message("microtale", l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=txt.get_microtale(l), parse_mode=ParseMode.HTML)

def definition(update, context):
	id = update.effective_chat.id
	l = get_language(id)
	logging.info("Sending a fictional definition to " + str(id))
	context.bot.send_message(chat_id=id, text=msg.get_message("definition", l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=txt.get_definition(l), parse_mode=ParseMode.HTML)

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
	m = msg.get_message("number", get_language(id)) + "<b>" + txt.format_sequence(r) + "</b>"
	logging.info("Sending a random sequence to " + str(id))
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

#Selecting a word from the message for the user...
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

#Triggering /help command...
def print_help(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " asked for help...")
	context.bot.send_message(chat_id=id, text=msg.get_message("help", get_language(id)), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=msg.get_message("help2", get_language(id)), parse_mode=ParseMode.HTML)

#Allowing the user to chose the language (español - english)...
def select_language(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

def set_language(update, context, selection):
	id = update.effective_chat.id
	if selection == 1:
		logging.info("English is the language selected by " + str(id))
		en_users.add(id)
		context.bot.send_message(chat_id=id, text=msg.get_message("language2", get_language(id)), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + str(id))
		en_users.discard(id)
	context.bot.send_message(chat_id=id, text=msg.get_message("language3", get_language(id)), parse_mode=ParseMode.HTML)

#Distributing button replies...
def button_click(update, context):
	query = update.callback_query
	query.answer()
	q = query.data.split("_")
	if q[0] == "l":
		set_language(update, context, int(q[1]))
	elif q[0] == "t":
		decide_text(update, context, int(q[1]))

#Deciding what text option to trigger...
def decide_text(update, context, selection):
	if selection == 0:
		poem(update, context)
	elif selection == 1:
		abstract(update, context)
	elif selection == 2:
		microtale(update, context)
	elif selection == 3:
		definition(update, context)

#Sending a message to bot admin when an error occur...
def error_notification(update, context):
	id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + str(id)
	logging.info(m)
	context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Checking the user's selected language...
def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

#Configuring logging and getting ready to work...
def main():
	if config["logging"] == "persistent":
		logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
						format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	elif config["logging"] == "debugging":
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	else:
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	updater = Updater(config["token"], request_kwargs={'read_timeout': 5, 'connect_timeout': 5})
	dp = updater.dispatcher
	#dp.add_error_handler(error_notification)
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("attractor", random_attractor))
	dp.add_handler(CommandHandler("text", text))
	dp.add_handler(CommandHandler("number", random_number))
	dp.add_handler(CommandHandler("sequence", random_sequence))
	dp.add_handler(CommandHandler("choice", random_choice))
	dp.add_handler(CommandHandler("language", select_language))
	dp.add_handler(CommandHandler("help", print_help))
	dp.add_handler(CallbackQueryHandler(button_click))
	dp.bot.send_message(chat_id=config["admin_id"], text="The bot is online!", parse_mode=ParseMode.HTML)
	updater.start_polling(drop_pending_updates=True)
	updater.idle()

if __name__ == "__main__":
	main()

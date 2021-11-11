from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import traceback, logging, sched, time
import json as js
from messages import Messages
from assets import Assets
from text import Text
from image import Image
from myrandom import MyRandom

config = js.load(open("config.json")) #The configuration .json file (token included)
msg = Messages() #The class which knows what to say...
ass = Assets() #The class to access the different persistent assets...
txt = Text() #The class which create text alternatives...
img = Image() #The class which create visual alternatives...
mrd = MyRandom() #A class with some custom random functions...
en_users = set() #In this set the bot store ids from users who prefer to speak in English

#Starting the chat with a new user...
def start(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " started the bot...")
	context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

#A function to update random variables in creation classes...
def update_sources():
	logging.info("Updating random variables in creation classes...")
	txt.update()
	img.update()

#Starting image alternatives...
def image(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " enter image alternatives menu...")
	b = []
	if get_language(id) == 1:
		b = ["Lines", "Escape", "Clock", "Distribution", "Attractor", "Sorprise"]
	else:
		b = ["Líneas", "Escape", "Reloj", "Distribución", "Atractor", "Sorpresa"]
	keyboard = [[InlineKeyboardButton(text=b[0], callback_data="i_0"),
				InlineKeyboardButton(text=b[1], callback_data="i_1")],
				[InlineKeyboardButton(text=b[2], callback_data="i_2"),
				InlineKeyboardButton(text=b[3], callback_data="i_3")],
				[InlineKeyboardButton(text=b[4], callback_data="i_4"),
				InlineKeyboardButton(text=b[5], callback_data="i_5")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("image", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

#The function to deliver the requested image to the user...
def image_request(update, context, data, msg_tag, log_tag):
	id = update.effective_chat.id
	logging.info("Uploading " + log_tag + " to Telegram servers...")
	try:
		context.bot.send_message(chat_id=id, text=msg.get_message(msg_tag, get_language(id)), parse_mode=ParseMode.HTML)
		context.bot.send_photo(chat_id=id, photo=data)
		logging.info("The " + log_tag + " attractor was sent to " + str(id))
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

#Starting sound alternatives...
def sound(update, context):
	id = update.effective_chat.id
	logging.info(str(id) + " enter sound alternatives menu...")
	b = []
	if get_language(id) == 1:
		b = ["Sorprise"]
	else:
		b = ["Sorpresa"]
	keyboard = [[InlineKeyboardButton(text=b[0], callback_data="s_0")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("sound", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

#The function to deliver the requested sound to the user...
def sound_request(update, context, data, msg_tag, log_tag):
	id = update.effective_chat.id
	logging.info("Uploading "  + log_tag + " to Telegram servers...")
	try:
		context.bot.send_message(chat_id=id, text=msg.get_message(msg_tag, get_language(id)), parse_mode=ParseMode.HTML)
		context.bot.send_voice(chat_id=id, voice=data)
		logging.info("The " + log_tag + " sound was sent to " + str(id))
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

#The function to deliver the requested text to the user...
def text_request(update, context, data, id, l, msg_tag, log_tag):
	logging.info("Sending a " + log_tag + " to " + str(id))
	context.bot.send_message(chat_id=id, text=msg.get_message(msg_tag, l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=data, parse_mode=ParseMode.HTML)

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
	elif q[0] == "i":
		decide_image(update, context, int(q[1]))
	elif q[0] == "s":
		decide_sound(update, context, int(q[1]))

#Triggering requested image functions...
def decide_image(update, context, selection):
	if selection == 0:
		image_request(update, context, img.draw_lines(), "img_lines", "lines image")
	elif selection == 1:
		image_request(update, context, img.draw_escape(), "img_escape", "escape image")
	elif selection == 2:
		image_request(update, context, img.draw_clock(), "img_clock", "clock image")
	elif selection == 3:
		image_request(update, context, img.draw_distribution(), "img_distribution", "distribution image")
	elif selection == 4:
		image_request(update, context, ass.get_attractor(), "img_attractor", "attractor")
	elif selection == 5:
		image_request(update, context, ass.get_image_piece(), "img_surprise", "surprise image")

#Triggering requested sound functions...
def decide_sound(update, context, selection):
	if selection == 0:
		sound_request(update, context, ass.get_sound(), "sound_surprise", "random sound")

#Triggering requested text functions...
def decide_text(update, context, selection):
	id = update.effective_chat.id
	l = get_language(id)
	if selection == 0:
		text_request(update, context, txt.get_poem(l), id, l, "txt_poem", "random poem")
	elif selection == 1:
		text_request(update, context, txt.get_abstract(l), id, l, "txt_abstract", "random abstract")
	elif selection == 2:
		text_request(update, context, txt.get_microtale(l), id, l, "txt_microtale", "microtale")
	elif selection == 3:
		text_request(update, context, txt.get_definition(l), id, l, "txt_definition", "fictional definition")

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
	dp.add_error_handler(error_notification)
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("color", image))
	dp.add_handler(CommandHandler("text", text))
	dp.add_handler(CommandHandler("noise", sound))
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

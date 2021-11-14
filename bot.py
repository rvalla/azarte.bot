from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import traceback, logging
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
requests_counter = [0,0,0] #Counting the number of requests by category (image, sound, text)
update_cycle = 3 #Number of requests before updating configuration...

#Starting the chat with a new user...
def start(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " started the bot...")
	context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

#Starting image alternatives...
def image(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " enter image alternatives menu...")
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
		logging.info("The " + log_tag + " was sent to " + hide_id(id))
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

#Starting sound alternatives...
def sound(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " enter sound alternatives menu...")
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
		logging.info("The " + log_tag + " sound was sent to " + hide_id(id))
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

#Starting textual alternatives...
def text(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " enter text alternatives menu...")
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
	logging.info("Sending a " + log_tag + " to " + hide_id(id))
	context.bot.send_message(chat_id=id, text=msg.get_message(msg_tag, l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=data, parse_mode=ParseMode.HTML)

#Sending a random number to the user...
def random_number(update, context):
	m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		faces = int(m[1])
		r = mrd.diceroll(faces)
	except:
		r = mrd.diceroll(6)
	m = msg.get_message("number", get_language(id)) + "<b>" + str(r) + "</b>"
	logging.info("Sending a random dice to " + hide_id(id))
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

#Sending a random sequence to the user...
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
	logging.info("Sending a random sequence to " + hide_id(id))
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)

#Selecting a word from the message for the user...
def random_choice(update, context):
	in_m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		r = mrd.diceroll(len(in_m)-1)
		out_m = msg.get_message("choice", get_language(id)) + "<b>" + in_m[r] + "</b>"
		logging.info("Sending a choice to " + hide_id(id))
		context.bot.send_message(chat_id=id, text=out_m, parse_mode=ParseMode.HTML)
	except:
		logging.info("Error while processing a choice for " + hide_id(id))
		context.bot.send_message(chat_id=id, text=msg.get_message("empty", get_language(id)), parse_mode=ParseMode.HTML)

#Triggering /help command...
def print_help(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " asked for help...")
	context.bot.send_message(chat_id=id, text=msg.get_message("help", get_language(id)), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=msg.get_message("help2", get_language(id)), parse_mode=ParseMode.HTML)

#Advicing user not to chat with a bot...
def wrong_message(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " intended to chat...")
	context.bot.send_message(chat_id=id, text=msg.get_message("wrong_message", get_language(id)), parse_mode=ParseMode.HTML)

#Allowing the user to chose the language (español - english)...
def select_language(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

def set_language(update, context, selection):
	id = update.effective_chat.id
	if selection == 1:
		logging.info("English is the language selected by " + hide_id(id))
		en_users.add(id)
		context.bot.send_message(chat_id=id, text=msg.get_message("language2", get_language(id)), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + hide_id(id))
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
	context.bot.send_message(chat_id=id, text=msg.get_message("patience", l), parse_mode=ParseMode.HTML)
	increase_request(0, img)
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
	context.bot.send_message(chat_id=id, text=msg.get_message("patience", l), parse_mode=ParseMode.HTML)
	increase_request(1, img)
	if selection == 0:
		sound_request(update, context, ass.get_sound(), "sound_surprise", "random sound")

#Triggering requested text functions...
def decide_text(update, context, selection):
	id = update.effective_chat.id
	l = get_language(id)
	increase_request(2, txt)
	if selection == 0:
		text_request(update, context, txt.get_poem(l), id, l, "txt_poem", "random poem")
	elif selection == 1:
		text_request(update, context, txt.get_abstract(l), id, l, "txt_abstract", "random abstract")
	elif selection == 2:
		text_request(update, context, txt.get_microtale(l), id, l, "txt_microtale", "microtale")
	elif selection == 3:
		text_request(update, context, txt.get_definition(l), id, l, "txt_definition", "fictional definition")

#Deciding when to update random variables configuration...
def increase_request(c, object):
	global requests_counter
	requests_counter[c] += 1
	if requests_counter[c] > update_cycle:
		requests_counter[c] = 0
		object.update()
		logging.info("Updating class: " + str(c))

#Sending a message to bot admin when an error occur...
def error_notification(update, context):
	id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + hide_id(id)
	logging.info(m)
	context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Checking the user's selected language...
def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

#Hiding the first numbers of a chat id for the log...
def hide_id(id):
	s = str(id)
	return "****" + s[len(s)-4:]

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
	dp.add_handler(MessageHandler(Filters.text, wrong_message))
	dp.bot.send_message(chat_id=config["admin_id"], text="The bot is online!", parse_mode=ParseMode.HTML)
	updater.start_polling(drop_pending_updates=True)
	updater.idle()

if __name__ == "__main__":
	main()

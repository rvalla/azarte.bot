from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import traceback, logging
import json as js
import importlib as iplib
from usage import Usage
from messages import Messages
from assets import Assets
from text import Text
from image import Image
from gen import Genuary
from interaction import Interaction
from myrandom import MyRandom

config = js.load(open("config.json")) #The configuration .json file (token included)
us = Usage("usage.csv") #The class to save bot's usage data...
msg = Messages() #The class which knows what to say...
ass = Assets() #The class to access the different persistent assets...
txt = Text() #The class which create text alternatives...
img = Image() #The class which create visual alternatives...
gny = Genuary() #The class to process #genuary related requests...
ion = Interaction() #The class to make thing from user's messages...
mrd = MyRandom() #A class with some custom random functions...
en_users = set() #In this set the bot store ids from users who prefer to speak in English
WAITING = range(1) #Conversation states...
requests_counter = [0,0,0] #Counting the number of requests by category (image, sound, text)
update_cycle = 13 #Number of requests before updating configuration...

#Starting the chat with a new user...
def start(update, context):
	id = update.effective_chat.id
	logging.info(hide_id(id) + " started the bot...")
	us.add_start()
	context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

#Starting image alternatives...
def image(update, context):
	id = update.effective_chat.id
	b = []
	l = get_language(id)
	if l == 1:
		b = ["Lines", "Escape", "Clock", "Distribution", "Attractor", "Surprise"]
	else:
		b = ["Líneas", "Escape", "Reloj", "Distribución", "Atractor", "Sorpresa"]
	keyboard = [[InlineKeyboardButton(text=b[0], callback_data="i_0"),
				InlineKeyboardButton(text=b[1], callback_data="i_1")],
				[InlineKeyboardButton(text=b[2], callback_data="i_2"),
				InlineKeyboardButton(text=b[3], callback_data="i_3")],
				[InlineKeyboardButton(text=b[4], callback_data="i_4"),
				InlineKeyboardButton(text=b[5], callback_data="i_5")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("image", l), reply_markup=reply, parse_mode=ParseMode.HTML)

#The function to deliver the requested image to the user...
def image_request(update, context, id, data):
	try:
		context.bot.send_photo(chat_id=id, photo=data)
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

#Starting sound alternatives...
def sound(update, context):
	id = update.effective_chat.id
	b = []
	l = get_language(id)
	if l == 1:
		b = ["Score","Surprise"]
	else:
		b = ["Partitura","Sorpresa"]
	keyboard = [[InlineKeyboardButton(text=b[0], callback_data="s_0"),
				InlineKeyboardButton(text=b[1], callback_data="s_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("sound", l), reply_markup=reply, parse_mode=ParseMode.HTML)

#The function to deliver the requested sound to the user...
def sound_request(update, context, id, data):
	try:
		context.bot.send_audio(chat_id=id, audio=data)
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

#The function to deliver the requested video to the user...
def video_request(update, context, id, data):
	try:
		context.bot.send_video(chat_id=id, video=data)
	except:
		logging.info("Network error when uploading!")
		context.bot.send_message(chat_id=id, text=msg.get_message("error", get_language(id)), parse_mode=ParseMode.HTML)

#Starting textual alternatives...
def text(update, context):
	id = update.effective_chat.id
	b = []
	l = get_language(id)
	if l == 1:
		b = ["Poem", "Abstract", "Microtale", "Definition"]
	else:
		b = ["Poema", "Resumen", "Microrelato", "Definición"]
	keyboard = [[InlineKeyboardButton(text=b[0], callback_data="t_0"),
				InlineKeyboardButton(text=b[1], callback_data="t_1")],
				[InlineKeyboardButton(text=b[2], callback_data="t_2"),
				InlineKeyboardButton(text=b[3], callback_data="t_3")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("text", l), reply_markup=reply, parse_mode=ParseMode.HTML)

#The function to deliver the requested text to the user...
def text_request(update, context, id, l, data, msg_tag):
	context.bot.send_message(chat_id=id, text=msg.get_message(msg_tag, l), parse_mode=ParseMode.HTML)
	context.bot.send_message(chat_id=id, text=data, parse_mode=ParseMode.HTML)

#Starting an interaction...
def start_interaction(update, context):
	id = update.effective_chat.id
	context.bot.send_message(chat_id=id, text=msg.get_message("start_interaction", get_language(id)), parse_mode=ParseMode.HTML)
	return WAITING

#Ejecuting a text interaction...
def text_interaction(update, context):
	id = update.effective_chat.id
	m = update.message.text
	us.add_interaction(0)
	context.bot.send_message(chat_id=id, text=msg.get_message("text_interaction", get_language(id)), parse_mode=ParseMode.HTML)
	context.bot.send_chat_action(chat_id=id, action="UPLOAD_PHOTO")
	image_request(update, context, id, ion.build_message_curve(m))

#Ejecuting an image interaction...
def img_interaction(update, context):
	id = update.effective_chat.id
	photo = update.message.photo[-1].get_file()
	us.add_interaction(1)
	context.bot.send_message(chat_id=id, text=msg.get_message("img_interaction", get_language(id)), parse_mode=ParseMode.HTML)
	data, image = ion.build_chess_portrait(photo.download_as_bytearray())
	context.bot.send_message(chat_id=id, text=msg.build_chessportrait_message(data.split(";"), get_language(id)), parse_mode=ParseMode.HTML)
	context.bot.send_chat_action(chat_id=id, action="UPLOAD_PHOTO")
	image_request(update, context, id, image)

#Canceling the challenge without offering another one...
def wrong_interaction(update, context):
	id = update.effective_chat.id
	us.add_interaction(3)
	context.bot.send_message(id, text=msg.get_message("wrong_interaction", get_language(id)), parse_mode=ParseMode.HTML)

#Canceling the challenge without offering another one...
def cancel_interaction(update, context):
	id = update.effective_chat.id
	us.add_interaction(3)
	context.bot.send_message(id, text=msg.get_message("end_interaction", get_language(id)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Processing a #genuary request...
def genuary(update, context):
	id = update.effective_chat.id
	l = get_language(id)
	m = update.message.text.split(" ")
	d = None
	if len(m) == 2:
		try:
			d = int(m[1])
		except:
			d = gny.get_day()
	else:
		d = gny.get_day()
	context.bot.send_message(chat_id=id, text=msg.genuary_message(d, l), parse_mode=ParseMode.HTML)
	type, piece = gny.get_art(d)
	if not type == None:
		if type == "image":
			image_request(update, context, id, piece)
		elif type == "video_id":
			video_request(update, context, id, piece)
	else:
		context.bot.send_message(chat_id=id, text=msg.genuary_message(0, l), parse_mode=ParseMode.HTML)
	us.add_genuary()

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
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	us.add_number()

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
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	us.add_sequence()

#Selecting a word from the message for the user...
def random_choice(update, context):
	in_m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		r = mrd.diceroll(len(in_m)-1)
		out_m = msg.get_message("choice", get_language(id)) + "<b>" + in_m[r] + "</b>"
		context.bot.send_message(chat_id=id, text=out_m, parse_mode=ParseMode.HTML)
		us.add_choice(True)
	except:
		context.bot.send_message(chat_id=id, text=msg.get_message("empty", get_language(id)), parse_mode=ParseMode.HTML)
		us.add_choice(False)

#Selecting a word from the message for the user...
def qatar(update, context):
	in_m = update.message.text.split(" ")
	id = update.effective_chat.id
	try:
		game, comment = mrd.worldcup_match(get_language(id), in_m[1], in_m[2])
		context.bot.send_message(chat_id=id, text=game, parse_mode=ParseMode.HTML)
		context.bot.send_message(chat_id=id, text=comment, parse_mode=ParseMode.HTML)
		us.add_qatar(True)
	except:
		context.bot.send_message(chat_id=id, text=msg.get_message("qatar_error", get_language(id)), parse_mode=ParseMode.HTML)
		us.add_qatar(False)

#Triggering /help command...
def print_help(update, context):
	id = update.effective_chat.id
	m = msg.get_message("help", get_language(id)) + "\n" + msg.get_message("help2", get_language(id))
	context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	us.add_help()

#Advicing user not to chat with a bot...
def wrong_message(update, context):
	id = update.effective_chat.id
	if update.message.reply_to_message == None:
		context.bot.send_message(chat_id=id, text=msg.get_message("wrong_message", get_language(id)), parse_mode=ParseMode.HTML)
	else:
		context.bot.send_message(chat_id=id, text=msg.random_reply(get_language(id)), parse_mode=ParseMode.HTML)
	us.add_wrong_message()

#Allowing the user to chose the language (español - english)...
def select_language(update, context):
	id = update.effective_chat.id
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

def set_language(update, context, selection):
	id = update.effective_chat.id
	if selection == 1:
		en_users.add(id)
		context.bot.send_message(chat_id=id, text=msg.get_message("language2", get_language(id)), parse_mode=ParseMode.HTML)
		us.add_language(selection)
	else:
		en_users.discard(id)
		us.add_language(selection)
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
	id = update.effective_chat.id
	l = get_language(id)
	if selection == 0:
		context.bot.send_message(chat_id=id, text=msg.get_message("img_lines", l), parse_mode=ParseMode.HTML)
		context.bot.send_chat_action(chat_id=id, action="UPLOAD_PHOTO")
		image_request(update, context, id, img.draw_lines())
		increase_request(0, img)
		us.add_color(0)
	elif selection == 1:
		context.bot.send_message(chat_id=id, text=msg.get_message("img_escape", l), parse_mode=ParseMode.HTML)
		context.bot.send_chat_action(chat_id=id, action="UPLOAD_PHOTO")
		image_request(update, context, id, img.draw_escape())
		increase_request(0, img)
		us.add_color(1)
	elif selection == 2:
		context.bot.send_message(chat_id=id, text=msg.get_message("img_clock", l), parse_mode=ParseMode.HTML)
		context.bot.send_chat_action(chat_id=id, action="UPLOAD_PHOTO")
		image_request(update, context, id, img.draw_clock())
		increase_request(0, img)
		us.add_color(2)
	elif selection == 3:
		context.bot.send_message(chat_id=id, text=msg.get_message("img_distribution", l), parse_mode=ParseMode.HTML)
		context.bot.send_chat_action(chat_id=id, action="UPLOAD_PHOTO")
		increase_request(0, img)
		image_request(update, context, id, img.draw_distribution())
		us.add_color(3)
	elif selection == 4:
		context.bot.send_message(chat_id=id, text=msg.get_message("img_attractor", l), parse_mode=ParseMode.HTML)
		image_request(update, context, id, ass.get_attractor())
		us.add_color(4)
	elif selection == 5:
		context.bot.send_message(chat_id=id, text=msg.get_message("img_surprise", l), parse_mode=ParseMode.HTML)
		image_request(update, context, id, ass.get_image_piece())
		us.add_color(5)

#Triggering requested sound functions...
def decide_sound(update, context, selection):
	id = update.effective_chat.id
	l = get_language(id)
	if selection == 1:
		context.bot.send_message(chat_id=id, text=msg.get_message("sound_surprise", l), parse_mode=ParseMode.HTML)
		sound_request(update, context, id, ass.get_sound())
		us.add_noise(3)
	elif selection == 0:
		m = msg.build_score_message(txt.get_score_data(l), l)
		context.bot.send_message(chat_id=id, text=msg.get_message("sound_score", l), parse_mode=ParseMode.HTML)
		context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
		us.add_noise(2)

#Triggering requested text functions...
def decide_text(update, context, selection):
	id = update.effective_chat.id
	l = get_language(id)
	increase_request(2, txt)
	if selection == 0:
		text_request(update, context, id, l, txt.get_poem(l), "txt_poem")
		us.add_text(0)
	elif selection == 1:
		text_request(update, context, id, l, txt.get_abstract(l), "txt_abstract")
		us.add_text(1)
	elif selection == 2:
		text_request(update, context, id, l, txt.get_microtale(l), "txt_microtale")
		us.add_text(2)
	elif selection == 3:
		text_request(update, context, id, l, txt.get_definition(l), "txt_definition")
		us.add_text(3)

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
	us.add_error()
	context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Checking the user's selected language...
def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

#Sending usage data...
def bot_usage(update, context):
	id = update.effective_chat.id
	m = update.message.text.split(" ")
	if len(m) > 1 and m[1] == config["password"]:
		m = us.build_usage_message()
		context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	else:
		logging.info(hide_id(id) + " wanted to check bot usage data...")
		context.bot.send_message(chat_id=id, text=msg.get_message("intruder", get_language(id)), parse_mode=ParseMode.HTML)

#Saving usage data...
def save_usage(update, context):
	id = update.effective_chat.id
	m = update.message.text.split(" ")
	if len(m) > 1 and m[1] == config["password"]:
		us.save_usage()
		context.bot.send_message(chat_id=id, text="Datos guardados...", parse_mode=ParseMode.HTML)
	else:
		logging.info(hide_id(id) + " wanted to save bot usage data...")
		context.bot.send_message(chat_id=id, text=msg.get_message("intruder", get_language(id)), parse_mode=ParseMode.HTML)

#Function to print file ids from audios...
def print_audio_id(update, context):
	print(update.message.audio["file_id"])

#Function to print file ids from photos...
def print_photo_id(update, context):
	print(update.message.photo[0]["file_id"])

#Function to print file ids from videos...
def print_video_id(update, context):
	print(update.message.video["file_id"])

#Hiding the first numbers of a chat id for the log...
def hide_id(id):
	s = str(id)
	return "****" + s[len(s)-4:]

#Building the conversation handler...
def build_conversation_handler():
	handler = ConversationHandler(
		entry_points=[CommandHandler("interaction", start_interaction)],
		states={WAITING: [MessageHandler(Filters.text & ~Filters.command, text_interaction),
						MessageHandler(Filters.photo, img_interaction),
						MessageHandler(Filters.voice, wrong_interaction),
						MessageHandler(Filters.video, wrong_interaction)]},
				fallbacks=[MessageHandler(Filters.command, cancel_interaction)],
				per_chat=True, per_user=False, per_message=False)
	return handler

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
#	dp.add_error_handler(error_notification)
	dp.add_handler(build_conversation_handler(), group=1)
	dp.add_handler(MessageHandler(Filters.text & ~Filters.command, wrong_message), group=1)
	dp.add_handler(CommandHandler("start", start), group=2)
	dp.add_handler(CommandHandler("color", image), group=2)
	dp.add_handler(CommandHandler("text", text), group=2)
	dp.add_handler(CommandHandler("noise", sound), group=2)
	dp.add_handler(CommandHandler("genuary", genuary), group=2)
	dp.add_handler(CommandHandler("number", random_number), group=2)
	dp.add_handler(CommandHandler("sequence", random_sequence), group=2)
	dp.add_handler(CommandHandler("choice", random_choice), group=2)
	dp.add_handler(CommandHandler("qatar", qatar), group=2)
	dp.add_handler(CommandHandler("language", select_language), group=2)
	dp.add_handler(CommandHandler("help", print_help), group=2)
	dp.add_handler(CallbackQueryHandler(button_click), group=2)
	dp.add_handler(CommandHandler("botusage", bot_usage), group=2)
	dp.add_handler(CommandHandler("saveusage", save_usage), group=2)
	#dp.add_handler(MessageHandler(Filters.video & ~Filters.command, print_video_id))
	dp.bot.send_message(chat_id=config["admin_id"], text="The bot is starting!", parse_mode=ParseMode.HTML)
	if config["webhook"]:
		wh_url = "https://" + config["public_ip"] + ":" + str(config["webhook_port"]) + "/" + config["webhook_path"]
		updater.start_webhook(listen="0.0.0.0", port=config["webhook_port"], url_path=config["webhook_path"], key="webhook.key",
							cert="webhook.pem", webhook_url=wh_url, drop_pending_updates=True)
	else:
		updater.start_polling(drop_pending_updates=True)
		updater.idle()

if __name__ == "__main__":
	main()

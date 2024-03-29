import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("assets/text/es/messages_es.json"))
		self.msg_en = js.load(open("assets/text/en/messages_en.json"))
		self.replies_es = open("assets/text/es/random_replies.txt").readlines()
		self.replies_en = open("assets/text/en/random_replies.txt").readlines()
		self.errors_es = open("assets/text/es/random_apologies.txt").readlines()
		self.errors_en = open("assets/text/en/random_apologies.txt").readlines()

	#Returning a message from the database...
	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]
	
	#Returning a formated list...
	def get_list_text(self, the_list):
		m = ""
		for w in the_list:
			m += w
			m += ", "
		return m[:len(m)-2]

	#Returning a random reply...
	def random_reply(self, l):
		if l == 1:
			return rd.choice(self.replies_en)
		else:
			return rd.choice(self.replies_es)
	
	#Returning a random apology...
	def random_apology(self, l):
		if l == 1:
			return rd.choice(self.errors_en)
		else:
			return rd.choice(self.errors_es)

	#Formating a score message...
	def build_score_message(self, data, l):
		m = "<b>" + data[0] + "</b>\n"
		if l == 0:
			m += "Materiales necesarios: " + data[1] + "\n\n"
		else:
			m += "Materials needed: " + data[1] + "\n\n"
		m += "<i>" + data[2] + "</i>"
		return m

	#Building a chess portrait message...
	def build_chessportrait_message(self, game_data, l):
		m = ""
		if l == 1:
			m += "I decided to use a game in which <b>"
			m += game_data[0].split(",")[0]
			m += "</b> faced <b>"
			m += game_data[1].split(",")[0]
			m += "</b> ("
			m += game_data[3]
			m += ")."
		else:
			m += "Decidí usar una partida en la que <b>"
			m += game_data[0].split(",")[0]
			m += "</b> enfrentó a <b>"
			m += game_data[1].split(",")[0]
			m += "</b> ("
			m += game_data[3]
			m += ")."
		return m

	#Building #genuary messages...
	def genuary_message(self, day, l):
		key = "genuary_" + str(day)
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]

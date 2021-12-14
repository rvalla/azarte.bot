import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("messages_es.json"))
		self.msg_en = js.load(open("messages_en.json"))
		self.replies_es = open("assets/text/es/respuestasaleatorias.txt").readlines()
		self.replies_en = open("assets/text/en/randomreplies.txt").readlines()

	#Returning a message from the database...
	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]

	#Returning a random reply...
	def random_reply(self, l):
		if l == 1:
			return rd.choice(self.replies_en)
		else:
			return rd.choice(self.replies_es)

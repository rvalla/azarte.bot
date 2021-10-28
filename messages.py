import json as js

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("messages_es.json"))
		self.msg_en = js.load(open("messages_en.json"))

	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]

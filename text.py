import os
import random as rd

class Text():
	"The class the bot use to create random text..."

	def __init__(self):
		self.input_path = "assets/text/"
		self.input_list_es = [f for f in os.listdir(self.input_path + "es/") if not f.startswith(".")]
		self.input_list_en = [f for f in os.listdir(self.input_path + "en/") if not f.startswith(".")]
		self.input_tale_es = open(self.input_path + "es/" + rd.choice(self.input_list_es)).readlines()
		self.input_tale_en = open(self.input_path + "en/" + rd.choice(self.input_list_en)).readlines()

	def get_poem(self, l):
		p = ""
		lines = rd.choice([2,3,5,8,13,21])
		metric = rd.choice([1,2,2,3,3,3,3,5])
		p += self.get_title(l)
		for i in range(lines):
			p += self.get_line(l, metric)
		return p

	def get_line(self, l, m):
		line = ""
		source = None
		if l == 0:
			r = rd.randint(0, len(self.input_tale_es) - 1)
			source = self.input_tale_es[r].split(" ")
		elif l == 1:
			r = rd.randint(0, len(self.input_tale_en) - 1)
			source = self.input_tale_en[r].split(" ")
		for w in range(m):
			line += rd.choice(source)
			line += " "
		line += "\n"
		return line

	def get_title(self, l):
		if l == 0:
			r = rd.randint(0, len(self.input_tale_es) - 1)
			source = self.input_tale_es[r].split(" ")
		elif l == 1:
			r = rd.randint(0, len(self.input_tale_en) - 1)
			source = self.input_tale_en[r].split(" ")
		title = "<b>" + rd.choice(source) + "</b>" + "\n" + "\n"
		return title

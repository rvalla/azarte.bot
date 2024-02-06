import os
import random as rd

class Text():
	"The class the bot use to create random text..."

	def __init__(self):
		self.input_path = "assets/text/"
		self.input_list_es = [f for f in os.listdir(self.input_path + "es/random/") if not f.startswith(".")]
		self.input_list_en = [f for f in os.listdir(self.input_path + "en/random/") if not f.startswith(".")]
		self.input_tale_es = open(self.input_path + "es/random/" + rd.choice(self.input_list_es)).readlines()
		self.input_tale_en = open(self.input_path + "en/random/" + rd.choice(self.input_list_en)).readlines()
		self.fiction_dict_es = open(self.input_path + "es/dictionary.csv").readlines()
		self.fiction_dict_en = open(self.input_path + "en/dictionary.csv").readlines()
		self.microtales_es = open(self.input_path + "es/microtales.txt").readlines()
		self.microtales_en = open(self.input_path + "en/microtales.txt").readlines()
		self.scores_es = open(self.input_path + "es/scores.csv").readlines()[1:]
		self.scores_en = open(self.input_path + "en/scores.csv").readlines()[1:]

	#Updating sources...
	def update(self):
		self.input_tale_es = open(self.input_path + "es/random/" + rd.choice(self.input_list_es)).readlines()
		self.input_tale_en = open(self.input_path + "en/random/" + rd.choice(self.input_list_en)).readlines()

	#Function to build a random poem...
	def get_poem(self, l):
		p = ""
		lines = rd.choice([5,8,8,8,13,21])
		metric = rd.choice([1,2,3,3,3,4,5,6])
		p += self.get_title(l)
		for i in range(lines):
			p += self.get_line(l, metric)
		return p

	#Function to build a random poem line...
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

	#Deciding a poem's title...
	def get_title(self, l):
		if l == 0:
			r = rd.randint(0, len(self.input_tale_es) - 1)
			source = self.input_tale_es[r].split(" ")
		elif l == 1:
			r = rd.randint(0, len(self.input_tale_en) - 1)
			source = self.input_tale_en[r].split(" ")
		title = "<b>" + rd.choice(source) + "</b>" + "\n" + "\n"
		return title

	#Building a random abstract...
	def get_abstract(self, l):
		abstract = ""
		if l == 0:
			abstract = self.build_abstract(self.input_tale_es)
		elif l == 1:
			abstract = self.build_abstract(self.input_tale_en)
		return abstract

	#Building a random abstract...
	def build_abstract(self, source):
		count = len(source)
		r = rd.randint(1,count-1)
		text = source[0]
		for i in range(5):
			text += source[(r+i)%count]
		text += source[count-1]
		text = " ".join(text.splitlines())
		text = "".join(text.split("."))
		words = text.split(" ")
		count = len(words)
		r = rd.randint(5,20)
		abstract = " " + words[0] + " " + words [1] + " " + words[2]
		while r < count - 3:
			for i in range(3):
				abstract += " " + words[r+i]
			r += rd.randint(5,20)
		abstract += " " + words[count-1] + "."
		return abstract[1:].capitalize()

	#Returning a fictional definition from the database...
	def get_definition(self, l):
		d = ""
		if l == 0:
			d = rd.choice(self.fiction_dict_es)
		elif l == 1:
			d = rd.choice(self.fiction_dict_en)
		return self.format_definition(d)

	#Formating a fictional definition...
	def format_definition(self, s):
		a = s.split(";")
		d = "<b>" + a[0] + "</b> "
		d += "<i>(" + a[1] + ")</i>: "
		d += a[2]
		return d

	#Returning a microtale from the database...
	def get_microtale(self, l):
		mt = "<i>"
		if l == 0:
			mt += rd.choice(self.microtales_es)
		else:
			mt +=  rd.choice(self.microtales_en)
		mt += "</i>"
		return mt

	#Returning a score from the database...
	def get_score_data(self, l):
		data = None
		if l == 0:
			data = rd.choice(self.scores_es)
		else:
			data = rd.choice(self.scores_en)
		return data.split(";")

	#Formating a number sequence...
	def format_sequence(self, s):
		f = ""
		for v in s:
			f += str(v) + " "
		return f

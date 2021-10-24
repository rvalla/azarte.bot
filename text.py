import os
import random as rd

class Text():
	"The class the bot use to create random text..."

	def __init__(self):
		self.input_path = "assets/text/"
		self.input_list = os.listdir(self.input_path)
		self.cleanFileList(self.input_list)
		self.input_tale_lines = open(self.input_path + rd.choice(self.input_list)).readlines()

	def get_poem(self):
		p = ""
		lines = rd.choice([2,3,5,8,13,21])
		metric = rd.choice([1,2,2,3,3,3,3,5])
		r = rd.randint(0, len(self.input_tale_lines) - 1)
		source = self.input_tale_lines[r].split(" ")
		p += "<b>" + rd.choice(source) + "</b>" + "\n" + "\n"
		for l in range(lines):
			r = rd.randint(0, len(self.input_tale_lines) - 1)
			source = self.input_tale_lines[r].split(" ")
			for w in range(metric):
				p += rd.choice(source)
				p += " "
			p += "\n"
		return p

	def cleanFileList(self, filelist):
		f = 0
		while (f < len(filelist)):
			if filelist[f].startswith("."):
				del filelist[f]
			else:
				f += 1

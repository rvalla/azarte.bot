import os
import re
import random as rd

class Assets():
	"The class the bot use to access the assets..."

	def __init__(self):
		self.img_path = "assets/img/"
		self.attractor_list = os.listdir(self.img_path + "attractors/")
		self.cleanFileList(self.attractor_list)

	def get_attractor(self):
		return self.img_path + "attractors/" + rd.choice(self.attractor_list)

	def cleanFileList(self, filelist):
		f = 0
		while (f < len(filelist)):
			if filelist[f].startswith("."):
				del filelist[f]
			else:
				f += 1

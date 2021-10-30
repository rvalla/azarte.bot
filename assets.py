import os
import random as rd

class Assets():
	"The class the bot use to access the assets..."

	def __init__(self):
		self.img_path = "assets/img/"
		self.attractor_list = [f for f in os.listdir(self.img_path + "attractors/") if not f.startswith(".")]

	def get_attractor(self):
		attractor = open(self.img_path + "attractors/" + rd.choice(self.attractor_list), "rb")
		return attractor

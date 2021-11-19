import os
import random as rd

class Assets():
	"The class the bot use to access the assets..."

	def __init__(self):
		self.attractor_list, self.img_pieces_list, self.sounds_list = self.build_ids_lists("assets/online_resources_ids.csv")

	def get_attractor(self):
		return rd.choice(self.attractor_list)

	def get_image_piece(self):
		return rd.choice(self.img_pieces_list)

	def get_sound(self):
		return rd.choice(self.sounds_list)

	def build_ids_lists(self, path):
		lines = open(path).readlines()[1:]
		attractors = []
		img_pieces = []
		sounds = []
		for l in lines:
			data = l.split(";")
			if data[1] == "img_attractor":
				attractors.append(data[0])
			elif data[1] == "img_surprise":
				img_pieces.append(data[0])
			elif data[1] == "audio_surprise":
				sounds.append(data[0])
		return attractors, img_pieces, sounds

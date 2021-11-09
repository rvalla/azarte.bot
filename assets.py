import os
import random as rd

class Assets():
	"The class the bot use to access the assets..."

	def __init__(self):
		self.img_path = "assets/img/"
		self.audio_path = "assets/audio/"
		self.attractor_list = [f for f in os.listdir(self.img_path + "attractors/") if not f.startswith(".")]
		self.img_pieces_list = [f for f in os.listdir(self.img_path + "pieces/") if not f.startswith(".")]
		self.sounds_list = [f for f in os.listdir(self.audio_path + "random/") if not f.startswith(".")]

	def get_attractor(self):
		attractor = open(self.img_path + "attractors/" + rd.choice(self.attractor_list), "rb")
		return attractor

	def get_image_piece(self):
		image = open(self.img_path + "pieces/" + rd.choice(self.img_pieces_list), "rb")
		return image

	def get_sound(self):
		sound = open(self.audio_path + "random/" + rd.choice(self.sounds_list), "rb")
		return sound

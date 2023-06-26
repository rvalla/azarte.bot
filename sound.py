import os
import math
import numpy as np
import random as rd
import time as tm

class Sound():
	"The class the bot uses to process sounds..."

	def __init__(self):
		self.background = (210,210,192)
		self.w = 1080
		self.h = 1920
		self.lw = 3
		self.scale = rd.randint(5,12)
		self.angles = self.get_angles(rd.randint(3,16))
		self.sizes = self.get_sizes(len(self.angles))
		self.mask_path = "assets/img/masks/"
		self.input_mask_list = [f for f in os.listdir(self.mask_path) if not f.startswith(".")]

	def update(self):
		self.scale = rd.randint(5,20)
		self.angles = self.get_angles(rd.randint(3,16))
		self.sizes = self.get_sizes(len(self.angles))

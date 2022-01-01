import numpy as np
from PIL import Image as im

class NCanvas():
	"The canvas to draw with pixels for genuary..."

	def __init__(self, width, height):
		self.background = (255,255,255)
		self.w = width
		self.h = height
		self.c = (self.w/2, self.h/2)
		self.data = np.full((h, w, 3), self.background)

	#Setting up pixels colors...
	def paint_pixel(self, color, x, y, width):
		for i in range(width):
			self.paint_pixel(color, i+x, i+y)

	#Setting up a pixel color...
	def paint_pixel(self, color, x, y):
		self.data[y][x] = color

	#Function to save image...
	def save(self, filepath, filename):
		data = np.array(np.round(self.data), dtype="uint8")
		image = im.fromarray(data)
		image.save(filepath + filename + ".jpg")

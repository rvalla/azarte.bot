import numpy as np
from PIL import Image as im

class NCanvas():
	"The canvas to draw with pixels for genuary..."

	def __init__(self, width, height, background):
		self.background = background
		self.w = width
		self.h = height
		self.data = np.full((self.h, self.w, 3), self.background)

	#Setting up pixels colors...
	def paint_pixel(self, color, x, y, width):
		for i in range(width):
			self.paint_pixel(color, i+x, i+y)

	#Setting up a pixel color...
	def paint_pixel(self, color, x, y):
		self.data[y][x] = color

	#Function to save image...
	def get_image(self):
		data = np.array(np.round(self.data), dtype="uint8")
		image = im.fromarray(data)
		return image

	#Function to show image...
	def show(self):
		data = np.array(np.round(self.data), dtype="uint8")
		image = im.fromarray(data)
		image.show()

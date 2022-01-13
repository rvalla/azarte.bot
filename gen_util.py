from io import BytesIO
import math
import time as tm
import random as rd
from PIL import Image as im

class GenUtil():
	"A class to join interesting functions for genuary..."

	#Getting a random color based on time in rgb space...
	def get_time_color(self):
		t = tm.localtime()
		r = t.tm_sec * 2
		g = t.tm_min * 2
		b = t.tm_hour * 5
		return (r,g,b)

	#Getting a random color based on time in rgba space...
	def get_time_alpha_color(self, alpha):
		t = tm.localtime()
		r = t.tm_sec * 2
		g = t.tm_min * 2
		b = t.tm_hour * 5
		return (r,g,b, alpha)

	#Moving a color randomly in rgb color space...
	def move_color(self, color, motion):
		r = rd.randint(-motion,motion)
		g = rd.randint(-motion,motion)
		b = rd.randint(-motion,motion)
		return ((color[0]+r)%255,(color[1]+g)%255,(color[2]+b)%255)

	#A function to invert a color in rgb color space...
	def invert_color(self, color):
		return (255-color[0],255-color[1],255-color[2])

	#Moving a color randomly in rgba color space...
	def move_alpha_color(self, color, motion):
		r = rd.randint(-motion,motion)
		g = rd.randint(-motion,motion)
		b = rd.randint(-motion,motion)
		a = rd.randint(-motion,motion)
		return ((color[0]+r)%255,(color[1]+g)%255,(color[2]+b)%255,(color[3]+a)%255)

	#A function to invert a color in rgba color space...
	def invert_alpha_color(self, color):
		return (255-color[0],255-color[1], 255-color[2],255-color[3])

	#Changing a color with control...
	def color_grading(self, color, destiny, speed):
		r = color[0] + round((destiny[0] - color[0]) * speed)
		g = color[1] + round((destiny[0] - color[1]) * speed)
		b = color[2] + round((destiny[0] - color[2]) * speed)
		return (r,g,b)

	#A function to get an image combining two images...
	def mean_image(self, back_image, top_image, name):
		back_image.convert("RGBA")
		top_image.convert("RGBA").resize(back_image.size)
		mask = im.new("L", back_image.size, 127)
		new = im.composite(back_image, top_image, mask)
		new.save(name + ".jpg")

	#A function to paint a mask with an input image...
	def mask_merge(self, background, top_image, name):
		top_image.convert("RGBA")
		mask = im.open(self.mask_path + rd.choice(self.input_mask_list)).convert("L").resize(top_image.size)
		back_image = im.new("RGBA", top_image.size, background)
		new = im.composite(back_image, top_image, mask)
		new.save(name + ".jpg")

	#The function to store the Image object in a byte stream...
	def create_image(self, image):
		file = BytesIO()
		image.save(file, "jpeg", quality=85, optimize=True)
		file.name = "random_creation.jpg"
		file.seek(0)
		return file

	#A function to build a random signal...
	def random_signal(self, base_frequency, base_amplitude, components):
		signal = []
		for c in range(components):
			fq = rd.random() * base_frequency
			a = base_amplitude / (c + 1)
			fase = rd.random() * math.pi * 2
			signal.append((fq, a, fase))
		return signal

	#A function to build a harmonic signal...
	def harmonic_signal(self, base_frequency, base_amplitude, components):
		signal = []
		for c in range(components):
			fq = base_frequency * (c + 1)
			a = base_amplitude / (c + 1)
			fase = rd.random() * math.pi * 2
			signal.append((fq, a, fase))
		return signal

	#A function to draw a rectangle with rectangles...
	def gen_rectangle(self, canvas, w, h, location, density, colors, color_motion, factors, size_factor, constant_size):
		steps = [h / density[0], w / density[1]]
		thinghw = [steps[1] * size_factor, steps[0] * size_factor]
		color_count = len(colors)
		active_color = rd.randint(0,color_count-1)
		aux_size = thinghw
		for i in range(density[0]):
			active_color = (active_color+i)%color_count
			c = colors[active_color]
			if not constant_size:
				aux_size = (aux_size[0] , (thinghw[1] + i%(4*steps[1])))
			for j in range(density[1]):
				x = location[1] + steps[1] / 2 + (j * factors[0])%density[1] * steps[1]
				y = location[0] + steps[0] / 2 + (j * factors[1] + i * factors[0])%density[0] * steps[0]
				center = (x, y)
				if not constant_size:
					aux_size = (thinghw[0] + j%(4*steps[0]), aux_size[1])
				canvas.draw_rectangle(c, center, aux_size)
				c = self.move_alpha_color(c, color_motion)
			colors[active_color] = c

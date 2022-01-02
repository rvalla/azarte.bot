import random as rd
import datetime as dt
import numpy as np
from PIL import Image as im
from gen_util import GenUtil
from gen_drawing_canvas import DCanvas
from gen_data_canvas import NCanvas

ut = GenUtil()

class Genuary():
	"The class the bot uses to be part of genuary..."

	def __init__(self):
		self.start = dt.date(2022,1,1)
		self.factors = [1,2,3,7,13,17,19,40,41,43,89]
		self.w = 1080
		self.h = 1080

	#Checking which day of the cycle is today...
	def get_day(self):
		today = dt.date.today()
		d = (today - self.start).days
		return d%31 + 1

	#Building a piece for this particual day...
	def get_art(self, day):
		if day == 1:
			bg = (255,255,255)
			c = [ut.get_time_alpha_color(30)]
			c.append(ut.invert_alpha_color(c[0]))
			f = [rd.choice(self.factors),rd.choice(self.factors)]
			return "image", self.gen_1(self.w, self.h, bg, c, f, 0.8, [160, 80])
		elif day == 2:
			path = "assets/img/dithering/dithering_" + str(rd.randint(1,9)) + ".jpg"
			border = rd.randint(0,120) + 60
			return "image", self.gen_2(path, border, (255,255,255))
		else:
			return None, "Nothing to send..."

	#Building day 1 piece...
	def gen_1(self, w, h, background, colors, factors, sizefactor, margins):
		canvas = DCanvas(w,h,background)
		steps = [(w - margins[0] * 2) / 100, (h - margins[1] * 2) / 100]
		thingwh = [steps[0] * 1, steps[1] * 1]
		color_count = len(colors)
		active_color = 0
		size = thingwh
		for i in range(100):
			active_color = (active_color + i) % color_count
			c = colors[active_color]
			size = (size[0] , (thingwh[1] + i%(7*steps[1])))
			for j in range(100):
				x = margins[0] + steps[0] / 2 + (j * factors[0])%100 * steps[0]
				y = margins[1] + steps[1] / 2 + (i * factors[1] + j * factors[0])%100 * steps[1]
				center = (x, y)
				size = (thingwh[0] + j%(7*steps[0]), size[1])
				canvas.draw_rectangle(c, center, size)
				c = ut.move_color(c, 1)
			colors[active_color] = c
		return ut.create_image(canvas.canvas)

	#Building day 2 piece...
	def gen_2(self, input_path, border, background):
		input = np.array(im.open(input_path))
		margins = [input.shape[1] // 9, input.shape[0] // 9]
		hw = [input.shape[1] + margins[0] * 2, input.shape[0] + margins[1] * 2]
		canvas = NCanvas(hw[0],hw[1],background)
		for r in range(input.shape[0]):
			channel = rd.choice([0,1,2])
			for c in range(input.shape[1]):
				color = input[r][c]
				v = color[channel]
				if v < border:
					v = 0
				else:
					v = 255
				e = border - v
				color[channel] = v
				input[r][(c+1)%input.shape[1]][channel] += e
				canvas.paint_pixel(color, c + margins[0], r + margins[1])
		return ut.create_image(canvas.get_image())

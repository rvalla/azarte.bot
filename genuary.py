import random as rd
import datetime as dt
from gen_util import GenUtil
from gen_drawing_canvas import DCanvas

ut = GenUtil()

class Genuary():
	"The class the bot uses to be part of genuary..."

	def __init__(self):
		self.start = dt.date(2022,1,1)
		self.primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
		self.w = 1080
		self.h = 1080
		self.alpha_colors = [(30,30,30,30),(120,120,120,30),(120,30,60,30),(30,120,60,30),(30,60,120,30),(30,120,120,30)]
		self.colors = [(30,30,30),(120,120,120),(120,30,60),(30,120,60),(30,60,120),(30,120,120)]

	#Checking which day of the cycle is today...
	def get_day(self):
		today = dt.date.today()
		d = (today - self.start).days
		return d%31 + 1

	#Building a piece for this particual day...
	def get_art(self, day):
		if day == 1:
			bg = (255,255,255)
			c = [rd.choice(self.alpha_colors),rd.choice(self.alpha_colors)]
			f = [rd.choice(self.primes),rd.choice(self.primes)]
			return "image", self.gen_1(self.w, self.h, bg, c, f, 0.8, [160, 80])
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

import random as rd
import datetime as dt
import numpy as np
from PIL import Image as im
from gen_util import GenUtil
from gen_drawing_canvas import DCanvas
from gen_data_canvas import NCanvas
from gen_virus import GenVirus
from gen_pixel import GenPixel

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
			c = [ut.get_time_alpha_color(30)]
			c.append(ut.invert_alpha_color(c[0]))
			f = [rd.choice(self.factors),rd.choice(self.factors)]
			return "image", self.gen_1(self.w, self.h, (255,255,255), c, f, 0.8, [80, 80])
		elif day == 2:
			path = "assets/img/dithering/dithering_" + str(rd.randint(1,8)) + ".jpg"
			border = rd.randint(0,120) + 60
			return "image", self.gen_2(path, border, (255,255,255))
		elif day == 3:
			c = ut.get_time_color()
			bg = ut.invert_color(c)
			return "image", self.gen_3(self.w, self.h, [160,160], bg, c, 90)
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

	#Building a day 3 piece...
	def gen_3(self, w, h, margins, background, color, days):
		aw = w - margins[1] * 2
		ah = h - margins[0] * 2
		pixels = self.load_gen_pixels(ah, aw, background)
		virus = self.load_virus(color)
		x = aw // 2
		y = ah // 2
		pixels[y][x].infection(virus)
		d = 0
		while d < days:
			self.simulate_day(aw, ah, virus, pixels)
			d += 1
			print(d, end="\r")
		return ut.create_image(self.paint_gen_3(w,h,aw,ah,margins,pixels,background))

	def load_gen_pixels(self,ah,aw,background):
		pixels = []
		for h in range(ah):
			l = []
			for w in range(aw):
				l.append(GenPixel(w,h,background))
			pixels.append(l)
		return pixels

	def load_virus(self, color):
		t = rd.uniform(0.03,0.1)
		m = rd.randint(2,5)
		d = rd.randint(3,5)
		virus = GenVirus(color, t, m, d)
		return virus

	def simulate_day(self, aw, ah, virus, pixels):
		for h in range(ah):
			for w in range(aw):
				if pixels[h][w].is_infected:
					for i in range(-2,2):
						for j in range(-2,2):
							t = rd.random()
							if t < virus.threshold:
								pixels[(h+i)%ah][(w+j)%aw].infection(virus)
					pixels[h][w].update()
		virus.update()

	def paint_gen_3(self, w, h, aw, ah, margins, pixels, background):
		canvas = NCanvas(h, w, background)
		for h in range(ah):
			for w in range(aw):
				canvas.paint_pixel(pixels[h][w].c, w + margins[1], h + margins[0])
		return canvas.get_image()

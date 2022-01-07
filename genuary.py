import math
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
			return "image", self.gen_1(self.w - 240, self.h - 240, (255,255,255), c, 0.8, [120, 120])
		elif day == 2:
			path = "assets/img/dithering/dithering_" + str(rd.randint(1,8)) + ".jpg"
			border = rd.randint(0,120) + 60
			return "image", self.gen_2(path, border, (255,255,255))
		elif day == 3:
			c = ut.get_time_color()
			bg = ut.invert_color(c)
			return "image", self.gen_3(self.w - 160, self.h - 160, [80,80], bg, c, 90)
		elif day == 4:
			c = [ut.get_time_alpha_color(30)]
			c.append(ut.invert_alpha_color(c[0]))
			angle_var = [rd.random() * math.pi * 2, rd.random() * math.pi * 2]
			return "image", self.gen_4(self.w - 160, self.h - 160, [80,80], (255,255,255), c, [500,500], angle_var, 300)
		elif day == 5:
			c = ut.get_time_color()
			c2 = ut.invert_color(c)
			return "image", self.gen_5(self.w - 320, self.h - 320, (255,255,255), [c, c2], 0.8, [160,160], [5,5], 20)
		elif day == 6:
			c = ut.get_time_color()
			off = rd.random() * 75 + 25
			s = rd.randint(5,15)
			signal_A = ut.random_signal(rd.random()*5, 10, 5)
			signal_B = ut.random_signal(rd.random()*5, 10, 3)
			return "image", self.gen_6(self.w, self.h, [100,100], (255,255,255), c, signal_A, signal_B, 0.1, off, s, 0.005)
		else:
			return None, "Nothing to send..."

	#Building day 1 piece...
	def gen_1(self, w, h, background, colors, sizefactor, margins):
		f = [rd.choice(self.factors),rd.choice(self.factors)]
		canvas = self.gen_1_piece(w, h, background, colors, f, sizefactor, margins)
		return ut.create_image(canvas.canvas)

	def gen_1_piece(self, w, h, background, colors, factors, sizefactor, margins):
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
				x = margins[1] + steps[1] / 2 + (j * factors[0])%100 * steps[1]
				y = margins[0] + steps[0] / 2 + (j * factors[1] + i * factors[0])%100 * steps[0]
				center = (x, y)
				size = (thingwh[0] + j%(7*steps[0]), size[1])
				canvas.draw_rectangle(c, center, size)
				c = ut.move_color(c, 1)
			colors[active_color] = c
		return canvas

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
		c = rd.randint(0,5)
		contacts = (c - 5, c)
		virus = GenVirus(color, contacts, t, m, d)
		return virus

	def simulate_day(self, aw, ah, virus, pixels):
		infected_list = self.infected_list(ah, aw, pixels)
		for p in infected_list:
			for i in range(virus.contacts[0],virus.contacts[1]):
				for j in range(virus.contacts[0],virus.contacts[1]):
					t = rd.random()
					if t < virus.threshold:
						pixels[(p[0]+i)%ah][(p[1]+j)%aw].infection(virus)
			pixels[p[0]][p[1]].update()
		virus.update()

	def infected_list(self, ah, aw, pixels):
		l = []
		for h in range(ah):
			for w in range(aw):
				if pixels[h][w].is_infected:
					l.append((h,w))
		return l

	def paint_gen_3(self, w, h, aw, ah, margins, pixels, background):
		canvas = NCanvas(h, w, background)
		for h in range(ah):
			for w in range(aw):
				canvas.paint_pixel(pixels[h][w].c, w + margins[1], h + margins[0])
		return canvas.get_image()

	#Building a day 4 piece...
	def gen_4(self, w, h, margins, background, colors, steps, angle_var, lines):
		field = self.load_field(angle_var, steps)
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] * 2, background)
		self.paint_field(w,h,canvas,lines,colors,margins,field,steps)
		return ut.create_image(canvas.canvas)

	def load_field(self, angle_var, steps):
		a = rd.random() * math.pi
		field = []
		for y in range(steps[0]):
			list = []
			a += y/steps[0] * angle_var[0]
			for x in range(steps[1]):
				a += x/steps[0] + angle_var[1]
				list.append(a)
			field.append(list)
		return field

	def paint_field(self, w, h, canvas, lines, colors, margins, field, steps):
		distance = h / lines
		for l in range(lines):
			p = (rd.randint(0,w), rd.randint(0,h))
			c_count = len(colors)
			for c in range(c_count):
				colors[c] = ut.move_color(colors[c], 5)
			t = 0
			offset = rd.randint(1,200)+200
			while t < 500:
				if self.is_point_in(p, w, h):
					a = self.look_for_angle(p, w, h, field, steps)
					s = math.sin(0.1 * t) * 10
					np = self.get_new_point(p, a, s)
					canvas.draw_circle(colors[(t//offset)%c_count], (np[0]+margins[1],np[1]+margins[0]), s)
					p = np
				t += 1

	def look_for_angle(self, point, w, h, field, steps):
		x = math.floor(point[0] / w * (steps[1] - 1))
		y = math.floor(point[1] / h * (steps[0] - 1))
		return field[y][x]

	def get_new_point(self, last_point, angle, scale):
		x = math.cos(angle) * scale
		y = math.sin(angle) * scale
		return (last_point[0] + x, last_point[1] + y)

	#Building a day 5 piece...
	def gen_5(self, w, h, background, colors, sizefactor, margins, cuts, cuts_width):
		f = [13,0]
		canvas = self.gen_1_piece(w, h, background, colors, f, sizefactor, margins)
		self.destroy_square(1, canvas, 20, cuts, background, cuts_width)
		self.destroy_square(0, canvas, 20, cuts, background, cuts_width)
		return ut.create_image(canvas.canvas)

	def destroy_square(self, x, canvas, noise, cuts, color, width):
		y = (x + 1) % 2
		as1 = rd.sample(range(canvas.hw[x]), cuts[x])
		as2 = rd.sample(range(canvas.hw[x]), cuts[x])
		as1.sort()
		as2.sort()
		b1 = 0 + rd.randint(0, noise)
		b2 = canvas.hw[y] - b1
		for a1, a2 in zip(as1,as2[::-1]):
			if y == 0:
				canvas.draw_line(color, width, (a1,b1), (a2,b2))
			elif y == 1:
				canvas.draw_line(color, width, (b1, a1), (b2, a2))

	#Building a day 6 piece...
	def gen_6(self, w, h, margins, background, color, signal_A, signal_B, resolution, offset, scale, speed):
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] * 2, background)
		signal_width = round(w - offset)
		signal_A_h = h // 3
		signal_B_h = 2 * signal_A_h
		for l in range(signal_width):
			x1 = l + margins[1]
			x2 = l + offset + margins[1]
			y1 = signal_A_h + self.get_signal_y(signal_A, resolution * l, scale) + margins[0]
			y2 = signal_B_h + self.get_signal_y(signal_B, resolution * l, scale) + margins[0]
			canvas.draw_line(color, 0, (x1,y1), (x2,y2))
			color = ut.move_color(color, 2)
			color = ut.color_grading(color, background, speed)
		return ut.create_image(canvas.canvas)

	def get_signal_y(self, signal, angle, scale):
		y = math.pi / 2
		for s in signal:
			y += math.sin(s[0] * angle) * s[1] * scale
		return y

	#Util...
	def is_point_in(self, point, w, h):
		is_in = True
		if (point[0] < 0 or point[0] > w or point[1] < 0 or point[1] > h):
			is_in = False
		return is_in

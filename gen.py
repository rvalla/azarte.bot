from io import BytesIO
import math
import numpy as np
import random as rd
import datetime as dt
import time as tm
import numpy as np
from PIL import Image as im, ImageDraw as idraw

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
			return "image", self.gen_1(self.w, self.h, [160, 160], (255,255,255), c, 10, 0.8)
		elif day == 2:
			path = "assets/img/dithering/dithering_" + str(rd.randint(1,8)) + ".jpg"
			border = rd.randint(0,120) + 60
			return "image", self.gen_2(path, border, (255,255,255))
		elif day == 3:
			c = ut.get_time_color()
			bg = ut.invert_color(c)
			return "image", self.gen_3(self.w - 160, self.h - 160, [80,80], bg, c, 75)
		elif day == 4:
			c = [ut.get_time_alpha_color(30)]
			c.append(ut.invert_alpha_color(c[0]))
			angle_var = [rd.random() * math.pi * 2, rd.random() * math.pi * 2]
			return "image", self.gen_4(self.w - 160, self.h - 160, [80,80], (255,255,255), c, [500,500], angle_var, 300)
		elif day == 5:
			c = ut.get_time_alpha_color(30)
			c2 = ut.invert_alpha_color(c)
			return "image", self.gen_5(self.w, self.h, [240,240], (255,255,255), [c, c2], 10, 0.8, [5,5], 20)
		elif day == 6:
			c = ut.get_time_color()
			off = rd.random() * 75 + 25
			s = rd.randint(5,15)
			signal_A = ut.random_signal(rd.random()*5, 10, 5)
			signal_B = ut.random_signal(rd.random()*5, 10, 3)
			return "image", self.gen_6(self.w, self.h, [100,100], (255,255,255), c, signal_A, signal_B, 0.1, off, s, 0.005)
		elif day == 7:
			c = ut.get_time_color()
			p = rd.randint(13,89)
			return "image", self.gen_7(self.w, self.h, [160,160], (255,255,255), c, p, 2)
		elif day == 8:
			c = ut.get_time_color()
			signal = ut.random_signal(rd.random(), 10, 3)
			s = rd.randint(5,15)
			speed = rd.random() / 25
			return "image", self.gen_8(self.w, self.h, [160,160], (255,255,255), c, signal, 0.1, s, 34, speed)
		elif day == 9:
			colors = [ut.get_time_color()]
			colors.append(ut.invert_color(colors[0]))
			windows_c = [ut.get_time_alpha_color(100)]
			windows_c.append(ut.move_alpha_color(windows_c[0],50))
			windows_c.append(ut.move_alpha_color(windows_c[0],50))
			buildings = rd.randint(13,21)
			return "image", self.gen_9(self.w, self.h//3, [40,40], (255,255,255), colors, 25, windows_c, 8, buildings)
		elif day == 10:
			c = ut.get_time_color()
			lines = rd.randint(21,89)
			scale = rd.randint(5,13)
			width = 200 // lines
			return "image", self.gen_10(self.w, self.h, [160,160], (255,255,255), c, 10, lines, width, scale)
		elif day == 13:
			c = [ut.get_time_alpha_color(100)]
			c.append(ut.move_alpha_color(c[0], 25))
			c.append(ut.move_alpha_color(c[0], 30))
			c.append(ut.invert_alpha_color(c[0]))
			return "image", self.gen_13(self.w, self.h, [200,200], (255,255,255), [6,60], c, [3,18], 0.6)
		elif day == 14:
			center = [self.w/2, self.h/2]
			init_p = [center[0] + 100 + rd.random()*200, center[1] + 100 + rd.random()*200]
			init_v = [rd.random()*2-1,rd.random()*2-1]
			return "image", self.gen_14(self.w, self.h, (255,255,255), center, init_p, init_v, 20)
		elif day == 15:
			color = ut.get_time_color()
			center = [self.w/2, self.h/2]
			init_p = [center[0] + 100 + rd.random()*200, center[1] + 100 + rd.random()*200]
			init_v = [rd.random()*2-1,rd.random()*2-1]
			return "image", self.gen_15(self.w, self.h, (255,255,255), color, 2, center, init_p, init_v, 20)
		elif day == 16:
			color = ut.get_time_color()
			signal = ut.random_signal(rd.random(), 10, 3)
			motion = rd.randint(1,3)
			lines = [760,380,190]
			choice = rd.choice(range(len(lines)))
			return "image", self.gen_16(self.w - 320, self.h - 320, [160,160], (255,255,255), color, motion,
											signal, 5, lines[choice], 200 + rd.randint(0,200))
		elif day == 17:
			colors = [ut.get_time_color()]
			colors.append(ut.invert_color(colors[0]))
			colors.append((rd.randint(30,200),rd.randint(30,200),rd.randint(30,200)))
			return "image", self.gen_17(self.w, self.h, [160,160], (255,255,255), colors, 2, 300, 10, 5)
		elif day == 18:
			file_id = "BAACAgEAAxkBAAIRjGHnR14aIMTPwKrFo0woqi9cLeK-AAKiAQACcRI5R5V8hqrHCN0KIwQ"
			return "video_id", file_id
		elif day == 25:
			return None, "Nothing to send..."
		else:
			return None, "Nothing to send..."

	#Building day 1 piece...
	def gen_1(self, w, h, margins, background, colors, color_motion, size_factor):
		factors = [rd.choice(self.factors),rd.choice(self.factors)]
		canvas = DCanvas(w, h, background)
		ut.gen_rectangle(canvas, w - margins[1] * 2, h - margins[0] * 2, margins, [100,100], colors, color_motion,
							factors, size_factor, False)
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
	def gen_5(self, w, h, margins, background, colors, color_motion, size_factor, cuts, cuts_width):
		factors = [rd.choice([13,17,19,23]),0]
		canvas = DCanvas(w, h, background)
		ut.gen_rectangle(canvas, w - margins[1] * 2, h - margins[0] * 2, margins, [100,100], colors,
							color_motion, factors, size_factor, False)
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

	#Building a day 7 piece...
	def gen_7(self, w, h, margins, background, color, points, line_width):
		color = GenColor(color)
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] * 2, background)
		points = self.load_LeWitt_points(w, h, points, margins)
		for p1 in range(len(points)):
			for p2 in points[p1:]:
				canvas.draw_line(color.c, line_width, points[p1], p2)
				color.translate(2)
		return ut.create_image(canvas.canvas)

	def load_LeWitt_points(self, w, h, points, margins):
		xs = rd.sample(range(0,w),points)
		ys = rd.sample(range(0,h),points)
		list = []
		for x, y in zip(xs, ys):
			list.append((margins[1] + x, margins[0] + y))
		return list

	#Building a day 8 piece...
	def gen_8(self, w, h, margins, background, color, signal, resolution, scale, lines, speed):
		color = GenColor(color)
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] * 2, background)
		self.paint_single_curve(canvas, w, h, margins, color, background, signal, lines, resolution, scale, speed)
		return ut.create_image(canvas.canvas)

	def paint_single_curve(self, canvas, w, h, margins, color, background, signal, lines, resolution, scale, speed):
		signal_h = h // 2
		for l in range(lines):
			for s in range(w):
				x = s + margins[1]
				y = signal_h + self.get_signal_y(signal, resolution * s, scale) + margins[0]
				canvas.draw_point(color.c, (x,y))
			signal_h += 1
			color.degrade(background, speed)

	#Building a day 9 piece...
	def gen_9(self, w, h, margins, background, colors, color_motion, windows_colors, windows_density, buildings):
		night = rd.choice([True, False])
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] * 2, background)
		b_widths, b_heights = self.building_heights(w, h, buildings)
		self.skyline(canvas, w, h, b_widths, b_heights, colors, buildings, color_motion, margins)
		self.fill_buildings(canvas, w, h, b_widths, b_heights, buildings, color_motion, windows_colors, margins, night)
		return ut.create_image(canvas.canvas)

	def skyline(self, canvas, w, h, b_widths, b_heights, colors, buildings, color_motion, margins):
		x = margins[1] + w / 2
		y = margins[0] + h / 2
		canvas.draw_rectangle(colors[0], (x,y), (w, h))
		for b in range(1, buildings + 1):
			x = b_widths[b-1] * b - b_widths[b-1] / 2 + margins[1]
			y = margins[0] + h - b_heights[b - 1] / 2
			canvas.draw_rectangle(colors[1], (x,y), (b_widths[b-1],b_heights[b-1]))
			colors[1] = ut.move_color(colors[1], color_motion)

	def fill_buildings(self, canvas, w, h, b_widths, b_heights, buildings, color_motion, windows_colors, margins, night):
		h_margin = b_widths[0] / 10
		level_height = b_widths[0] / 2 - 2 * h_margin
		start_x = margins[1]
		start_y = 2 * margins[0] + h
		for b in range(buildings):
			levels = math.floor((b_heights[b] - 10) / (level_height + h_margin))
			row = rd.choice([1,2,2,3,3,3,4])
			self.windows(canvas, w, h, start_x, start_y, levels, h_margin, level_height, b_widths[b], row, color_motion, windows_colors, margins, night)
			start_x += b_widths[b]

	def windows(self, canvas, w, h, start_x, start_y, levels, margin, height, total_width, row, color_motion, windows_colors, margins, night):
		width = self.windows_widths(margin, total_width, row)
		floor = h + margins[0]
		density = [rd.randint(3,6),rd.randint(5,10)]
		color = rd.choice(windows_colors)
		motion = rd.randint(color_motion // 2, color_motion)
		factors = [rd.choice([11,13,17,19]),rd.choice([0,0,0,17,19,23])]
		for r in range(row):
			x = start_x + margin + r * (width + margin)
			for l in range(levels):
				window_on = True
				if night:
					if rd.random() < 0.5:
						window_on = False
				if window_on:
					y = floor - margin - height - l * (height + margin)
					ut.gen_rectangle(canvas, width, height, [y,x], density, [color], motion, factors, 1, True)

	def windows_widths(self, margin, total_width, row):
		width = 0
		if row == 1:
			width = total_width - 2 * margin
		else:
			width = (total_width - margin) / row - margin
		return width

	def building_heights(self, w, h, buildings):
		bw = []
		step = w / buildings
		for w in range(buildings):
			bw.append(step)
		w / buildings
		bh = []
		min = h / 3
		step = h / 9
		if buildings > 6:
			heights = 6
		else:
			heights = buildings
		hs = rd.sample(range(0,6),heights)
		for i in range(buildings):
			bh.append(hs[i%len(hs)] * step + min)
		return bw, bh

	#Building a day 10 piece...
	def gen_10(self, w, h, margins, background, c, color_motion, lines, line_w, scale):
		color = GenColor(c)
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] * 2, background)
		self.run(canvas, w, h, margins, color, color_motion, lines, line_w, scale)
		return ut.create_image(canvas.canvas)

	def run(self, canvas, w, h, margins, color, color_motion, lines, line_w, scale):
		y = h // 2 + margins[0]
		x = w // 3 + margins[1]
		for l in range(lines):
			self.draw_path(canvas, w, h, margins, (x,y), math.pi + rd.random() * 6, scale, line_w, color)
			color.translate(color_motion)

	def draw_path(self, canvas, w, h, margins, origin, angle, scale, line_w, color):
		p = origin
		np = self.get_new_point(p, angle, scale)
		noise = rd.random() / 100 - 0.005
		while self.is_line_trap(margins, h, np):
			canvas.draw_line(color.c, line_w, p, np)
			p = np
			np = self.get_new_point(p, angle, scale)
			angle += noise
		angle = self.turn(angle)
		if not self.is_line_out(w, np):
			self.draw_path(canvas, w, h, margins, p, angle, scale, line_w, color)

	def is_line_trap(self, margins, h, p):
		if p[0] < margins[1] or p[1] < margins[0] or p[1] > margins[0] + h:
			return False
		else:
			return True

	def is_line_out(self, w, p):
		if p[0] > w:
			return True
		else:
			return False

	def turn(self, angle):
		return angle + rd.random() - 0.5

	#Building a day 13 piece...
	def gen_13(self, w, h, margins, background, density, colors, color_motion, size_factor):
		densities = [density, [density[0], round(density[1] * 0.4)]]
		canvas = DCanvas(w, h, background)
		self.hexagram(canvas, w, h, margins, colors, color_motion, size_factor, densities)
		return ut.create_image(canvas.canvas)

	def hexagram(self, canvas, w, h, margins, colors, color_motion, size_factor, densities):
		height = (h - margins[0] * 2) / 11
		space = (w - margins[1] * 2) / 5
		strips = self.get_strips()
		y = margins[0]
		for s in strips:
			factors = self.get_factors(s)
			color = colors[s%len(colors)]
			location = [y, margins[1]]
			if s < 2:
				if s == 0:
					ut.gen_rectangle(canvas, w - margins[1] * 2, height, location, densities[0], [color], color_motion[0], factors, size_factor, True)
				else:
					ut.gen_rectangle(canvas, w - margins[1] * 2, height, location, densities[0], [color], color_motion[1], factors, size_factor, True)
			else:
				if s == 2:
					ut.gen_rectangle(canvas, 2 * space, height, location, densities[1], [color], color_motion[0], factors, size_factor, True)
					location[1] += space * 3
					ut.gen_rectangle(canvas, 2 * space, height, location, densities[1], [color], color_motion[0], factors, size_factor, True)
				else:
					ut.gen_rectangle(canvas, 2 * space, height, location, densities[1], [color], color_motion[1], factors, size_factor, True)
					location[1] += space * 3
					ut.gen_rectangle(canvas, 2 * space, height, location, densities[1], [color], color_motion[1], factors, size_factor, True)
			y += 2 * height

	def get_factors(self, case):
		primes = [13,17,19,23]
		return [primes[case], 0]

	def get_strips(self):
		strips = []
		for s in range(6):
			strips.append(self.flip_coins())
		return strips

	#John Cage used 3 coins to decide each line of an hexagram. Then mapped each hexagram to a table...
	def flip_coins(self):
		cs = 0
		for c in range(3):
			cs += self.flip_coin()
		return cs

	def flip_coin(self):
		return rd.choice([0,1])

	#Building a day 14 piece...
	def gen_14(self, w, h, background, center, initial_position, initial_velocity, g_constant):
		pendulum = GenPendulum(center, initial_position, initial_velocity, g_constant, False, 1)
		canvas = DCanvas(w, h, background)
		self.oscillation(canvas, pendulum, GenColor((0,0,0)), 0, 50000, 1)
		return ut.create_image(canvas.canvas)

	def oscillation(self, canvas, pendulum, color, color_motion, times, grains):
		for t in range(times):
			pendulum.update()
			self.drop_sand(canvas, pendulum, color, grains)
			color.move(color_motion)

	#Building a day 15 piece...
	def gen_15(self, w, h, background, color, color_motion, center, initial_position, initial_velocity, g_constant):
		pendulum = GenPendulum(center, initial_position, initial_velocity, g_constant, False, 1)
		canvas = DCanvas(w, h, background)
		self.oscillation(canvas, pendulum, GenColor(color), color_motion, 8000, 20)
		return ut.create_image(canvas.canvas)

	#Building a day 16 piece...
	def gen_16(self, w, h, margins, background, c, color_motion, signal, scale, lines, lines_h):
		color = GenColor(c)
		color.d = self.set_color_directions()
		axis = h // 2 + margins[0]
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] *  2, background)
		self.draw_gradient_lines(canvas, w, axis, margins, lines, lines_h, signal, scale, color, color_motion)
		return ut.create_image(canvas.canvas)

	def draw_gradient_lines(self, canvas, w, axis, margins, lines, lines_h, signal, scale, color, color_motion):
		step = w // lines
		y_offset = axis - lines_h // 2
		signal_resolution = w / lines * 0.05
		for l in range(lines):
			x = l*step + margins[1]
			y = - self.get_signal_y(signal, l * signal_resolution, scale) + y_offset
			canvas.draw_line(color.c, 0, (x,y), (x,y+lines_h))
			color.overflow(color_motion)

	def set_color_directions(self):
		r = rd.choice([-1,1])
		g = rd.choice([-1,1])
		b = rd.choice([-1,1])
		return [r,g,b]

	#Building a day 17 piece...
	def gen_17(self, w, h, margins, background, the_colors, lines_w, lines_height, loops, loop_size):
		lines_h, lines_m, ys = self.get_y_data(h, margins, lines_height)
		colors = [GenColor(c) for c in the_colors]
		canvas = DCanvas(w + margins[1] * 2, h + margins[0] *  2, background)
		self.draw_getting_close_lines(canvas, w, margins, colors, ys, lines_h, loops, loop_size, lines_w)
		return ut.create_image(canvas.canvas)

	def draw_getting_close_lines(self, canvas, w, margins, colors, ys, lines_h, loops, loop_size, lines_w):
		step = w / (loops * loop_size)
		for l in range(loops):
			offset = l * step * loop_size + margins[1] + step / 2
			for t in range(loop_size):
				x = t*step + offset
				for i in range(3):
					canvas.draw_line(colors[i].c, lines_w, (x,ys[i]), (x,ys[i]+lines_h))
			self.update_getting_close_colors(colors)

	def get_y_data(self, h, margins, lines_h):
		ys = []
		margin = h / 3 - lines_h
		ys.append(margins[0] + margin / 2)
		ys.append(ys[0] + lines_h + margin)
		ys.append(ys[1] + lines_h + margin)
		return lines_h, margin, ys

	def update_getting_close_colors(self, colors):
		for c in range(3):
			colors[c].getting_close(colors[rd.choice([0,1,2])].c)

	#Util...
	def is_point_in(self, point, w, h):
		is_in = True
		if (point[0] < 0 or point[0] > w or point[1] < 0 or point[1] > h):
			is_in = False
		return is_in

	def get_new_point(self, last_point, angle, scale):
		x = math.cos(angle) * scale
		y = math.sin(angle) * scale
		return (last_point[0] + x, last_point[1] + y)

	def get_signal_y(self, signal, angle, scale):
		y = math.pi / 2
		for s in signal:
			y += math.sin(s[0] * (angle + s[2])) * s[1] * scale
		return y

	def drop_sand(self, canvas, pendulum, color, grains):
		for g in range(grains): #dropping grains in each position...
			noise_x = g * (rd.random() * 10 - 5)
			noise_y = g * (rd.random() * 10 - 5)
			x = pendulum.p[0] + noise_x
			y = pendulum.p[1] + noise_y
			canvas.draw_point(color.c, (x,y))

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

class DCanvas():
	"The canvas to draw with Pillow for genuary..."

	def __init__(self, width, height, background):
		self.background = background
		self.hw = [height,width]
		self.c = (self.hw[0]/2, self.hw[1]/2)
		self.canvas = im.new("RGB",(self.hw[1], self.hw[0]),self.background)
		self.draw = idraw.Draw(self.canvas)

	#Function to draw a point...
	def draw_point(self, c, p):
		self.draw.point(p, fill=c)

	#Function to draw a line...
	def draw_line(self, c, w, a, b):
		self.draw.line([a,b], fill=c, width=w)

	#Function to draw a circle...
	def draw_circle(self, color, c, d):
		a = (c[0] - d/2, c[1] - d/2)
		b = (c[0] + d/2, c[1] + d/2)
		self.draw.ellipse([a,b], fill=color, outline=None)

	#Function to draw a rectangle...
	def draw_rectangle(self, color, center, size):
		a = (center[0] - size[0]/2, center[1] - size[1] / 2)
		b = (a[0] + size[0], a[1] + size[1])
		self.draw.rectangle([a,b], fill=color, outline=None)

	#Function to draw a rounded rectangle...
	def draw_rounded_rectangle(self, color, center, size, r):
		a = (center[0] - size[0]/2, center[1] - size[1] / 2)
		b = (a[0] + size[0], a[1] + size[1])
		self.draw.rounded_rectangle([a,b], radius=r, fill=color, outline=None)

	#Function to write a message...
	def write(self, x, y, cell, message, font, color):
		self.draw.text((x,y), message, anchor="mm", font=font, fill=color)

	#Function to save the drawing...
	def save(self, filepath, filename):
		self.canvas.save(filepath + filename + ".jpg")

class GenColor():
	"A class to creat a living color..."

	def __init__(self, color):
		self.o = color
		self.c = color
		self.d = [1,1,1]

	#Moving a color randomly in rgb color space...
	def move(self, motion):
		r = (self.c[0] + rd.randint(-motion,motion))%255
		g = (self.c[1] + rd.randint(-motion,motion))%255
		b = (self.c[2] + rd.randint(-motion,motion))%255
		self.c = (r,g,b)

	#Moving a color in its direction...
	def translate(self, motion):
		self.check_directions(motion)
		r = self.c[0] + motion * self.d[0]
		g = self.c[1] + motion * self.d[1]
		b = self.c[2] + motion * self.d[2]
		self.c = (r,g,b)

	#Moving a color without stopping...
	def overflow(self, motion):
		r = (self.c[0] + motion * self.d[0])%255
		g = (self.c[1] + motion * self.d[1])%255
		b = (self.c[2] + motion * self.d[2])%255
		self.c = (r,g,b)

	#Moving a color without stopping independtly...
	def independent_overflow(self, motion):
		r = (self.c[0] + motion[0] * self.d[0])%255
		g = (self.c[1] + motion[1] * self.d[1])%255
		b = (self.c[2] + motion[2] * self.d[2])%255
		self.c = (r,g,b)

	#Getting close to another color...
	def getting_close(self, the_other_color):
		r = self.c[0] + (the_other_color[0] - self.c[0]) // 8
		g = self.c[1] + (the_other_color[1] - self.c[1]) // 8
		b = self.c[2] + (the_other_color[2] - self.c[2]) // 8
		self.c = (r,g,b)

	#Checking if it is posible to move...
	def check_directions(self, motion):
		for d in range(len(self.d)):
			v = self.c[d] + motion
			if self.c[d] < 0 or self.c[d] > 255:
				self.d[d] = self.d[d] * -1

	#A function to invert the color in rgb color space...
	def invert(self):
		self.c = (255-self.c[0],255-self.c[1],255-self.c[2])

	#Changing a color with control...
	def degrade(self, destiny, speed):
		r = self.c[0] + round((destiny[0] - self.c[0]) * speed)
		g = self.c[1] + round((destiny[0] - self.c[1]) * speed)
		b = self.c[2] + round((destiny[0] - self.c[2]) * speed)
		self.c = (r,g,b)

	#Reseting to original color...
	def reset(self):
		self.c = self.o

class GenPendulum():
	"A class to move a pendulum..."

	def __init__(self, center, initial_position, initial_velocity, g_constant, degrades, degrade_step):
		self.c = np.array(center)
		self.p = np.array(initial_position)
		self.s = np.array(initial_velocity)
		self.a = np.array([0.0,0.0])
		self.m = 1.0
		self.g = g_constant #the famous G constant...
		self.degrades = degrades #taking into account the loose of mass...
		self.degrade_step = degrade_step #mass lost in each update...

	def update(self):
		self.update_acceleration()
		self.update_speed()
		self.p += self.s

	def update_acceleration(self):
		difference = self.c - self.p
		magnitude = self.get_sq_magnitude(difference)
		if self.degrades:
			magnitude = self.friction(magnitude)
		self.a = self.set_vector(difference, magnitude)

	def update_speed(self):
		self.s += self.a

	def friction(self, magnitude):
		if self.m > 0.5:
			self.m -= self.degrade_step
		self.s = self.s * self.m
		return magnitude * self.m

	def get_sq_magnitude(self, vector):
		m = self.g / (vector[0]*vector[0] + vector[1]*vector[1])
		if m < 0.1:
			m = 0.1
		elif m > 8:
			m = 8
		return m

	def set_vector(self, difference, magnitude):
		a = self.get_unit_vector(difference)
		a[0] = a[0] * magnitude
		a[1] = a[1] * magnitude
		return a

	def get_unit_vector(self, vector):
		v = np.array([0.0,0.0])
		v[0] = (vector[0] / (abs(vector[0]) + abs(vector[1])))
		v[1] = (vector[1] / (abs(vector[0]) + abs(vector[1])))
		return v

class GenPixel():
	"A class to work with an interesting pixel..."

	def __init__(self, x, y, background):
		self.x = x
		self.y = y
		self.c = background
		self.is_infected = False
		self.is_immune = False
		self.infection_evol = None
		self.infection_end = None

	def infection(self, virus):
		if self.is_infected == False and self.is_immune == False:
			self.infection_evol = 0
			self.c = virus.color
			self.is_infected = True
			self.infection_end = virus.duration

	def update(self):
		self.infection_evol += 1
		if self.infection_evol > self.infection_end:
			self.is_infected = False
			self.is_immune = True

class GenVirus():
	"A class to infect pixels..."

	def __init__(self, color, contacts, threshold, mutation_cycle, duration):
		self.color = color
		self.contacts = contacts
		self.threshold = threshold
		self.mutation_cycle = mutation_cycle
		self.last_mutation = 0
		self.age = 0
		self.duration = duration

	def update(self):
		self.age += 1
		if self.age - self.last_mutation > self.mutation_cycle:
			self.threshold = self.threshold + rd.random() / 200
			self.color = ut.move_color(self.color, 15)
			self.last_mutation = self.age

class GenCurve():
	"A class to work with a curve..."

	resolution = math.pi/6

	def __init__(self, x, y, angle, scale, curve):
		self.p = (x,y) #current position
		self.a = angle #current angle
		self.s = scale #scale
		self.curve = curve #description of the curve
		self.points = None #points relative to (0,0)
		self.build_points()

	def get_points(self):
		points = [self.p]
		for p in self.points:
			points.append((self.p[0] + p[0], self.p[1] + p[1]))
		return points

	def random_curve(self):
		steps = rd.randint(1,5)
		self.curve = []
		for s in range(steps):
			a = rd.random() / 2
			count = rd.randint(5,30)
			self.curve.append([count, a])
		self.build_points()

	def build_points(self):
		self.points = []
		last_point = (0,0)
		angle = self.a
		self.points.append(last_point)
		for data in self.curve:
			for p in range(data[0]):
				new_point = self.new_point((last_point), angle)
				self.points.append(new_point)
				last_point = new_point
				angle += data[1]

	def new_point(self, last_point, angle):
		x = math.cos(angle) * self.s
		y = math.sin(angle) * self.s
		return (last_point[0] + x, last_point[1] + y)

	def move(self, x, y):
		self.p = (self.p[0] + x, self.p[1] + y)

	def mutation(self):
		for data in self.curve:
			data[0] += rd.randint(0,4) - 2
		self.build_points()

ut = GenUtil()

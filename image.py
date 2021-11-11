import os
from io import BytesIO
import math
import random as rd
import time as tm
from PIL import Image as im, ImageDraw as idraw, ImageFilter as ifil

class Image():
	"The class the bot uses to process the images..."

	def __init__(self):
		self.background = (210,210,192)
		self.w = 1080
		self.h = 1920
		self.c = (self.w/2, self.h/2)
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

	def draw_escape(self):
		i = im.new("RGB",(self.w, self.h),self.background)
		margin = self.w / 10
		d = idraw.Draw(i)
		m = rd.choice([0,1])
		c = self.get_time_color()
		for r in range(200):
			p = (self.w/2,self.h/3*2)
			c = self.move_color(c,3)
			while self.is_point_in(p, margin):
				np = self.get_dice_point(m, p)
				self.draw_line(d,c,self.lw,p,np)
				p = np
		return self.create_image(i)

	def draw_clock(self):
		i = im.new("RGB",(self.w, self.h),self.background)
		cs = (self.w/10, self.h/10)
		d = idraw.Draw(i)
		t = tm.localtime()
		s = (math.pi * 2 * t.tm_sec / 60) - math.pi / 2
		m = (math.pi * 2 * t.tm_min / 60) - math.pi / 2
		h = (math.pi * 2 * (t.tm_hour%12) / 12) - math.pi / 2
		p1 = (self.c[0] + math.cos(h) * cs[0] * 2, self.c[1] + math.sin(h) * cs[1] * 2)
		p2 = (self.c[0] + math.cos(m) * cs[0] * 3, self.c[1] + math.sin(m) * cs[1] * 3)
		p3 = (self.c[0] + math.cos(s) * cs[0] * 4, self.c[1] + math.sin(s) * cs[1] * 4)
		op1 = (self.c[0] + math.cos(h) * cs[0] * 2, self.c[1] - math.sin(h) * cs[1] * 2)
		op2 = (self.c[0] - math.cos(m) * cs[0] * 3, self.c[1] + math.sin(m) * cs[1] * 3)
		op3 = (self.c[0] - math.cos(s) * cs[0] * 4, self.c[1] - math.sin(s) * cs[1] * 4)
		color = self.get_time_color()
		d.polygon([op1,op2,op3], fill=color, outline=None)
		self.draw_circle(d, (170,30,30), p1, cs[0]*1.66)
		self.draw_circle(d, (75,150,75), p2, cs[0]*1.33)
		self.draw_circle(d, (35,70,180), p3, cs[0])
		return self.create_image(i)

	def draw_lines(self):
		i = im.new("RGB",(self.w, self.h),self.background)
		d = idraw.Draw(i)
		c = self.get_time_color()
		p1 = (self.w/2,self.h/5)
		p2 = (self.w/2,self.h/5*4)
		margin = self.w / 10
		for r in range(3000):
			np1 = self.get_random_motion(p1)
			np2 = self.get_random_motion(p2)
			if self.is_point_in(np1, margin) and self.is_point_in(np2, margin):
				self.draw_line(d,c,1,np1,np2)
				p1 = np1
				p2 = np2
				c = self.move_color(c,1)
		return self.create_image(i)

	def get_random_motion(self, last_point):
		x = rd.randint(-30,30)
		y = rd.randint(-30,30)
		return (last_point[0] + x, last_point[1] + y)

	def get_dice_point(self, mode, last_point):
		c = len(self.angles)
		if mode == 0:
			r = rd.randint(0,c-1)
			x = math.cos(self.angles[r]) * self.sizes[r] * self.scale
			y = math.sin(self.angles[r]) * self.sizes[r] * self.scale
		else:
			r = round((rd.randint(0,c-1) + rd.randint(0,c-1))/2)
			x = math.cos(self.angles[r]) * self.sizes[r] * self.scale
			y = math.sin(self.angles[r]) * self.sizes[r] * self.scale
		return (last_point[0] + x, last_point[1] + y)

	def is_point_in(self, point, margin):
		is_in = True
		if (point[0] < margin or point[0] > self.w - margin
				or point[1] < margin or point[1] > self.h - margin):
			is_in = False
		return is_in

	def draw_line(self, draw, c, w, a, b):
		draw.line([a,b], fill=c, width=w)

	def draw_circle(self, draw, color, c, d):
		a = (c[0] - d/2, c[1] - d/2)
		b = (c[0] + d/2, c[1] + d/2)
		draw.ellipse([a,b], fill=color, outline=None)

	def get_time_color(self):
		t = tm.localtime()
		r = t.tm_sec * 2
		g = t.tm_min * 2
		b = t.tm_hour * 5
		return (r,g,b)

	def move_color(self, color, motion):
		r = rd.randint(-motion,motion)
		g = rd.randint(-motion,motion)
		b = rd.randint(-motion,motion)
		return ((color[0]+r)%255,(color[1]+g)%255,(color[2]+b)%255)

	def get_angles(self, count):
		ang = []
		v = 2 * math.pi / count
		for a in range(count):
			ang.append(a * v)
		return ang

	def get_sizes(self, count):
		aux = [rd.randint(1,6) for r in range(count)]
		aux.sort()
		offset = rd.randint(0,count)
		sizes = []
		for i in range(len(aux)):
			sizes.append(aux[(i+offset)%count])
		return sizes

	def mean_image(self, back_image, top_image):
		back_image.convert("RGBA")
		top_image.convert("RGBA").resize(back_image.size)
		mask = im.new("L", back_image.size, 127)
		new = im.composite(back_image, top_image, mask)
		return self.create_image(i)

	def mask_merge(self, background, top_image):
		top_image.convert("RGBA")
		mask = im.open(self.mask_path + rd.choice(self.input_mask_list)).convert("L").resize(top_image.size)
		back_image = im.new("RGBA", top_image.size, background)
		new = im.composite(back_image, top_image, mask)
		return self.create_image(i)

	def create_image(self, image):
		file = BytesIO()
		image.save(file, "jpeg", quality=85, optimize=True)
		file.name = "random_creation.jpg"
		file.seek(0)
		return file

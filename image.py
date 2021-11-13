import os
from io import BytesIO
import math
import random as rd
import time as tm
from PIL import Image as im, ImageDraw as idraw

class Image():
	"The class the bot uses to process the images..."

	def __init__(self):
		self.background = (210,210,192)
		self.w, self.h = self.get_image_size()
		self.c = (self.w/2, self.h/2)
		self.lw = 3
		self.scale = rd.randint(8,12)
		self.angles = self.get_angles(rd.randint(3,12))
		self.sizes = self.get_escape_sizes(len(self.angles))
		self.mask_path = "assets/img/masks/"
		self.input_mask_list = [f for f in os.listdir(self.mask_path) if not f.startswith(".")]

	#Update method to change random variables configuration
	def update(self):
		self.w, self.h = self.get_image_size()
		self.c = (self.w/2, self.h/2)
		self.scale = rd.randint(8,12)
		self.angles = self.get_angles(rd.randint(3,12))
		self.sizes = self.get_escape_sizes(len(self.angles))

	#Drawing an escape art piece...
	def draw_escape(self):
		i = im.new("RGB",(self.w, self.h),self.background)
		margin = self.w / 10
		d = idraw.Draw(i)
		c = self.get_time_color()
		for r in range(144):
			p = self.get_escape_start_point()
			c = self.move_color(c,3)
			while self.is_point_in(p, margin):
				np = self.get_dice_point(p)
				self.draw_line(d,c,self.lw,p,np)
				p = np
		return self.create_image(i)

	#Drawing an artistic clock...
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
		self.draw_circle(d, self.move_color((170,30,30),5), p1, cs[0]*1.66)
		self.draw_circle(d, self.move_color((75,150,75),5), p2, cs[0]*1.33)
		self.draw_circle(d, self.move_color((35,70,180),5), p3, cs[0])
		return self.create_image(i)

	#Drawing lines joining two random walks...
	def draw_lines(self):
		i = im.new("RGB",(self.w, self.h),self.background)
		d = idraw.Draw(i)
		c = self.get_time_color()
		p1 = (self.w/2,self.h/5)
		p2 = (self.w/2,self.h/5*4)
		margin = self.w / 10
		for r in range(2584):
			np1 = self.get_random_motion(p1)
			np2 = self.get_random_motion(p2)
			if self.is_point_in(np1, margin) and self.is_point_in(np2, margin):
				self.draw_line(d,c,1,np1,np2)
				p1 = np1
				p2 = np2
				c = self.move_color(c,1)
		return self.create_image(i)

	#Drawing a beautiful rando histogram...
	def draw_distribution(self):
		i = im.new("RGB",(self.w, self.h),self.background)
		d = idraw.Draw(i)
		c = self.get_time_color()
		margin = self.w / 50
		steps = 21
		data = self.get_distribution(steps)
		data_max = max(data) * 1.5
		m = (self.w-margin) / steps / 3
		w = m * 2
		color = self.get_time_color()
		for b in range(steps):
			a = (m + m * b + w * b, m)
			b = (a[0] + w, (self.h * data[b] / data_max) + m)
			self.draw_rectangle(d, self.invert_color(color), a, b)
			a = (a[0], self.h - m)
			b = (b[0], b[1] + m)
			self.draw_rectangle(d, color, a, b)
			color = self.move_color(color, 5)
		return self.create_image(i)

	#Creating a random data list to draw a distribution...
	def get_distribution(self, steps):
		data = [1 for i in range(steps)]
		type = rd.choice([0,1,2])
		for v in range(100):
			if type == 0:
				data[rd.randint(0,len(data)-1)] += 1
			elif type == 1:
				r = (rd.randint(0,len(data)-1) + rd.randint(0,len(data)-1)) // 2
				data[r] += 1
			else:
				a = rd.randint(0,len(data)-1)
				b = rd.randint(0,len(data)-1)
				r = 0
				if a < b:
					r = a
				else:
					r = b
				data[r] += 1
		return data

	#Function to move a point randomly...
	def get_random_motion(self, last_point):
		x = rd.randint(-30,30)
		y = rd.randint(-30,30)
		return (last_point[0] + x, last_point[1] + y)

	#Function to move a point for a escape drawing...
	def get_dice_point(self, last_point):
		c = len(self.angles)
		r = rd.randint(0,c-1)
		x = math.cos(self.angles[r]) * self.sizes[r] * self.scale
		y = math.sin(self.angles[r]) * self.sizes[r] * self.scale
		return (last_point[0] + x, last_point[1] + y)

	#Checking if a point is in the canvas...
	def is_point_in(self, point, margin):
		is_in = True
		if (point[0] < margin or point[0] > self.w - margin
				or point[1] < margin or point[1] > self.h - margin):
			is_in = False
		return is_in

	#Function to draw a line...
	def draw_line(self, draw, c, w, a, b):
		draw.line([a,b], fill=c, width=w)

	#Function to draw a circle...
	def draw_circle(self, draw, color, c, d):
		a = (c[0] - d/2, c[1] - d/2)
		b = (c[0] + d/2, c[1] + d/2)
		draw.ellipse([a,b], fill=color, outline=None)

	#Function to draw a rectangle...
	def draw_rectangle(self, draw, color, a, b):
		draw.rectangle([a,b], fill=color, outline=None)

	#Getting a random color based on time...
	def get_time_color(self):
		t = tm.localtime()
		r = t.tm_sec * 2
		g = t.tm_min * 2
		b = t.tm_hour * 5
		return (r,g,b)

	#Moving a color randomly in rgb color space...
	def move_color(self, color, motion):
		r = rd.randint(-motion,motion)
		g = rd.randint(-motion,motion)
		b = rd.randint(-motion,motion)
		return ((color[0]+r)%255,(color[1]+g)%255,(color[2]+b)%255)

	#A function to invert a color...
	def invert_color(self, color):
		return (255-color[0], 255-color[1], 255-color[2])

	#A function to chose a default image size to work with...
	def get_image_size(self):
		size = rd.choice([(1080,1920),(1080,1080),(1920,1080),(1920,1440),(1440,1920)])
		return size[0], size[1]

	#A function to obtain a list of angles in radian for the escape drawing algorithm...
	def get_angles(self, count):
		ang = []
		v = 2 * math.pi / count
		for a in range(count):
			ang.append(a * v)
		return ang

	#A function to obtain a list of relative sizes for the escape drawing algorithm...
	def get_escape_sizes(self, count):
		aux = [rd.randint(1,4) for r in range(count)]
		aux.sort()
		offset = rd.randint(0,count)
		sizes = []
		for i in range(len(aux)):
			sizes.append(aux[(i+offset)%count])
		return sizes

	#Adding some noise to the start point...
	def get_escape_start_point(self):
		x = self.w/5 + rd.random() * self.w/5 * 3
		y = self.h/5 + rd.random() * self.h/5 * 3
		return (x,y)

	#A function to get an image combining two images...
	def mean_image(self, back_image, top_image):
		back_image.convert("RGBA")
		top_image.convert("RGBA").resize(back_image.size)
		mask = im.new("L", back_image.size, 127)
		new = im.composite(back_image, top_image, mask)
		return self.create_image(i)

	#A function to paint a mask with an input image...
	def mask_merge(self, background, top_image):
		top_image.convert("RGBA")
		mask = im.open(self.mask_path + rd.choice(self.input_mask_list)).convert("L").resize(top_image.size)
		back_image = im.new("RGBA", top_image.size, background)
		new = im.composite(back_image, top_image, mask)
		return self.create_image(i)

	#The function to store the Image object in a byte stream...
	def create_image(self, image):
		file = BytesIO()
		image.save(file, "jpeg", quality=85, optimize=True)
		file.name = "random_creation.jpg"
		file.seek(0)
		return file

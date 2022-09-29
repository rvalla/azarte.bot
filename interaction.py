import os
from io import BytesIO
import math
import random as rd
import numpy as np
import time as tm
from PIL import Image as im, ImageDraw as idraw

class Interaction():
	"The class the bot uses to deliver interactive pieces..."

	#Some minor configurations...
	def __init__(self):
		self.background = (255,255,255)
		self.w = 1080
		self.h = 1080

	#Creating a curve from text...
	def build_message_curve(self, message):
		curve = MessageCurve(message, self.w)
		canvas = im.new("RGB",(self.w, self.h), self.background)
		draw = idraw.Draw(canvas)
		last_point = curve.get_point(0)
		for p in range(1,curve.length):
			point = curve.get_point(p)
			draw.line([last_point,point], fill=curve.get_color(p), width=curve.lw)
			last_point = point
		return self.create_image(canvas)

	#Creating a chess portrait from an image...
	def build_chess_portrait(self, image_bytes):
		image = im.open(BytesIO(image_bytes)).resize((1080, 1080))
		portrait = ChessPortrait(1080, 135, image)
		image = im.fromarray(np.array(np.round(portrait.portrait), dtype="uint8"))
		return portrait.game_data, self.create_image(image)

	#The function to store the Image object in a byte stream...
	def create_image(self, image):
		file = BytesIO()
		image.save(file, "jpeg", quality=85, optimize=True)
		file.name = "interaction_creation.jpg"
		file.seek(0)
		return file

class ChessPortrait():
	"The class the bot uses to create a chess portrait..."

	#Creating a chess portrait...
	def __init__(self, size, sq_size, image):
		self.game_data = rd.choice(open("assets/chess_heatmaps.csv").readlines()[1:])
		self.input_image = np.array(image)
		self.portrait = np.full((size, size, 3), (0,0,0))
		self.noise_width = rd.randint(25,90)
		self.sq_size = sq_size
		self.first_sq = self.is_first_square_negative() #0 if false, 1 if true
		self.size = size
		self.heatmap = self.get_float_list(self.game_data.split(";")[4])
		self.paint_output()

	def paint_output(self):
		for s in range(64):
			c, f = divmod(s, 8)
			negative = self.check_negative(c, f)
			start_x = self.sq_size * c
			start_y = self.sq_size * (7 - f) #To iterate following the heatmap squares order...
			for i in range(self.sq_size):
				for j in range(self.sq_size):
					x = start_x + i
					y = start_y + j
					if negative:
						pixel = self.get_pixel(self.get_inverted_pixel(self.input_image[x][y]), self.heatmap[s])
					else:
						pixel = self.get_pixel(self.input_image[x][y], self.heatmap[s])
					self.portrait[x][y] = pixel

	def get_pixel(self, color, sq_weight):
		r = color[0] - round(rd.randint(0,self.noise_width) * sq_weight)
		g = color[1] - round(rd.randint(0,self.noise_width) * sq_weight)
		b = color[2] - round(rd.randint(0,self.noise_width) * sq_weight)
		return (r, g, b)

	def get_inverted_pixel(self, color):
		r = 255 - color[0]
		g = 255 - color[1]
		b = 255 - color[2]
		return (r,g,b)

	def check_negative(self, c, f):
		if (c + f)%2 == 0:
			return True
		else:
			return False

	#To decide if the first square is negative (to match a real chessboard)
	def is_first_square_negative(self):
		lightness = self.get_lightness_average()
		if lightness < 128:
			return 1
		else:
			return 0

	def get_lightness_average(self):
		pixels = self.sq_size * self.sq_size
		lightness = 0
		for f in range(self.sq_size):
			for c in range(self.sq_size):
				r = int(self.input_image[f][c][0])
				g = int(self.input_image[f][c][1])
				b = int(self.input_image[f][c][2])
				lightness += (r + g + b) / 3
		return lightness / pixels

	def get_float_list(self, source):
		ls = []
		for v in source.split(","):
			ls.append(float(v))
		return ls

class MessageCurve():
	"The class the bot uses to create curves with a message..."

	#Building the curve...
	def __init__(self, message, size):
		self.s = size
		self.length = len(message) + 1
		self.limits = [[0,0.01],[0,0.01]]
		self.points = [(0,0)]
		self.blanks = set()
		self.subdivisions = [3,4,5,6,8,12,16]
		self.module = self.subdivisions[len(message)%7]
		self.base_angle = math.pi * 2 / self.module
		self.build_points(message)
		self.margins, self.scale, self.lw, self.color = self.get_configuration(message)
		self.background = (255-self.color[0],255-self.color[1],255-self.color[2])

	#Returning an specific point adjusting it to the canvas...
	def get_point(self, position):
		x = (self.points[position][0] - self.limits[0][0]) * self.scale + self.margins[0]
		y = (self.points[position][1] - self.limits[1][0]) * self.scale + self.margins[1]
		return (x,y)

	#Returning the color for an specific segment...
	def get_color(self, position):
		if position in self.blanks:
			return self.background
		else:
			return self.color

	#Building the curve of scale 1...
	def build_points(self, message):
		last_point = (0,0)
		angle = 0
		for l in range(len(message)):
			o = ord(message[l])
			n = (o-32)%self.module
			angle += self.base_angle * (n + 1)
			p = self.get_new_point(last_point, angle)
			self.points.append(p)
			self.update_limits(p)
			last_point = p
			if o == 32 or o == 9 or o == 10:
				self.blanks.add(l + 1)

	#A new point...
	def get_new_point(self, last_point, angle):
		x = math.cos(angle)
		y = math.sin(angle)
		return (last_point[0] + x, last_point[1] + y)

	#Storing minimun and maximun width and height...
	def update_limits(self, point):
		if point[0] < self.limits[0][0]:
			self.limits[0][0] = point[0]
		elif point[0] > self.limits[0][1]:
			self.limits[0][1] = point[0]
		if point[1] < self.limits[1][0]:
			self.limits[1][0] = point[1]
		elif point[1] > self.limits[1][1]:
			self.limits[1][1] = point[1]

	#Finishing the creation of the curve...
	def get_configuration(self, message):
		w = abs(self.limits[0][0] - self.limits[0][1])
		h = abs(self.limits[1][0] - self.limits[1][1])
		scales = [(self.s-self.s/5) / w]
		scales.append((self.s-self.s/5) / h)
		margins = None
		scale = min(scales)
		if scale*w < scale*h:
			margins = [(self.s-scale*w)/2,self.s/10]
		else:
			margins = [self.s/10,(self.s-scale*h)/2]
		return margins, scale, self.set_line_width(len(message)), self.set_color(message)

	#Deciding line width...
	def set_line_width(self, length):
		if length < 10:
			return 13
		else:
			return round(13 / (length / 10)) + 3

	#Deciding color...
	def set_color(self, message):
		list = [0,0,0]
		start = len(message)%3
		length = len(message)
		if length > 2:
			for i in range(3):
				list[start] += ord(message[i%length])
				list[(start+1)%3] += ord(message[(len(message)-i-1)%length])
		list[(start+2)%3] = length
		return (35+list[0]%190,35+list[1]%190,35+list[2]%190)

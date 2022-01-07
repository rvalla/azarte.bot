import random as rd

class GenColor():
	"A class to creat a living color..."

	def __init__(self, color):
		self.o = color
		self.c = color
		self.d = [1,1,1]

	#Moving a color randomly in rgb color space...
	def move(self, motion):
		r = rd.randint(-motion,motion)
		g = rd.randint(-motion,motion)
		b = rd.randint(-motion,motion)
		self.c = ((self.c[0]+r)%255,(self.c[1]+g)%255,(self.c[2]+b)%255)

	#Moving a color in its direction...
	def translate(self, motion):
		self.check_directions(motion)
		r = self.c[0] + motion * self.d[0]
		g = self.c[1] + motion * self.d[1]
		b = self.c[2] + motion * self.d[2]
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

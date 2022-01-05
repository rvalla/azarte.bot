from PIL import Image as im, ImageDraw as idraw

class DCanvas():
	"The canvas to draw with Pillow for genuary..."

	def __init__(self, width, height, background):
		self.background = background
		self.hw = [height,width]
		self.c = (self.hw[0]/2, self.hw[1]/2)
		self.canvas = im.new("RGB",(self.hw[1], self.hw[0]),self.background)
		self.draw = idraw.Draw(self.canvas)

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

	#Function to save the drawing...
	def save(self, filepath, filename):
		self.canvas.save(filepath + filename + ".jpg")

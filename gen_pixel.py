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

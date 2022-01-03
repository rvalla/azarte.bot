import random as rd
from gen_util import GenUtil

ut = GenUtil()

class GenVirus():
	"A class to infect pixels..."

	def __init__(self, color, threshold, mutation_cycle, duration):
		self.color = color
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

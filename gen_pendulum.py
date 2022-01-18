import numpy as np

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

import math
import numpy as np
import random as rd
import datetime as dt

class Genuary():
	"The class the bot uses to be part of genuary..."

	def __init__(self):
		self.start = dt.date(2022,1,1)
		self.w = 1080
		self.h = 1080

	#Checking which day of the cycle is today...
	def get_day(self):
		today = dt.date.today()
		d = (today - self.start).days
		if d < 0:
			return 0
		else:
			return d%31 + 1

	#Building a piece for this particual day...
	def get_art(self, day):
		if day == -1:
			return "Success"
		else:
			return None, "Nothing to send..."

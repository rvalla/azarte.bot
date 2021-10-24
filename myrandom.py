import random as rd

class MyRandom():
	"The class the bot use to create random numbers and sequences..."

	#Rolling a dice
	def diceroll(self, f):
		return rd.randint(1,f)

	#A sequence of dice rolls
	def dicerolls(self, n, f):
		l = []
		for r in range(n):
			l.append(self.diceroll(f))
		return l

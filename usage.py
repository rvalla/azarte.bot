import datetime as dt

class Usage():
	"The class to save usage data..."

	def __init__(self, path):
		self.output_path = path
		self.reset()

	#Resseting data variables...
	def reset(self):
		self.last_save = dt.datetime.now() #the start up time...
		self.start = 0
		self.color = [0,0,0,0,0,0] #lines, escape, clock, distribution, attractor, surprise...
		self.text = [0,0,0,0] #poem, abstract, microtale, definition...
		self.noise = [0,0,0,0] #melody, counterpoint, score, surprise...
		self.interaction = [0,0,0,0] #text, image, sound, canceled...
		self.genuary = 0 #counting genuary requests...
		self.number = 0
		self.sequence = 0
		self.choice = [0,0] #success, empty...
		self.qatar = [0,0] #success, error...
		self.language = [0,0] #spanish, english...
		self.help = 0
		self.wrong_message = 0
		self.errors = 0

	#Building usage information message...
	def build_usage_message(self):
		m = "<b>Usage data:</b>" + "\n" + \
			"start: " + str(self.start) + "\n" + \
			"color: " + str(self.color) + "\n" + \
			"text: " + str(self.text) + "\n" + \
			"noise: " + str(self.noise) + "\n" + \
			"interaction: " + str(self.interaction) + "\n" + \
			"genuary: " + str(self.genuary) + "\n" + \
			"number: " + str(self.number) + "\n" + \
			"sequence: " + str(self.sequence) + "\n" + \
			"choice: " + str(self.choice) + "\n" + \
			"qatar: " + str(self.qatar) + "\n" + \
			"language: " + str(self.language) + "\n" + \
			"help: " + str(self.help) + "\n" + \
			"wrong_message: " + str(self.wrong_message) + "\n" \
			"errors: " + str(self.errors)
		return m

	#Saving usage to file...
	def save_usage(self):
		file = open(self.output_path, "a")
		t = dt.datetime.now()
		i = t - self.last_save
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		interval = str(i).split(".")[0]
		line = self.build_usage_line(date, interval)
		file.write(line)
		file.close()
		self.reset()

	#Building a data line to save...
	def build_usage_line(self, date, interval):
		line = date + ";"
		line += interval + ";"
		line += str(self.start) + ";"
		line += str(self.color) + ";"
		line += str(self.text) + ";"
		line += str(self.noise) + ";"
		line += str(self.interaction) + ";"
		line += str(self.genuary) + ";"
		line += str(self.number) + ";"
		line += str(self.sequence) + ";"
		line += str(self.choice) + ";"
		line += str(self.qatar) + ";"
		line += str(self.language) + ";"
		line += str(self.help) + ";"
		line += str(self.wrong_message) + ";"
		line += str(self.errors) + "\n"
		return line

	#Registering a new start command...
	def add_start(self):
		self.start += 1

	#Registering a new color...
	def add_color(self, key):
		self.color[key] += 1

	#Registering a new text...
	def add_text(self, key):
		self.text[key] += 1

	#Registering a new noise...
	def add_noise(self, key):
		self.noise[key] += 1

	#Registering a new interaction...
	def add_interaction(self, key):
		self.interaction[key] += 1

	#Registering a new genuary...
	def add_genuary(self):
		self.genuary += 1

	#Registering a new number...
	def add_number(self):
		self.number += 1

	#Registering a new sequence...
	def add_sequence(self):
		self.sequence += 1

	#Registering a new choice...
	def add_choice(self, success):
		if success:
			self.choice[0] += 1
		else:
			self.choice[1] += 1

	#Registering a new qatar...
	def add_qatar(self, success):
		if success:
			self.qatar[0] += 1
		else:
			self.qatar[1] += 1

	#Registering a new language...
	def add_language(self, l):
		self.language[l] += 1

	#Registering a new help...
	def add_help(self):
		self.help += 1

	#Registering a new wrong_message...
	def add_wrong_message(self):
		self.wrong_message += 1

	#Registering a new error...
	def add_error(self):
		self.errors += 1

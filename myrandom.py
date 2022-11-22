import random as rd

class MyRandom():
	"The class the bot use to create random numbers, sequences and predictions..."

	def __init__(self):
		self.wc = FifaWC()

	#Rolling a dice
	def diceroll(self, f):
		return rd.randint(1,f)

	#A sequence of dice rolls
	def dicerolls(self, n, f):
		l = []
		for r in range(n):
			l.append(self.diceroll(f))
		return l

	def worldcup_match(self, l, home, visiting):
		return self.wc.match(l, home, visiting)

class FifaWC():
	"The class to guess the result of Fifa World Cup matches..."

	teams_code = {"qatar": "QAT", "catar": "QAT",
					"ecuador": "ECU",
					"senegal": "SEN",
					"netherlands": "NED", "paisesbajos": "NED", "paísesbajos": "NED", "holanda": "NED",
					"england": "ENG", "inglaterra": "ENG",
					"iran": "IRN", "irán": "IRN",
					"usa": "USA", "eeuu": "USA", "estadosunidos": "USA",
					"wales": "WAL", "gales": "WAL",
					"argentina": "ARG",
					"saudiarabia": "KSA", "arabiasaudita": "KSA", "arabia": "KSA",
					"mexico": "MEX", "méxico": "MEX", "méjico": "MEX",
					"poland": "POL", "polonia": "POL",
					"france": "FRA", "francia": "FRA",
					"australia": "AUS",
					"denmark": "DEN", "dinamarca": "DEN",
					"tunisia": "TUN", "túnez": "TUN", "tunez": "TUN",
					"spain": "ESP", "españa": "ESP",
					"costarica": "CRC",
					"germany": "GER", "alemania": "GER",
					"japan": "JPN", "japón": "JPN", "japon": "JPN",
					"belgium": "BEL", "bélgica": "BEL", "belgica": "BEL",
					"canada": "CAN", "canadá": "CAN",
					"morocco": "MAR", "marruecos": "MAR",
					"croatia": "CRO", "croacia": "CRO",
					"brazil": "BRA", "brasil": "BRA",
					"serbia": "SRB",
					"switzerland": "SUI", "suiza": "SUI",
					"cameroon": "CMR", "camerún": "CMR", "camerun": "CMR",
					"portugal": "POR",
					"ghana": "GHA", "gana": "GHA",
					"uruguay": "URU",
					"korea": "KOR", "corea": "KOR", "coreadelsur": "KOR"
				}

	def __init__(self):
		self.teams = self.load_teams()
		self.matches = 0
		self.max_attacks = 10
		self.max_goals = 7
		self.es_comments = self.build_comments("assets/text/es/fifawc_2022_msg_es.csv")
		self.en_comments = self.build_comments("assets/text/en/fifawc_2022_msg_en.csv")

	def match(self, l, home, visiting):
		team_a_c = self.get_team_code(home)
		team_b_c = self.get_team_code(visiting)
		if not team_a_c == None and not team_b_c == None:
			team_a = self.look_for_team(team_a_c)
			team_b = self.look_for_team(team_b_c)
			result, score = self.decide_match(self.look_for_team(team_a_c), self.look_for_team(team_b_c))
			return self.build_message(l, score, team_a, team_b)
		else:
			return "<b>#$%%()@-|!*^{}</b>", self.build_null_message(l, home, visiting)

	def decide_match(self, team_a, team_b):
		score = [self.decide_attacks(team_a, team_b), self.decide_attacks(team_b, team_a)]
		result = self.get_result(score)
		self.update_teams(result, score, team_a, team_b)
		return result, score

	def build_message(self, l, score, team_a, team_b):
		return self.build_match_result(l, score, team_a, team_b), self.build_match_comment(l, score, team_a, team_b)

	def build_match_result(self, l, score, team_a, team_b):
		m = ""
		if l == 1:
			m = "<b>" + team_a.en_name + " " + str(score[0]) + " - "
			m += team_b.en_name + " " + str(score[1]) + "</b>"
		else:
			m = "<b>" + team_a.es_name + " " + str(score[0]) + " - "
			m += team_b.es_name + " " + str(score[1]) + "</b>"
		return m

	def build_match_comment(self, l, score, team_a, team_b):
		m = ""
		if team_a.code == team_b.code:
			if l == 1:
				m = "Do you know something about football? In a match there must be two different teams. At least "
				m += "when you intend the game to take place in a single universe. Note that a ball, twenty two players, "
				m += "three referees and the other things needed are a lot of stuff to think that they can take "
				m += "advantage of the quantum properties of matter."
			else:
				m = "¿Sabés algo de fútbol? En un partido debe haber dos equipos diferentes. Al menos "
				m += "si pretendés que el partido suceda en un único universo. Hay que tener en cuenta que "
				m += "una pelota, veintidós jugadores, tres árbitros y todo los demás son muchas cosas como para "
				m += "pensar que pueden aprovechar las propiedades cuánticas de la materia."
		else:
			if l == 1:
				n = rd.randint(0, len(self.en_comments)-1)
				m += self.en_comments[n][0]
				m += ", "
				n = rd.randint(0, len(self.en_comments)-1)
				m += self.en_comments[n][1]
				m += ", "
				n = rd.randint(0, len(self.en_comments)-1)
				m += self.en_comments[n][2]
			else:
				n = rd.randint(0, len(self.es_comments)-1)
				m += self.es_comments[n][0]
				m += ", "
				n = rd.randint(0, len(self.es_comments)-1)
				m += self.es_comments[n][1]
				m += ", "
				n = rd.randint(0, len(self.es_comments)-1)
				m += self.es_comments[n][2]
		return m

	def build_null_message(l, home, visiting):
		m = ""
		if l == 1:
			m = "I think a match between " + home + "and" + visiting + " "
			m += "is not possible during the Qatar Fifa World Cup. Did you spell the name of the teams correctly? "
			m += "Please don't waste my time!"
		else:
			m = "Creo que un partido entre " + home + "y" + visiting + " "
			m += "no es posible durante el Mundial de Fútbol organizado por la Fifa en Qatar. "
			m += "¿Escribiste los nombres de los equipos correctamente? "
			m += "¡No me hagas perder el tiempo!"

	#Predicting a match result...
	def decide_attacks(self, attack, deffense):
		goals = 0
		n = round(self.max_attacks * attack.strength)
		for a in range(n):
			if self.decide_goal(attack.strength, deffense.strength):
				goals += 1
		return goals

	#Deciding if an attack is a goal...
	def decide_goal(self, attack_strength, deffense_strength):
		is_goal = False
		a = rd.random()
		if a < attack_strength:
			d = rd.random()
			if d > deffense_strength:
				is_goal = True
		return is_goal

	def update_teams(self, result, score, team_a, team_b):
		expected_result_a = team_a.strength - team_b.strength
		result_a = (score[0] - score[1]) / self.max_goals - expected_result_a
		expected_result_b = team_b.strength - team_a.strength
		result_b = (score[1] - score[0]) / self.max_goals - expected_result_b
		if result == 1:
			team_a.update_team(0, team_a.strength + result_a)
			team_b.update_team(2, team_b.strength + result_b)
		elif result == 0:
			team_a.update_team(1, team_a.strength + result_a)
			team_b.update_team(1, team_b.strength + result_b)
		elif result == -1:
			team_a.update_team(2, team_a.strength + result_a)
			team_b.update_team(0, team_b.strength + result_b)

	def get_result(self, score):
		result = 0
		if score[0] > score[1]:
			result = 1
		elif score[0] < score[1]:
			result = -1
		return result

	def load_teams(self):
		teams = []
		file = open("assets/fifawc_2022_teams.csv").readlines()[1:]
		for line in file:
			data = line.split(";")
			teams.append(Team(data[0],data[1],data[2],float(data[3])))
		return teams

	def look_for_team(self, code):
		team = None
		for t in self.teams:
			if t.code == code:
				team = t
				break
		return team

	def get_team_code(self, team):
		try:
			return FifaWC.teams_code[team.lower()]
		except:
			return None

	def build_comments(self, path):
		lines = open(path).readlines()[1:]
		comments = []
		for line in lines:
			comments.append(line.split(";"))
		return comments

class Team():
	"The tiny class to represent a football team..."

	def __init__(self, code, en_name, es_name, strength):
		self.code = code
		self.en_name = en_name
		self.es_name = es_name
		self.strength = strength
		self.results = [0,0,0] #victories, draws, defeats

	#Update team
	def update_team(self, result, result_strength):
		self.update_strength(result_strength)
		self.update_result_history(result)

	#Updating a team strength
	def update_strength(self, result_strength):
		self.strength = round((self.strength * 3 + result_strength) / 4, 2)
		if self.strength > 1:
			self.strength = 1
		elif self.strength < 0:
			self.strength = 0

	#Updating result history
	def update_result_history(self, result):
		self.results[result] += 1

	def __str__(self):
		return "I am a representation of a football team..." + "\n" + \
				"I am " + self.en_name + "\n" + \
				"My actual strength is " + str(self.strength)

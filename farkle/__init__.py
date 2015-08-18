import random

"""

TODO: Allow for n-sided dice.

"""

class FarklePlayer(object):
	"""A helper class for managing a Farkle player's session."""
	def __init__(self, rolls = []):
		super(FarklePlayer, self).__init__()

		self.rolls = rolls
		self.name = "Player"
		self.score = 0
		self.current_points = 0

	def add_roll(roll):
		self.rolls.append(roll)

class Farkle(object):
	"""A simple class for handling a Farkle game"""
	def __init__(self, num_players = 4, game_options = {}):
		super(Farkle, self).__init__()

		self.players = []
		self.set_num_players(num_players)

		self.num_dice = 6
		self.minimum_score = 1000
		self.winning_score = 10000
		self.roll_scores_table = {
			"5": 50, 
			"1": 100, 
			"222": 200,
			"333": 300, 
			"444": 400,
			"555": 500,
			"666": 600,
			"111": 1000, 
			"2222": 1000, 
			"3333": 1000, 
			"4444": 1000, 
			"5555": 1000, 
			"6666": 1000,
			"1111": 2000, 
			"22222": 2000, 
			"33333": 2000, 
			"44444": 2000, 
			"55555": 2000, 
			"66666": 2000, 
			"11111": 3000, 
			"123456": 2500,
			"222222": 3000, 
			"333333": 3000, 
			"444444": 3000, 
			"555555": 3000, 
			"666666": 3000, 
			"111111": 4000, 
		}

		self.set_options(game_options)

		if self.num_players < 1:
			self.num_players = 1

		if self.num_dice < 1:
			self.num_dice = 1

		if self.roll_scores_table["1"] < 1:
			self.roll_scores_table = 1

		self.roll_scores_table["1"] = 100
		self.current_player = 0

	def set_num_players(self, n):
		if n < 1:
			return

		self.num_players = n
		if len(self.players) == self.num_players:
			return
		elif len(self.players) > self.num_players:
			for i in range(self.num_players, len(self.players), -1):
				self.players.remove(i)
		elif len(self.players) < self.num_players:
			for i in range(len(self.players), self.num_players):
				p = FarklePlayer()
				p.name = "Player " + str(i + 1)
				self.players.append(p)

	def set_options(self, opts):
		for k in opts:
			setattr(self, k, opts[k])

	def roll(self, n = 0):
		roll = []
		if n < 1: n = self.num_dice
		for i in range(n):
			# Roll a six-sided die
			roll.append(str(random.randint(1, 6)))
		roll.sort()
		return ''.join(roll)

	def roll_scores(self, roll):
		scores = {}
		for k in self.roll_scores_table:
			x = roll.find(k)
			if x > -1:
				scores[k] = self.roll_scores_table[k]
		return scores

	def all_roll_scores(self, roll):
		scores = {}
		e = self.roll_scores(roll)
		for k in e:
			scores[k] = e[k]
			sub_scores = self.all_roll_scores(roll.replace(k, '' , 1))
			for j in sub_scores:
				scores[k+", "+j] = scores[k] + sub_scores[j]
		# Remove bad duplicates
		de_duped_scores = {}
		remove_me = []
		for k in scores:
			u = ''.join(sorted(k.replace(", ", ''))) + str(scores[k])
			if u in de_duped_scores:
				remove_me.append(k)
				continue
			de_duped_scores[u] = 1

		for k in remove_me:
			scores.pop(k, 0)

		return scores


"""

	def roll_scores(self, roll, roll_again = 0):
		scores = {}

		# Individual Scores
		for k in self.roll_scores_table:
			tmp_roll = roll
			added_index = 0
			while 1:
				start = tmp_roll.find(k)
				if start == -1: break
				start += added_index
				end = start + len(k)
				scores[str(start) + "," + str(end)] = self.roll_scores_table[k]
				added_index += len(k)
				tmp_roll = tmp_roll.replace(k, "", 1)

		# Compound Scores
		for k in scores:
			pieces = k.split(",")
			start = int(pieces[0])
			end = int(pieces[1])

			for j in scores:
				if j == k: continue

		return scores, roll_again
"""

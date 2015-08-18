from farkle import Farkle
import os, sys

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def is_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def number_input(query, default = 1, error = "Invalid Number"): 
	if query == "" and error == "":
		x = input()
	else:
		x = input("{0} (Default: {1}) ".format(query, default))
	while not is_int(x) and x != "":
		x = input("{1} {0} ".format(query, error))
	if x == "":
		x = default
	return int(x)

def yn_input(query): 
	x = input("{0} ('y' for yes) ".format(query))
	return x.lower().startswith("y")

def inv_yn_input(query): 
	x = input("{0} ('n' for no) ".format(query))
	return x.lower().startswith("n")

def list_choice_input(query, choices, default = 1):
	if len(choices) > 1000:
		raise Exception("Too many choices for list_choice_input()")
	choice = 0
	while choice < 1 or choice > len(choices):
		print("{0} ".format(query))
		for i in range(len(choices) - 1, -1, -1):
			index = i + 1
			text = choices[i]
			if index == default:
				index = "* " + str(index)
			else:
				index = "  " + str(index)
			print("{0}. {1} ".format(index, choices[i]))
		choice = input()
		if is_int(choice):
			choice = int(choice)
		elif choice == "":
			choice = default
		else: 
			choice = 0

	return choice - 1

class FarkleConsoleGame(Farkle):
	"""A class for managing and playing a Farkle instance via a terminal."""
	def __init__(self):
		super(FarkleConsoleGame, self).__init__()
		self.log_game = True
		self.log_file = "{0}-farkle-game.log"

	def start_new_game(self):
		clear_screen()
		self.num_players = number_input("How many players?", 4, "Invalid Number (0 to quit).")
		if self.num_players < 1:
			sys.exit(0)

		self.set_num_players(self.num_players)

		if yn_input("Do you want to name your players?"):
			for p in self.players:
				p.name = input(p.name + "'s name? ")

		self.game_loop()

	def game_loop(self):
		self.playing = True
		while self.playing:
			clear_screen()
			self.player_turn(self.current_player)
			self.current_player += 1
			if self.current_player >= len(self.players):
				self.current_player = 0

	def show_roll(self, roll):
		s = ['', '', '']
		for c in roll:
			s[0] += '╔═══╗'
			s[1] += '║{0}║'.format(' ' + c + ' ')
			s[2] += '╚═══╝'
		for t in s: print(t)

	def player_turn(self, player_id):
		if player_id < 0 or player_id >= len(self.players): return

		p = self.players[player_id]

		busted = False
		stop = False
		num_dice = 6

		while not busted and not stop:
			clear_screen()
			print("{0}'s Turn! (Score: {1}, Current Points: {2})\n".format(p.name, p.score, p.current_points))

			if p.current_points > 0:
				if inv_yn_input("Do you want to keep rolling {0} dice?".format(num_dice)):
					stop = True
					break

			roll = self.roll(num_dice)
			self.show_roll(roll)

			scores = self.all_roll_scores(roll)
			if len(scores) < 1:
				busted = True
				break

			score_index = {}
			choices = []
			smax = 0
			i = 1
			for s in scores:
				modmax = smax
				if scores[s] > modmax:
					default = i
					smax = scores[s]
				choices.append("Points: {0} ({1})".format(scores[s], s))
				score_index[i - 1] = scores[s], s
				i += 1
			choice = list_choice_input("What do you want to keep?", choices, default)

			if score_index[choice][0] == -1:
				stop = True
				break
			else:
				p.current_points += score_index[choice][0]
				num_dice -= len(score_index[choice][1].replace(", ", ''))
				if num_dice == 0:
					num_dice = 6

		if busted:
			print("{0} busted and drops {1} points! No points this turn. Score: {2}".format(p.name, p.current_points, p.score))
			p.current_points = 0
		elif stop:
			p.score += p.current_points
			if p.score < self.minimum_score:
				print("{0} is done with {1} points, but that's not enough to get on the board ({2}). Still no score!".format(p.name, p.current_points, self.minimum_score))
			else:
				print("{0} is done with {1} points. New score: {2}".format(p.name, p.current_points, p.score))
			p.current_points = 0

		input()


	def display_menu(self, menu, title):
		pass

if __name__ == "__main__":
	f = FarkleConsoleGame()
	f.start_new_game()



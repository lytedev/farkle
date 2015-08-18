score_table = {
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

import random

def get_dice_roll(n = 6):
	"""Generate a sorted, n-length string containing the result of nd6."""
	roll = []
	for i in range(n):
	   roll.append(str(random.randint(1, 6)))
	roll.sort()
	return ''.join(roll)

def get_scores(roll):
	"""Return a dictionary with the scores found in a roll where the keys are
	the scoring sets found and the values are the points worth."""
	scores = {}
	for combo in score_table:
		if combo in roll:
			scores[combo] = score_table[combo]
	return scores

def get_score_options(roll): 
	score_options = {}

	initial_options = get_scores(roll)
	for combo in initial_options:
		score_options[combo] = initial_options[combo]

		sub_scores = get_score_options(roll.replace(combo, '' , 1))
		for sub_combo in sub_scores:
			# Prevents duplicate combinations and sorts the combined keys 
			# ascending by points.
			if sub_scores[sub_combo] < score_options[combo]: continue 
			score_options[combo + ", " + sub_combo] = score_options[combo] \
				+ sub_scores[sub_combo]

	return score_options

def turn():
	"""Simulate a player's turn."""
	points = 0
	busted = False
	stopped = False
	num_dice = 6
	
	while not busted and not stopped:
		if points > 0:
			# ... Check if user wants to stop
				stopped = true
				break

		current_roll = roll(num_dice)
		score_options = scores(current_roll)

		if len(score_options) < 1:
			busted = True
			break
			
		# ... Let user choose scoring option
		
		points += score_options[choice]
		num_dice -= len(choice)
		if num_dice == 0: 
			num_dice = 6

r = get_dice_roll()
r = "111111"
print(r)
print(repr(get_scores(r)))
print(repr(get_score_options(r)))

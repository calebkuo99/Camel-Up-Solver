from game import *

class Solver(object):
	"""Solver"""
	def __init__(self, board):
		self.board = board

	def get_camels_not_moved(self):
		return [c for c in self.board.all_camels if c not in self.board.moved_camels]

	def move_camel_all_ways(self, camel_id):
		"""Returns a list of boards of the possibilities if camel_id moves."""
		new_boards = []
		for dice_roll in [1, 2, 3]:
			new_boards += [Board(board=self.board)]
			new_boards[dice_roll - 1].move_camel(camel_id, dice_roll)
		return new_boards

class BruteForce(Solver):
	def find_distributions(self):
		"""Finds the distributions of the likelihood that a given 
		camel will win this round. Takes into account the the camels 
		that have moved already."""

		camels_not_moved = self.get_camels_not_moved()
		all_camel_orderings = all_permutations(camels_not_moved)
		all_dice_orderings = all_dice_permutations(len(camels_not_moved))
		boards = []
		total = 0
		for camel_ordering in all_camel_orderings:
			for dice_ordering in all_dice_orderings:
				boards += [Board(board=self.board)]
				if len(camel_ordering) != len(dice_ordering):
					assert False, "something went wrong"
				
				for i in range(len(camel_ordering)):
					boards[total].move_camel(camel_ordering[i], dice_ordering[i])

				total += 1

		distributions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
		for b in boards:
			distributions[b.winning_camel()] += 1

		# normalize
		for k in distributions.keys():
			distributions[k] = distributions[k] / total
		
		return distributions

	def expected_powerup_value(self, position, powerup):
		"""Returns expected number of camels landing on a given powerup at a given position."""
		camels_not_moved = self.get_camels_not_moved()
		board_with_powerup = Board(board=self.board)
		board_with_powerup.add_powerup(position, powerup)

		all_camel_orderings = all_permutations(camels_not_moved)
		all_dice_orderings = all_dice_permutations(len(camels_not_moved))

		hits = 0
		total = 0
		for camel_ordering in all_camel_orderings:
			for dice_ordering in all_dice_orderings:
				simulation_board = Board(board=board_with_powerup)

				for i in range(len(camel_ordering)):
					hit = simulation_board.move_camel(camel_ordering[i], dice_ordering[i])
					if hit:
						hits += 1

				total += 1

		return hits / total
	
def all_permutations(l):
	"""Returns a list of all permutations of l.
	
	>>> all_permutations([1, 2, 3])
	[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
	>>> all_permutations([])
	[[]]
	"""
	if len(l) == 0 or len(l) == 1:
		return [l]

	permutations = []
	if len(l) == 2:
		permutations += [l]
		permutations += [l[1:] + l[:1]]
	else:
		for i in range(len(l)):
			subarray = l[:i] + l[i + 1:]
			small_permutations = all_permutations(subarray)
			for s in small_permutations:
				permutations += [[l[i]] + s]

	return permutations

def all_dice_permutations(num_camels):
	"""Returns a list of possible dice orderings.

	assume 1 <= num_camels <= 5
	"""
	if num_camels == 1:
		return [[1], [2], [3]]
	f = all_dice_permutations(num_camels - 1)
	answer = []
	for ordering in f:
		answer += [[1] + ordering]
		answer += [[2] + ordering]
		answer += [[3] + ordering]
	return answer

class Player(object):
	"""Play the game!"""

	def __init__(self, num_players):
		"""Create a Player object."""

		self.board = Board()
		self.solver = Solver(self.board)
		#self.num_players = num_players

	def add_camel(self, camel, position):
		self.board.add_camel(1)

"""
d = {0: [1, 2, 3], 1: [4], 2: [5]}
b = Board(d)
s = BruteForce(b)
"""
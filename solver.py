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

		distributions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
		total = 0
		for camel_ordering in all_camel_orderings:
			for dice_ordering in all_dice_orderings:
				state = self.board.fast_copy_state()
				moved_camels = [c for c in self.board.moved_camels]
				if len(camel_ordering) != len(dice_ordering):
					assert False, "something went wrong"
				
				for i in range(len(camel_ordering)):
					self.board.move_camel(camel_ordering[i], dice_ordering[i])

				distributions[self.board.winning_camel()] += 1
				# restore state
				self.board.state = state
				self.board.moved_camels = moved_camels

				total += 1

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
				state = board_with_powerup.fast_copy_state()
				moved_camels = [c for c in self.board.moved_camels]

				for i in range(len(camel_ordering)):
					hit = board_with_powerup.move_camel(camel_ordering[i], dice_ordering[i])

					if hit:
						hits += 1

				# restore state
				board_with_powerup.state = state
				board_with_powerup.moved_camels = moved_camels

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
	"""Play the game!
	ALL camels will be labeled and interacted with color as opposed to number.
	ALL tiles will be one-indexed.
	"""

	def __init__(self, num_players):
		"""Create a Player object."""

		self.board = Board()
		self.solver = Solver(self.board)
		#self.num_players = num_players

	def add_camel(self, camel_color, position):
		self.board.add_camels([NUM_OF[camel_color]], position-1)

	def move_camel(self, camel_color, num_space):
		self.board.move_camel(NUM_OF[camel_color], num_spaces)

	def reset_round(self):
		self.board.reset_round()


"""d = {0: [1, 2, 3], 1: [4], 2: [5]}
b = Board(d)
s = BruteForce(b)"""
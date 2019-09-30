from game import *

class Solver(object):
	"""Solver"""
	def __init__(self, board):
		self.board = board

	#def find_distributions(self):
	def brute_force(self):
		"""Finds the distributions of the likelihood that a given 
		camel will win this round. Takes into account the the camels 
		that have moved already."""

		camels_not_moved = [c for c in self.board.all_camels if c not in self.board.moved_camels]

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

	def move_camel_all_ways(self, camel_id):
		"""Returns a list of boards of the possibilities if camel_id moves."""
		new_boards = []
		for dice_roll in [1, 2, 3]:
			new_boards += [Board(board=self.board)]
			new_boards[dice_roll - 1].move_camel(camel_id, dice_roll)
		return new_boards


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


d = {0: [1, 2, 3], 1: [4], 2: [5]}
b = Board(d)
s = Solver(b)

b.add_powerup(4, -1)

print(b)
b.move_camel(2, 1)
print(b)
b.move_camel(5, 2)
print(b)

"""
print(b)
print(s.brute_force())

print(b)
b.move_camel(1, 3, 0)
print(b)
b.move_camel(2, 1)
print(b)
print(b.moved_camels)

b.new_round()
b.move_camel(1, 1)
print(b)

b.add_powerup(5, 1)
b.add_powerup(7, -1)
b.print_powerups()

b.move_camel(4, 1)
b.move_camel(3, 3)
print(b)
print(b.moved_camels)

b.add_powerup(0, 1)
b.print_powerups()
b.remove_powerup(0)
b.print_powerups()
b.remove_powerups()
b.print_powerups()
"""

import copy

NUM_TILES = 17 # 16 + 1 for end position

class Board(object):
	"""Game Board"""

	def __init__(self, starting=None, board=None):
		"""Create a Game Board

		state -- array of Places
		starting -- starting layout of camels; dictionary: index -> [camels]

		#TODO: how to use this constructor
		"""
		if board is not None:
			self.state = copy.deepcopy(board.state)
			self.moved_camels = copy.deepcopy(board.moved_camels)
			self.all_camels = copy.deepcopy(board.all_camels)
		else:
			self.state = [Place([]) for x in range(NUM_TILES)]
			self.moved_camels = []
			self.all_camels = []

			if starting != None:
				for p in starting.keys():
					self.state[p].add_camels(starting[p])
					self.all_camels += starting[p]
			else:
				self.state[0].add_camels([1, 2, 3])
				self.all_camels = [1, 2, 3]

	def move_camel(self, camel_id, num_spaces, position=None):
		"""Move camel_id (at position) num_spaces forward.
		
		>>> print(b)
		[[1, 2, 3][0], [4][0], [5][0], [][0], [][-1], [][0], ...]
		>>> b.move_camel(1, 3)
		>>> print(b)
		[[1][0], [4, 2, 3][0], [5][0], [][0], [][-1], [][0], ...]
		>>> b.move_camel(5, 2)
		>>> print(b)
		[[1][0], [4, 2, 3][0], [][0], [5][0], [][-1], [][0], ...]
		"""
		if num_spaces <= 0 or num_spaces > 3:
			assert False, "Camels can only move 1, 2, or 3 spaces!"

		if camel_id in self.moved_camels:
			assert False, "This camel has moved already!"

		if position == None:
			position = self.find_camel_position(camel_id)
		removed_camels = self.state[position].remove_camel(camel_id)
		
		# check for powerup
		end_position = position + num_spaces

		# check for winner
		if end_position >= NUM_TILES - 1 or (end_position == NUM_TILES - 2 and self.state[end_position].powerup == 1):
			end_position = NUM_TILES - 1
			self.state[end_position].add_camels(removed_camels)

			# WINNER = self.board.winning_camel()
			return
		powerup = self.state[end_position].powerup
		end_position += powerup

		if powerup == -1:
			self.state[end_position].add_camels(removed_camels, True)
		else:
			self.state[end_position].add_camels(removed_camels)
		
		self.moved_camels += [camel_id]

	def find_camel_position(self, camel_id):
		"""Find the position of camel_id

		return -- position (int) of camel_id"""
		position = -1
		for i in range(len(self.state)):
			p = self.state[i]
			if p.has_camel_here(camel_id):
				position = i
				break
		return position

	def add_powerup(self, position, powerup):
		"""Add powerup (-1 or 1) at position"""
		self.state[position].place_powerup(powerup)

	def remove_powerup(self, position):
		"""Remove powerup (reset to 0) at position"""
		self.state[position].remove_powerup()

	def remove_powerups(self):
		"""Remove all powerups"""
		for p in self.state:
			p.remove_powerup()

	def new_round(self):
		#TODO
		self.moved_camels = []
		self.remove_powerups()
		return 0

	def losing_camel(self):
		"""Returns id of the camel in last place."""
		for p in self.state:
			if p.has_camels():
				return p.losing_camel()

	def winning_camel(self):
		"""Returns id of the camel in first place."""
		for i in range(len(self.state) - 1, 0, -1):
			p = self.state[i]
			if p.has_camels():
				return p.winning_camel()

	def second_place_camel(self):
		"""Returns id of the camel in second place."""
		#TODO: needs testing/verification; breaks encapsulation
		found_first = False
		for i in range(len(self.state) - 1, 0, -1):
			p = self.state[i]
			if p.has_camels():
				if len(p.camels) == 1:
					found_first = True
				else:
					return p.camels[len(p.camels) - 2]
			if found_first:
				return p.winning_camel()
		return 0

	def print_powerups(self):
		"""Print layout of powerups"""
		l = []
		for p in self.state:
			l += [p.powerup]
		print(l)

	def __repr__(self):
		return str(self.state)

class Place(object):
	"""A Place holds camels or a powerup."""

	def __init__(self, camels):
		"""Create a Place

		position -- int of this Place's tile location
		camels -- list of camels in this place -- [bottom, ... , top]
		powerup -- int {-1, 0, 1} of a powerup in this Place
		"""
		self.camels = camels
		self.powerup = 0

	def add_camels(self, camels, under=False):
		"""Add camels to this Place

		camels -- list of camels to be added
		under -- if True, place camels under instead
		"""
		for c in camels:
			if c in self.camels:
				assert False, "Camel already here!"

		if under:
			self.camels = camels + self.camels
		else:
			self.camels += camels

	def remove_camels(self):
		"""Remove all camels from this Place.

		return -- list of camels (in same order) that were removed"""
		r = self.camels
		self.camels = []
		return r

	def remove_camel(self, camel_id):
		"""Remove camel with camel_id from this Place, as well as all
		camels that are on top of this camel.

		return -- list of camels (in same order) that were removed"""
		index = -1

		for i in range(len(self.camels)):
			if self.camels[i] == camel_id:
				index = i
				break

		if index == -1:
			assert False, "Camel not in this Place, cannot remove."

		r = self.camels[index:]
		self.camels = self.camels[:index]
		return r

	def has_camel_here(self, camel_id):
		"""Returns true if camel_id is present at this Place."""
		return camel_id in self.camels

	def has_camels(self):
		"""Returns true if there are any camels at this Place."""
		return not self.camels == []

	def place_powerup(self, powerup):
		"""Places a powerup (-1 or 1) at this Place."""
		if powerup not in [-1, 1]:
			assert False, "powerup must be -1 or 1!"

		if not self.camels == []:
			assert False, "camels occupy this area; powerup can't be placed here!"

		self.powerup = powerup

	def remove_powerup(self):
		"""Removes powerup from this Place."""
		self.powerup = 0

	def winning_camel(self):
		"""Returns the top camel in this Place."""
		return self.camels[len(self.camels) - 1]

	def losing_camel(self):
		"""Returns the lowest camel in this Place."""
		return self.camels[0]

	def __str__(self):
		return str(self.camels) + "[" + str(self.powerup) + "]"

	def __repr__(self):
		return str(self.camels) + "[" + str(self.powerup) + "]"


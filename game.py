NUM_TILES = 17 # 16 + 1 for end position
COLOR_OF = {1: "r", 2: "b", 3: "p", 4: "g", 5: "y"}
NUM_OF = {"r": 1, "b": 2, "p": 3, "g": 4, "y": 5}

class Board(object):
	"""Game Board"""

	def __init__(self, starting=None, board=None):
		"""Create a Game Board

		starting -- starting layout of camels; dictionary: index -> [camels]
		board -- create a copy of Board given a board

		state -- array of Places
		all_camels -- array of all the camels
		moved_camels -- array of the camels that have moved 
		"""
		self.state = []
		self.all_camels = []
		self.moved_camels = []
		self.round_bets = {}

		if board is not None:
			self.state = board.fast_copy_state()
			self.all_camels = [c for c in board.all_camels]
			self.moved_camels = [c for c in board.moved_camels]
		else:
			self.state = [[[], 0] for x in range(NUM_TILES)]

			if starting != None:
				for p in starting.keys():
					self.state[p][0] = starting[p]
					self.all_camels += starting[p]

		for i in range(1, 6):
			self.round_bets[i] = [0, 2, 2, 3, 5]

	def move_camel(self, camel_id, num_spaces, position=None):
		"""Move camel_id (at position) num_spaces forward. Updates moved_camels to include 
		the camel that moved. Returns True if the camel(s) had landed on a powerup. False otherwise.
		
		>>> b
		[[1, 2, 3][0], [4][0], [5][0], [][0], [][-1], [][0], ...]
		>>> b.moved_camels
		[]
		>>> b.move_camel(1, 3)
		>>> b
		[[1][0], [4, 2, 3][0], [5][0], [][0], [][-1], [][0], ...]
		>>> b.move_camel(5, 2)
		>>> b
		[[1][0], [4, 2, 3][0], [][0], [5][0], [][-1], [][0], ...]
		>>> b.moved_camels
		[1, 5]
		"""
		if num_spaces <= 0 or num_spaces > 3:
			assert False, "Camels can only move 1, 2, or 3 spaces!"

		if camel_id in self.moved_camels:
			assert False, "This camel has moved already!"

		if position == None:
			position = self.find_camel_position(camel_id)

		removed_camels = self.remove_camel(camel_id, position)
		
		# check for powerup
		end_position = position + num_spaces
		landed_on_powerup = False

		if end_position < NUM_TILES and self.state[end_position][1] != 0:
			landed_on_powerup = True

		# check for winner
		if end_position >= NUM_TILES - 1 or (end_position == NUM_TILES - 2 and self.state[end_position][1] == 1):
			end_position = NUM_TILES - 1
			self.add_camels(removed_camels, end_position)

			# WINNER = self.board.winning_camel()
			return landed_on_powerup

		powerup = self.state[end_position][1]
		end_position += powerup

		if powerup == -1:
			self.add_camels(removed_camels, end_position, under=True)
		else:
			self.add_camels(removed_camels, end_position)
		
		self.moved_camels += [camel_id]
		return landed_on_powerup

	def add_camels(self, camels_to_add, position, under=False):
		"""Add camels to this Place

		camels_to_add -- list of camels to be added
		position -- where to add the camels
		under -- if True, place camels under instead
		"""
		camels = self.state[position][0]
		for c in camels_to_add:
			if c in camels:
				assert False, "Camel already here!"

		if under:
			self.state[position][0] = camels_to_add + self.state[position][0]
		else:
			camels += camels_to_add

	def remove_camel(self, camel_id, position):
		"""Remove camel with camel_id from this Place, as well as all
		camels that are on top of this camel.

		return -- list of camels (in same order) that were removed"""
		index = -1

		for i in range(len(self.state[position][0])):
			if self.state[position][0][i] == camel_id:
				index = i
				break

		r = self.state[position][0][index:]
		self.state[position][0] = self.state[position][0][:index]
		return r

	def find_camel_position(self, camel_id):
		"""Find the position of camel_id

		return -- position (int) of camel_id"""
		for i in range(len(self.state)):
			if camel_id in self.state[i][0]:
				return i

	def add_powerup(self, position, powerup):
		"""Add powerup (-1 or 1) at position
		
		>>> b
		[[1, 2, 3][0], [4][0], [5][0], [][0], [][0], [][0]
		>>> b.add_powerup(4, -1)
		>>> b
		[[1, 2, 3][0], [4][0], [5][0], [][0], [][-1], [][0]
		"""
		if position >= NUM_TILES - 1 or position <= 0:
			assert False, "Cannot place powerup here: Invalid Position."

		if self.state[position][0] != []:
			assert False, "Cannot place powerup here: Camels already here."

		if not (powerup == 1 or powerup == -1):
			assert False, "Powerup must be -1 or 1!"

		self.state[position][1] = powerup

	def remove_powerup(self, position):
		"""Remove powerup (reset to 0) at position
		
		>>> b
		[[1, 2, 3][0], [4][0], [5][0], [][0], [][-1], [][0]
		>>> b.remove_powerup(4)
		>>> b
		[[1, 2, 3][0], [4][0], [5][0], [][0], [][0], [][0]
		"""
		self.state[position][1] = 0

	def take_round_bet(self, id):
		"""Bet on a camel and return the bet value."""
		if self.round_bets[id][-1] == 0:
			assert False, "No more bets left for this camel."

		return self.round_bets[id].pop()

	def view_round_bets(self):
		"""Returns a dictionary id : bets."""
		d = {}
		for k in self.round_bets.key():
			d[k] = self.round_bets[k][-1]
		return d

	def reset_round(self):
		"""Defines a new round."""
		# reset moved camels
		self.moved_camels = []

		# remove all powerups
		for place in self.state:
			place[1] = 0

		# reset round bets
		for i in range(1, 6):
			self.round_bets[i] = [0, 2, 2, 3, 5]

	def losing_camel(self):
		"""Returns id of the camel in last place."""
		for place in self.state:
			if place[0] != []:
				return place[0][0]

	def winning_camel(self):
		"""Returns id of the camel in first place."""
		for i in range(len(self.state) - 1, 0, -1):
			camels = self.state[i][0]
			if camels != []:
				return camels[-1]

	def second_place_camel(self):
		"""Returns id of the camel in second place."""
		found_first = False
		for i in range(len(self.state) - 1, 0, -1):
			camels = self.state[i][0]
			if len(camels) > 0:
				if found_first:
					return camels[-1]
				if len(camels) == 1:
					found_first = True
				else:
					return camels[len(camels) - 2]

	# def add_camel(self, camel_id, position):
	# 	"""Adds a camel at position."""
	# 	# self.state[position].add_camels([camel_id])
	# 	self.state[position][0] += [camel_id]

	def fast_copy_state(self):
		"""Returns a copy of self.state, and does it FAST."""
		return [[[c for c in place[0]], place[1]] for place in self.state]

	def __repr__(self):
		return str(self.state)

"""d = {0: [1, 2, 3], 1: [4], 2: [5]}
b = Board(d)"""

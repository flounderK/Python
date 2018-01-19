from random import shuffle

class card:
	"""A Basic playing card representation"""
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value

	def display(self):
		return self.__dict__

class deck(list):
	"""A representation of a deck of playing cards"""
	def __init__(self):
		super(deck, self).__init__()
		for k in ['clubs','hearts','spades','diamonds']:
			for i in range(2,11):
				self.append(card(suit=k, value=i))
			for i in ['J','Q','K','A']:
				self.append(card(suit=k, value=i))
		self.shuffle()

	def shuffle(self):
		shuffle(self)

	def draw(self):
		return self.pop().__dict__

	def view_deck(self):
		view = list()
		for i in self:
		 	view.append(i.__dict__)
		return view


class player:
	def __init__(self):
		self.hand = list()

	def __look_at_hand(self):
		view=list()
		for i in self.hand:
			view.append(i.__dict__)
		return view

	def draw(self, deck):
		pass

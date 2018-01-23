from random import shuffle

class card:
	"""A Basic playing card representation"""
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value

	def display(self):
		result =(str(self.__dict__['value']) + " of " +
				 str(self.__dict__['suit']))
		return result


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
		return self.pop()

	def reset(self):
		self.clear()
		self.__init__()

	# def view_deck(self):
	# 	view = list()
	# 	for i in self:
	# 	 	view.append(i.__dict__)
	# 	return view


class player:
	def __init__(self,name=None, cash=500):
		self.hand = list()
		self.cash = cash
		self.current_bet = 0

	def bet(self, cash):
		if cash > self.cash:
			return "You dont have that much money"

		self.cash = self.cash - cash
		self.current_bet = self.current_bet + cash

	def add_money(self, amount):
		self.cash = self.cash + amount

	def look_at_hand(self):
		view=list()
		for i in self.hand:
			view.append(i.display())
		return view

	def draw(self, deck):
		self.hand.append(deck.draw())

	def return_cards(self):
		self.hand.clear()

class game:
	def __init__(self):
		self.played_cards = list()
		self.pot = 0
		self.current_bid = 10
		self.players = list()

	def add_player(self, player):
		self.players.append(player)

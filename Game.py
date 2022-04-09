import random
from Player import Player
from Card import Card

class Game:
  def printPlayer(self, player):
    self.players[player].print()
  
  def printHand(self, player):
    self.players[player].printHand()

  def getHand(self, player):
    return self.players[player].hand

  def printActive(self, player):
    cards = []
    for card in self.active[player]:
      cards.append(card.name)
    print(", ".join(cards))

  def endTurn(self, player):
    self.end[player] = True

    if self.end[0] and self.end[1]:
      self.cardInteraction()
  
  def playCard(self, player, card):
    c = self.players[player].getCard(card)
    if (self.players[player].mana > c.manaCost):
      self.active[player].append(c)
      self.players[player].removeCard(c)
      self.players[player].reduceMana(c.manaCost)
    else:
      # cannot play card
      pass

  def getTotalDamage(self, player):
    sum = 0
    for c in self.active[player]:
      sum = sum + c.damage
    return sum

  def cardInteraction(self):
    sum_p1 = self.getTotalDamage(0)
    sum_p2 = self.getTotalDamage(1)

    for c in self.active[0]:
      if sum_p2 < c.defense:
        c.defense -= sum_p2
        break
      else:
        self.active[0].remove(c)
        sum_p2 -= c.defense
    for c in self.active[1]:
      if sum_p1 < c.defense:
        c.defense -= sum_p1
        break
      else:
        self.active[1].remove(c)
        sum_p1 -= c.defense

    self.players[0].reduceHealth(sum_p2)
    self.players[1].reduceHealth(sum_p1)

    self.end = [False, False]

    self.players[0].addCard(random.choice(deck).__copy__())
    self.players[1].addCard(random.choice(deck).__copy__())
    
  def dealHands(self):
    for i in range(5):
      self.players[0].addCard(random.choice(deck).__copy__())
      self.players[1].addCard(random.choice(deck).__copy__())

  def __init__(self):
    self.players = [Player(), Player()]
    self.end = [False, False]
    self.active = [[], []]

    self.dealHands()

deck = [
  Card("Knight", 2, 3, 2), Card("Knight", 2, 3, 2),
  Card("Squire", 1, 2, 3), Card("Squire", 1, 2, 3), 
  Card("Minions", 6, 4, 3), Card("Minions", 6, 4, 3), 
  Card("Wyvern", 8, 7, 6),
  Card("Ninja", 3, 5, 1)
]

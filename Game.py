import random
import json
import time
from Player import Player
from Card import Card

class Game:
  def getGameState(self):
    return json.dumps({
      "gameOver": self.gameOver,
      "winner": self.winner,
      "end": self.end,
      "turnNumber": self.turnNumber,
      "currentPlayer": self.currentPlayer,
      "turnCounter": self.turnCounter
    })

  def register(self):
    if not self.registered[0]:
      self.registered[0] = True
      return 0
    elif not self.registered[1]:
      self.registered[1] = True
      return 1
    else:
      return None

  def getPlayerInfo(self, player):
    return json.dumps({
      "health": self.players[player].health,
      "mana": self.players[player].mana
    })
  
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

  def getActive(self, player):
    cards = []
    for card in self.active[player]:
      cards.append(card.toDict())
    return json.dumps(cards)

  def endTurn(self, player):
    if player != self.currentPlayer:
      return

    self.end[player] = True

    #self.currentPlayer = (self.currentPlayer + 1) % 2
    self.turnNumber += 1
    self.currentPlayer = self.turnNumber % 2
    self.turnCounter = int(self.turnNumber / 2)

    if self.end[0] and self.end[1]:
      time.sleep(5)
      self.cardInteraction()
      self.players[0].addMana(3)
      self.players[1].addMana(3)

      if self.players[0].health <= 0 and self.players[1].health > 0:
        self.gameOver = True
        self.winner = 1
        # player 2 wins
      elif self.players[1].health <= 0 and self.players[0].health > 0:
        self.gameOver = True
        self.winner = 0
        pass
        # player 1 wins
      elif self.players[0].health <= 0 and self.players[1].health <= 0:
        pass
        # tie
  
  def playCard(self, player, card):
    if player != self.currentPlayer:
      return
    
    c = self.players[player].getCard(card)
    if (self.players[player].mana >= c.manaCost):
      self.active[player].append(c)
      self.players[player].removeCard(c)
      self.players[player].reduceMana(c.manaCost)

      self.active[player].sort(key=lambda x: x.priority)
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

    self.active[0].sort(key=lambda x: x.priority)
    self.active[1].sort(key=lambda x: x.priority)

    for c in self.active[0]:
      if sum_p2 < c.defense:
        c.defense -= sum_p2
        sum_p2 = 0
      else:
        self.active[0].remove(c)
        sum_p2 -= c.defense
    for c in self.active[1]:
      if sum_p1 < c.defense:
        c.defense -= sum_p1
        sum_p1 = 0
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
      self.players[0].addCard(deck[12].__copy__())

  def reset(self):
    self.players = [Player(), Player()]
    self.end = [False, False]
    self.active = [[], []]
    self.registered = [False, False]
    self.currentPlayer = 0
    self.turnNumber = 0
    self.turnCounter = 0

    self.gameOver = False
    self.winner = -1

    self.dealHands()

  def __init__(self):
    self.reset()

deck = [
  #negative priority goes first, positive goes last (last value)
  Card("Knight", 2, 3, 2, 0), Card("Knight", 2, 3, 2, 0),
  Card("Squire", 1, 2, 3, 0), Card("Squire", 1, 2, 3, 0), 
  Card("Minions", 6, 4, 4, -1), Card("Minions", 6, 4, 4, -1), 
  Card("Boar", 1, 1, 2, 0), Card("Boar", 1, 1, 2, 0),
  Card("Bobcat", 1, 2, 1, 0), Card("Bobcat", 1, 2, 1, 0),
  Card("Wyvern", 8, 7, 6, 0),
  Card("Ninja", 3, 5, 1, 0),
  Card("Wood Elf", 4, 4, 1, 2), 
  Card("Giant Turtle", 5, 0, 8, -2)
]

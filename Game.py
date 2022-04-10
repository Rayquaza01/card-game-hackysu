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
      self.cardInteraction()
      self.players[0].addMana(3)
      self.players[1].addMana(3)
      self.players[0].print()

      self.end = [False, False]

      self.players[0].addCard(random.choice(deck).__copy__())
      self.players[1].addCard(random.choice(deck).__copy__())

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
      if c.name == "Sun Card":
        if self.players[player].health <= 28:
          self.players[player].health = self.players[player].health + 2
        else:
          return

      if c.name == "Shield":
        if self.players[player].health <= 33:
          self.players[player].health = self.players[player].health + 2
        else:
          return

      if c.name == "Draw":
        self.players[player].addCard(random.choice(deck).__copy__())
        self.players[player].addCard(random.choice(deck).__copy__())

      if c.name == "Inspire":
        OK = False
        for card in self.active[player][::-1]:
          if card.defense == 0:
            continue
          else:
            card.damage = card.damage + 2
            OK = True
            break
        if not OK:
          return

      if c.name == "Harden":
        OK = False
        for card in self.active[player]:
          if card.defense == 0:
            continue
          else:
            card.defense = card.defense + 2
            OK = True
            break
        if not OK:
          return
        
      if c.name == "Fearsome Presence":
        OK = False
        for card in self.active[(player + 1) % 2][::-1]:
          if card.defense == 0:
            continue
          else:
            c.defense = card.damage
            c.toBeRemoved = True
            OK = True
            break
        if not OK:
          return

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
      if c.defense == 0:
        c.toBeRemoved = True
    return sum

  def cardInteraction(self):
    player1TotalDamage = self.getTotalDamage(0)
    player2TotalDamage = self.getTotalDamage(1)

    self.active[0].sort(key=lambda x: x.priority)
    self.active[1].sort(key=lambda x: x.priority)

    # loop through player 1's active cards
    # p1ActiveCopy = copy.deepcopy(self.active[0])
    # p1ActiveCopy = []
    # for card in self.active[0]:
    #   p1ActiveCopy.append(card)

    for card in self.active[0]:
      # spells have no health
      if card.defense == 0:
        continue

      # if player 2 does not kill card
      if player2TotalDamage < card.defense:
        card.defense = card.defense - player2TotalDamage
        player2TotalDamage = 0
      elif player2TotalDamage > card.defense:
        # player 2 kills card and has damage left over
        # self.active[0].remove(card)
        card.toBeRemoved = True
        player2TotalDamage = player2TotalDamage - card.defense
        print(self.active)
      else:
        # player 2 kills card and has no damage left over
        # self.active[0].remove(card)
        card.toBeRemoved = True
        player2TotalDamage = 0

    self.active[0] = list(filter(lambda x: not x.toBeRemoved, self.active[0]))
        
    # loop through player 1's active cards
    # p2ActiveCopy = copy.deepcopy(self.active[1])
    for card in self.active[1]:
      # if player 1 does not kill card
      if player1TotalDamage < card.defense:
        card.defense = card.defense - player1TotalDamage
        player1TotalDamage = 0
      elif player1TotalDamage > card.defense:
        # player 1 kills card and has damage left over
        # self.active[1].remove(card)
        card.toBeRemoved = True
        player1TotalDamage = player1TotalDamage - card.defense
      else:
        # player 1 kills card and has no damage left over
        # self.active[1].remove(card)
        card.toBeRemoved = True
        player1TotalDamage = 0

    self.active[1] = list(filter(lambda x: not x.toBeRemoved, self.active[1]))

#    for c in self.active[0]:
#      if sum_p2 < c.defense:
#        c.defense -= sum_p2
#        sum_p2 = 0
#      else:
#        self.active[0].remove(c)
#        sum_p2 -= c.defense
#
#    for c in self.active[1]:
#      if sum_p1 < c.defense:
#        c.defense -= sum_p1
#        sum_p1 = 0
#      else:
#        self.active[1].remove(c)
#        sum_p1 -= c.defense

    self.players[0].reduceHealth(player2TotalDamage)
    self.players[1].reduceHealth(player1TotalDamage)
    
  def dealHands(self):
    for i in range(5):
      self.players[0].addCard(random.choice(deck).__copy__())
      self.players[1].addCard(random.choice(deck).__copy__())
    # debug priority stuff
    self.players[0].addCard(deck[14].__copy__())
    self.players[1].addCard(deck[14].__copy__())
    self.players[0].addCard(deck[12].__copy__())
    self.players[1].addCard(deck[12].__copy__())
    self.players[0].addCard(deck[19].__copy__())
    self.players[0].addCard(deck[20].__copy__())
    self.players[1].addCard(deck[19].__copy__())
    self.players[1].addCard(deck[20].__copy__())

  def reset(self):
    self.players = [Player(13), Player(10)]
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
  Card("Giant Turtle", 5, 0, 8, -2), 
  Card("Fireball!", 3, 2, 0, 3), #Fireball: Spell that does 2 damage 
  Card("Inspire", 3, 0, 0, 3), #Inspire: Spell that adds 2 damage to the lowest priority non-spell card
  Card("Harden", 3, 0, 0, 3),
  Card("Sun Card", 3, 0, 0, 3),
  Card("Draw", 3, 0, 0, 3),
  Card("Shield", 3, 0, 0, 3),
  Card("Fearsome Presence", 3, 0, 0, -3)
]

class Player:
  def print(self):
    print("Health: " + str(self.health) + " Mana: " + str(self.mana))
  
  def reduceMana(self, cost):
    self.mana = self.mana - cost

  def addMana(self, amnt):
    self.mana = self.mana + amnt

  def reduceHealth(self, dmg):
    self.health = self.health - dmg

  def getCard(self, idx):
    return self.hand[idx]

  def addCard(self, card):
    self.hand.append(card)

  def removeCard(self, card):
    #del self.hand[idx]
    self.hand.remove(card)

  def printHand(self):
    cards = []
    for card in self.hand:
      cards.append(card.name)
    print(", ".join(cards))

  def __init__(self):
    self.health = 30
    self.mana = 25
    self.hand = []

class Card:
  def toDict(self):
    return {
      "name": self.name,
      "manaCost": self.manaCost,
      "damage": self.damage,
      "defense": self.defense,
      "priority": self.priority
    }
  
  def print(self):
    print("Card name: " + self.name)
    print("Mana Cost: " + str(self.manaCost))
    print("Damage: " + str(self.damage))
    print("Health: " + str(self.defense))
  
  def __copy__(self):
    return Card(self.name, self.manaCost, self.damage, self.defense, self.priority)

  def reduceHealth(self, dmg):
    self.defense = self.defense - dmg

  def __init__(self, name, manaCost, damage, defense, priority):
    self.name = name
    self.manaCost = manaCost
    self.damage = damage
    self.defense = defense
    self.priority = priority
    self.toBeRemoved = False

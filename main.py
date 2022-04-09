from Game import Game
import sys

obj = Game()

p = 0
while True:
  while not obj.gameOver:
    print("Player 1 Stats:")
    obj.printPlayer(0)
    print("Player 1 Active Cards:", end=" ")
    obj.printActive(0)
    print()
  
    print("Player 2 Stats:")
    obj.printPlayer(1)
    print("Player 2 Active Cards:", end=" ")
    obj.printActive(1)
    print()
    
    print("Your hand: ")
    obj.printHand(p)
    print("What would you like to do?")
    command = input("play / inspect / end / help: ").strip().lower()
  
    if (command == "play"):
      card = input("Enter card number: ")
      obj.playCard(p, int(card) - 1)
    elif command == "end":
      obj.endTurn(p)
      p = 0 if p == 1 else 1
    elif command == "inspect":
        card = input("Enter card number: ")
        obj.getHand(p)[int(card) - 1].print()
    elif command == "help":
      pass
    else:
      print("\nInvalid input.\n")

  print("Player " + str(obj.winner + 1) + " Wins!")
  
  ans = input("Would you like to play again? ")
  if ans == "y":
    obj.reset()
  else:
    sys.exit()
from Game import Game
import json
from flask import Flask, request

game = Game()

app = Flask(__name__)

@app.route("/")
def root():
  return "Card Game Server\n"

@app.route("/getHand")
def getHand():
  req = request.get_json()
  hand = game.getHand(req.player)
  hand_dict = []
  for x in hand:
    hand_dict.append(x.toDict())
  return json.dumps(hand_dict)

@app.route("/playCard")
def playCard():
  req = request.get_json()
  game.playCard(req.card)
  return "OK"

if __name__ == "__main__":
    app.run()

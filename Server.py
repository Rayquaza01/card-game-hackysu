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
  print(request.args)
  hand = game.getHand(int(request.args["player"]))
  hand_dict = []
  for x in hand:
    hand_dict.append(x.toDict())
  return json.dumps(hand_dict)

@app.route("/getActive")
def getActive():
  active = game.getActive(int(request.args["player"]))
  return active

@app.route("/playCard")
def playCard():
  game.playCard(int(request.args["player"]), int(request.args["card"]))
  return "OK"

@app.route("/getState")
def getGameState():
  return game.getGameState()

@app.route("/register")
def register():
  return json.dumps({"player": game.register()})

@app.route("/reset")
def reset():
  game.reset()
  return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

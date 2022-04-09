from flask import Flask, request

app = Flask(__name__)

@app.route("/playCard")
def root():
    return "Test"

@app.route("/getHand")
def getHand():
    return "{}"

if __name__ == "__main__":
    app.run()

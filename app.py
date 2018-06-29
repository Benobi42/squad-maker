import json

from flask import Flask, render_template, request

from players import PlayerList
from squads import getBalancedSquads

app = Flask(__name__)


@app.route("/")
def main():
    """
    Default page for webpage, which loads player data from a JSON file,
    and outputs them to a waiting list, which is displayed on the page.
    """
    playerList = PlayerList.fromJSON()
    playerList.toHTML()
    return render_template('index.html')


@app.route("/squads", methods=["POST"])
def generateSquads():
    """
    Generate a number of balanced squads equivalent to the user's input from
    the given player data, and enable them to be displayed on the new page.
    """
    numSquads = int(request.form["numSquads"])
    playerList = PlayerList.fromJSON()
    squads = getBalancedSquads(numSquads, playerList)
    squadsHTML = [("squad%d.html" % (i+1)) for i in range(numSquads)]

    return render_template('index.html', squads=squadsHTML)


if __name__ == "__main__":
    """
    When calling this file in the command line, run the application

    Configures the application to reload templates if their contents change,
    to avoid old data from persisting after updating.
    """
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()

"""Flask Application for Hockey Squad Builder."""
from flask import Flask, render_template, request

from players import PlayerList
from squads import getBalancedSquads

app = Flask(__name__)


@app.route("/")
def main():
    """
    Render the default page for application.

    Loads player data from a JSON file, and puts all players
    on a waiting list, which is displayed on the page.
    """
    playerList = PlayerList.fromJSON()

    return render_template('index.html', waitingList=playerList.toHTML(),
                           numPlayers=len(playerList.players))


@app.route("/squads", methods=["POST"])
def generateSquads():
    """
    Generate balanced squads and display them.

    Generate a number of balanced squads equivalent to the user's input from
    the given player data, and enable them to be displayed on the new page.
    """
    numSquads = int(request.form["numSquads"])
    playerList = PlayerList.fromJSON()
    numPlayers = len(playerList.players)
    try:
        squads = getBalancedSquads(numSquads, playerList)
    except Exception as err:
        return render_template('index.html', waitingList=playerList.toHTML(),
                               numPlayers=numPlayers, errorPopup=err)

    return render_template('index.html', waitingList=playerList.toHTML(),
                           numPlayers=numPlayers,
                           squads=[squad.toHTML() for squad in squads])


if __name__ == "__main__":
    """
    When calling this file in the command line, run the application.

    Configures the application to reload templates if their contents change,
    to avoid old data from persisting after updating.
    """
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0")

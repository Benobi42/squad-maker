"""Flask Application for Hockey Squad Builder."""

from flask import Flask, render_template

from players import PlayerList

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


if __name__ == "__main__":
    """When calling this file in the command line, run the application."""

    app.run(host="0.0.0.0")

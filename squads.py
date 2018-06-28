from math import floor

from players import Player, PlayerList, PlayerTable, writeHTMLToFile


AVERAGENAME = 'Average'


class Squad(PlayerList):
    """Representation of a Squad

    A squad is a group of players, with an identifying number.

    When printing out to HTML, the last entry in the squad contains
    the average values for each of the skills across the team.
    """
    def __init__(self, squadNum, players):
        """
        Create a Squad
        """
        self.squadNum = squadNum
        self.players = players

    def getAveragePlayer(self):
        """
        Get a player that represents the average of each of the
        skills across the whole team
        """
        skateSum = 0
        shootSum = 0
        checkSum = 0
        for player in self.players:
            skateSum += player.skate
            shootSum += player.shoot
            checkSum += player.check

        pLen = len(self.players)
        return Player(None, AVERAGENAME, floor(skateSum/pLen),
                      floor(shootSum/pLen), floor(checkSum/pLen))

    def toHTML(self):
        """
        Output the squad as a table to an HTML file with its corresponding
        squad number
        """
        self.players.append(self.getAveragePlayer())
        self.table = PlayerTable(self.players, ["playerList"])
        html = self.table.__html__()
        self.players.pop()

        fn = "templates/squad%d.html" % self.squadNum
        writeHTMLToFile(html, fn)

        return html

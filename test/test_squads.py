import squads

from math import floor
from unittest import TestCase
from unittest.mock import mock_open, patch

from players import Player, PlayerList, PlayerTable


class TestSquad(TestCase):
    player1 = Player("123", "Ben Schreiber", 51, 51, 51)
    player2 = Player("99", "Wayne Gretzky", 99, 99, 99)
    playerList = PlayerList([player1, player2])

    def testGetAveragePlayer(self):
        expectedAvg = floor((51+99)/2)
        expectedAvgPlayer = Player(None, squads.AVERAGENAME, expectedAvg,
                                   expectedAvg, expectedAvg)

        squad = squads.Squad(1, [self.player1, self.player2])
        self.assertEqual(squad.getAveragePlayer(), expectedAvgPlayer)

    def testToHTML(self):
        squad = squads.Squad(1, [self.player1, self.player2])
        averagePlayer = squad.getAveragePlayer()
        outputPlayers = squad.players
        outputPlayers.append(averagePlayer)
        expectedHTML = PlayerTable(outputPlayers, ["playerList"]).__html__()
        removed = outputPlayers.pop()
        self.assertEqual(removed, averagePlayer)

        with patch("builtins.open", mock_open()) as mock_file:
            html = squad.toHTML()

        self.assertEqual(html, expectedHTML)
        self.assertEqual(squad.players, outputPlayers)

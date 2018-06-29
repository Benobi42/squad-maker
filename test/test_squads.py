import squads

from math import floor
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

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


class TestBitReverse(TestCase):

    def testBitReverse(self):
        value = 3           # Binary representation 011
        expectedValue = 6   # Binary representation 110
        maxValue = 7        # Binary representation 111

        revValue = squads.bitReverse(value, maxValue)
        self.assertEqual(revValue, expectedValue)

    def testBitReverse__oneToMax(self):
        value = 1       # Binary representation 0001, reverses to 1000
        maxValue = 8    # Binary representation 1000

        revValue = squads.bitReverse(value, maxValue)
        self.assertEqual(revValue, maxValue)

    def testBitReverse__oneToOne(self):
        value = 1       # Binary representation 1
        maxValue = 1
        self.assertEqual(squads.bitReverse(value, maxValue), value)

    def testBitReverse__raisesValueError(self):
        value = 9
        maxValue = 8

        with self.assertRaises(ValueError):
            squads.bitReverse(value, maxValue)


class testTournamentRank(TestCase):

    def testTournamentRank(self):
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)     # Becomes 4
        player2 = Player("97", "Connor McDavid", 97, 97, 97)    # Becomes 2
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)    # Becomes 6
        player4 = Player("456", "Another Skater", 42, 42, 42)   # Becomes 1
        player5 = Player("789", "That Guy", 31, 31, 31)         # Becomes 5
        player6 = Player("404", "Nota RealPlayer", 20, 20, 20)  # Becomes 3

        players = [player1, player2, player3, player4, player5, player6]
        expectedTournament = [player4, player2, player6,
                              player1, player5, player3]
        tournament = squads.tournamentRank(players)
        self.assertEqual(tournament, expectedTournament)

    def testTournamentRank__single(self):
        player = Player("123", "Ben Schreiber", 51, 51, 51)
        self.assertEqual([player], squads.tournamentRank([player]))

    def testTournamentRank__doubleSwap(self):
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("123", "Ben Schreiber", 51, 51, 51)

        players = [player1, player2]
        expectedTournament = [player2, player1]
        tournament = squads.tournamentRank(players)
        self.assertEqual(tournament, expectedTournament)

    def testTournamentRankSorts(self):
        """
        Test that the tournament ranker sorts the given players before slotting
        """
        player1 = Player("123", "Ben Schreiber", 51, 51, 51)
        player2 = Player("99", "Wayne Gretzky", 99, 99, 99)

        players = [player1, player2]
        expectedTournament = [player1, player2]
        tournament = squads.tournamentRank(players)
        self.assertEqual(tournament, expectedTournament)

    def testTournamentRankSortsByHighSkill(self):
        """
        Test that the tournament ranker sorts the given players by their
        highest skill

        Since the skill of 100 is greater than 99, player 1 is now
        considered the "highest ranked" player when generating the tournament
        """
        player1 = Player("123", "Ben Schreiber", 51, 51, 100)
        player2 = Player("99", "Wayne Gretzky", 99, 99, 99)

        players = [player1, player2]
        expectedTournament = [player2, player1]
        tournament = squads.tournamentRank(players)
        self.assertEqual(tournament, expectedTournament)


class TestGetBalancedSquads(TestCase):

    @patch('players.PlayerList.toHTML', MagicMock)
    @patch('squads.Squad.toHTML', MagicMock)
    def testGetBalancedSquads(self):
        numSquads = 2
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        expectedSquads = [squads.Squad(1, [player4, player3]),
                          squads.Squad(2, [player2, player1])]

        balSquads = squads.getBalancedSquads(numSquads, playerList)

        self.assertEqual(balSquads, expectedSquads)

    @patch('players.PlayerList.toHTML', MagicMock)
    @patch('squads.Squad.toHTML', MagicMock)
    def testGetBalancedSquads__OneSquad(self):
        numSquads = 1
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        expectedSquads = [squads.Squad(1, playerList.players)]

        balSquads = squads.getBalancedSquads(numSquads, playerList)
        self.assertEqual(balSquads, expectedSquads)
        self.assertEqual(playerList.players, [])

    @patch('players.PlayerList.toHTML', MagicMock)
    @patch('squads.Squad.toHTML', MagicMock)
    def testGetBalancedSquads__NSquads(self):
        numSquads = 4
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        expectedSquads = [squads.Squad(1, [player4]),
                          squads.Squad(2, [player3]),
                          squads.Squad(3, [player2]),
                          squads.Squad(4, [player1])]

        balSquads = squads.getBalancedSquads(numSquads, playerList)

        self.assertEqual(balSquads, expectedSquads)
        self.assertEqual(playerList.players, [])

    def testGetBalancedSquadsRaisesValueError__GreaterThanNSquads(self):
        numSquads = 5
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        with self.assertRaises(ValueError):
            balSquads = squads.getBalancedSquads(numSquads, playerList)

    def testGetBalancedSquadsRaisesValueError__ZeroSquads(self):
        numSquads = 0
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        with self.assertRaises(ValueError):
            balSquads = squads.getBalancedSquads(numSquads, playerList)

    def testGetBalancedSquadsRaisesValueError__NegSquads(self):
        numSquads = -1
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        with self.assertRaises(ValueError):
            balSquads = squads.getBalancedSquads(numSquads, playerList)

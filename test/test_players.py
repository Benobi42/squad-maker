"""Unittests for players module."""
import players

from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch


TESTJSON = {
    "players": [
        {
            "_id": "123",
            "firstName": "Ben",
            "lastName": "Schreiber",
            "skills": [
                {
                   "type": "Shooting",
                    "rating": 90
                },
                {
                    "type": "Skating",
                    "rating": 50
                },
                {
                    "type": "Checking",
                    "rating": 99
                }
            ]
        },
        {
            "_id": "99",
            "firstName": "Wayne",
            "lastName": "Gretzky",
            "skills": [
                {
                    "type": "Shooting",
                    "rating": 85
                },
                {
                    "type": "Skating",
                    "rating": 99
                },
                {
                    "type": "Checking",
                    "rating": 80
                }
            ]
        }
    ]
}


class TestPlayer(TestCase):
    """Tests for Player class."""

    def testSkating(self):
        """Test getting a player's skating attribute."""
        skills = {players.Skill.Skating: 50, players.Skill.Shooting: 40,
                  players.Skill.Checking: 60}
        player = players.Player("123", "Ben Schreiber", skills)

        self.assertEqual(player.skating, skills[players.Skill.Skating])

    def testShooting(self):
        """Test getting a player's skating attribute."""
        skills = {players.Skill.Skating: 50, players.Skill.Shooting: 40,
                  players.Skill.Checking: 60}
        player = players.Player("123", "Ben Schreiber", skills)

        self.assertEqual(player.shooting, skills[players.Skill.Shooting])

    def testChecking(self):
        """Test getting a player's skating attribute."""
        skills = {players.Skill.Skating: 50, players.Skill.Shooting: 40,
                  players.Skill.Checking: 60}
        player = players.Player("123", "Ben Schreiber", skills)

        self.assertEqual(player.checking, skills[players.Skill.Checking])

    def testEquality(self):
        """Test that a player is equal to itself."""
        skills = {players.Skill.Skating: 50, players.Skill.Shooting: 50,
                  players.Skill.Checking: 50}
        player1 = players.Player("123", "Ben Schreiber", skills)
        player2 = players.Player("123", "Ben Schreiber", skills)
        self.assertEqual(player1, player2)

    def testInequality(self):
        """Test that two different players are not equal."""
        skills1 = {players.Skill.Skating: 50, players.Skill.Shooting: 50,
                   players.Skill.Checking: 50}
        skills2 = {players.Skill.Skating: 99, players.Skill.Shooting: 99,
                   players.Skill.Checking: 99}
        player1 = players.Player("123", "Ben Schreiber", skills1)
        player2 = players.Player("99", "Wayne Gretzky", skills2)
        self.assertNotEqual(player1, player2)

    def testInequality__oneAttribute(self):
        """
        Test Player Inequality.

        Two players are not equal if at least one attribute is different.
        """
        skills = {players.Skill.Skating: 50, players.Skill.Shooting: 50,
                  players.Skill.Checking: 50}
        player1 = players.Player("123", "Ben Schreiber", skills)
        player2 = players.Player("124", "Ben Schreiber", skills)
        self.assertNotEqual(player1, player2)

    def testFromJSON(self):
        """Test that expected JSON data can be turned into a Player."""
        data = {"_id": "123", "firstName": "Ben", "lastName": "Schreiber",
                "skills": [{"type": players.Skill.Skating.name, "rating": 50},
                           {"type": players.Skill.Shooting.name, "rating": 50},
                           {"type": players.Skill.Checking.name,
                            "rating": 50}]}

        skills = {players.Skill.Skating: 50, players.Skill.Shooting: 50,
                  players.Skill.Checking: 50}
        expectedPlayer = players.Player("123", "Ben Schreiber", skills)
        player = players.Player.fromJSON(data)
        self.assertEqual(player, expectedPlayer)


class TestGetSkillRatings(TestCase):
    """Tests for getSkillRatings method."""

    def testGetSkillRatings(self):
        """Test getting the Skating skill."""
        data = {"_id": "123", "firstName": "Ben", "lastName": "Schreiber",
                "skills": [{"type": players.Skill.Skating.name,
                            "rating": 50},
                           {"type": players.Skill.Shooting.name,
                            "rating": 40},
                           {"type": players.Skill.Checking.name,
                            "rating": 60}]}

        expectedSkills = {players.Skill.Skating: 50,
                          players.Skill.Shooting: 40,
                          players.Skill.Checking: 60}
        self.assertEqual(players.getSkillRatings(data), expectedSkills)


class TestPlayerList(TestCase):
    """Tests for PlayerList class."""

    skills1 = {players.Skill.Skating: 50, players.Skill.Shooting: 90,
               players.Skill.Checking: 99}
    skills2 = {players.Skill.Skating: 99, players.Skill.Shooting: 85,
               players.Skill.Checking: 80}
    skills3 = {players.Skill.Skating: 90, players.Skill.Shooting: 97,
               players.Skill.Checking: 90}
    player1 = players.Player("123", "Ben Schreiber", skills1)
    player2 = players.Player("99", "Wayne Gretzky", skills2)
    player3 = players.Player("97", "Connor McDavid", skills3)

    def testSortedPlayers(self):
        """Test sorting the player list defaults to sorting by name."""
        myList = [self.player1, self.player2, self.player3]
        playerList = players.PlayerList(myList)

        self.assertEqual(playerList.sortedPlayers(),
                         sorted(myList, key=lambda p: p.name))

    def testSortedPlayersSkating(self):
        """Test sorting the player list sorting by the Skating rating."""
        myList = [self.player1, self.player2, self.player3]
        playerList = players.PlayerList(myList)

        self.assertEqual(playerList.sortedPlayers(players.Skill.Skating),
                         sorted(myList, key=lambda p: p.skating))

    def testSortedPlayersShooting(self):
        """Test sorting the player list sorting by the Shooting rating."""
        myList = [self.player1, self.player2, self.player3]
        playerList = players.PlayerList(myList)

        self.assertEqual(playerList.sortedPlayers(players.Skill.Shooting),
                         sorted(myList, key=lambda p: p.shooting))

    def testSortedPlayersChecking(self):
        """Test sorting the player list sorting by the Checking rating."""
        myList = [self.player1, self.player2, self.player3]
        playerList = players.PlayerList(myList)

        self.assertEqual(playerList.sortedPlayers(players.Skill.Checking),
                         sorted(myList, key=lambda p: p.checking))

    def testEquality(self):
        """
        Test PlayerList Equality.

        Two PlayerLists are equal if they contain the same list of Players.
        """
        playerList1 = players.PlayerList([self.player1, self.player2])
        playerList2 = players.PlayerList([self.player1, self.player2])
        self.assertEqual(playerList1, playerList2)

    def testInquality(self):
        """
        Test PlayerList Inequality.

        Two PlayerLists are not equal if they have a different list of Players.
        """
        playerList1 = players.PlayerList([self.player1, self.player2])
        playerList2 = players.PlayerList([self.player1])
        self.assertNotEqual(playerList1, playerList2)

    @patch("json.load", MagicMock(return_value=TESTJSON))
    def testFromJSON(self):
        """Test that a PlayerList can be created from JSON data."""
        expectedPlayerList = players.PlayerList([self.player1, self.player2])

        with patch("builtins.open", mock_open()):
            playerList = players.PlayerList.fromJSON("myJSONFile")

        self.assertEqual(playerList, expectedPlayerList)

    def testToHTML(self):
        """Test that toHTML outputs the expected HTML data."""
        playerList = players.PlayerList([self.player1, self.player2])
        expectedHTML = playerList.table.__html__()
        html = playerList.toHTML()

        self.assertEqual(html, expectedHTML)

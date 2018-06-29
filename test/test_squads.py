"""Unittests for Squad functionality."""
import squads

from unittest import TestCase

from players import Player, Skill


class TestSquad(TestCase):
    """Tests for the Squad class."""

    def testSkating(self):
        """Test getting the total value of skating in the squad."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        expectedSkating = sum([p.skating for p in players])
        squad = squads.Squad(1, players)
        self.assertEqual(squad.skating, expectedSkating)

    def testShooting(self):
        """Test getting the total value of shooting in the squad."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        expectedShooting = sum([p.shooting for p in players])
        squad = squads.Squad(1, players)
        self.assertEqual(squad.shooting, expectedShooting)

    def testChecking(self):
        """Test getting the total value of checking in the squad."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        expectedChecking = sum([p.checking for p in players])
        squad = squads.Squad(1, players)
        self.assertEqual(squad.checking, expectedChecking)

    def testGetAverageSkating(self):
        """Test getting the average Skating rating of the squad."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        expectedAvgSkate = sum([p.skating for p in players])//len(players)
        squad = squads.Squad(1, players)
        self.assertEqual(squad.averageSkating, expectedAvgSkate)

    def testGetAverageSkatingEmpty(self):
        """Test that the average Skating rating of an empty squad is zero."""
        squad = squads.Squad(1, [])
        self.assertEqual(squad.averageSkating, 0)

    def testGetAverageShooting(self):
        """Test getting the average Shooting rating of the squad."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        expectedAvgShoot = sum([p.shooting for p in players])//len(players)
        squad = squads.Squad(1, players)
        self.assertEqual(squad.averageShooting, expectedAvgShoot)

    def testGetAverageShootingEmpty(self):
        """Test that the average Shooting rating of an empty squad is zero."""
        squad = squads.Squad(1, [])
        self.assertEqual(squad.averageShooting, 0)

    def testGetAverageChecking(self):
        """Test getting the average Checking rating of the squad."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        expectedAvgCheck = sum([p.checking for p in players])//len(players)
        squad = squads.Squad(1, players)
        self.assertEqual(squad.averageChecking, expectedAvgCheck)

    def testGetAverageCheckingEmpty(self):
        """Test that the average Checking rating of an empty squad is zero."""
        squad = squads.Squad(1, [])
        self.assertEqual(squad.averageChecking, 0)

    def testGetAveragePlayer(self):
        """Test getting the average player of the squad."""
        skills1 = {Skill.Skating: 51, Skill.Shooting: 51,
                   Skill.Checking: 51}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 99,
                   Skill.Checking: 99}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        averageSkating = sum([p.skating for p in players])//len(players)
        averageShooting = sum([p.shooting for p in players])//len(players)
        averageChecking = sum([p.checking for p in players])//len(players)
        expectedAvgSkills = {Skill.Skating: averageSkating,
                             Skill.Shooting: averageShooting,
                             Skill.Checking: averageChecking}

        expectedAvgPlayer = Player(squads.AVERAGEID, squads.AVERAGENAME,
                                   expectedAvgSkills)

        squad = squads.Squad(1, players)
        self.assertEqual(squad.averagePlayer, expectedAvgPlayer)

    def testGetAveragePlayer__odd(self):
        """Test getting the average player when the sum of skills is odd."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 50,
                   Skill.Checking: 50}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 99,
                   Skill.Checking: 99}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        averageSkating = sum([p.skating for p in players])//len(players)
        averageShooting = sum([p.shooting for p in players])//len(players)
        averageChecking = sum([p.checking for p in players])//len(players)
        expectedAvgSkills = {Skill.Skating: averageSkating,
                             Skill.Shooting: averageShooting,
                             Skill.Checking: averageChecking}

        expectedAvgPlayer = Player(squads.AVERAGEID, squads.AVERAGENAME,
                                   expectedAvgSkills)

        squad = squads.Squad(1, players)
        self.assertEqual(squad.averagePlayer, expectedAvgPlayer)

    def testGetAveragePlayer__differentValues(self):
        """Test getting the average player when players have varied skills."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 40,
                   Skill.Checking: 60}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 98,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        players = [player1, player2]

        averageSkating = sum([p.skating for p in players])//len(players)
        averageShooting = sum([p.shooting for p in players])//len(players)
        averageChecking = sum([p.checking for p in players])//len(players)
        expectedAvgSkills = {Skill.Skating: averageSkating,
                             Skill.Shooting: averageShooting,
                             Skill.Checking: averageChecking}

        expectedAvgPlayer = Player(squads.AVERAGEID, squads.AVERAGENAME,
                                   expectedAvgSkills)

        squad = squads.Squad(1, players)
        self.assertEqual(squad.averagePlayer, expectedAvgPlayer)

    def testGetAveragePlayer__oddNumPlayers(self):
        """Test getting the average player with more than two players."""
        skills1 = {Skill.Skating: 50, Skill.Shooting: 50,
                   Skill.Checking: 50}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 99,
                   Skill.Checking: 99}
        skills3 = {Skill.Skating: 97, Skill.Shooting: 97,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        player3 = Player("97", "Connor McDavid", skills3)

        players = [player1, player2, player3]

        averageSkating = sum([p.skating for p in players])//len(players)
        averageShooting = sum([p.shooting for p in players])//len(players)
        averageChecking = sum([p.checking for p in players])//len(players)
        expectedAvgSkills = {Skill.Skating: averageSkating,
                             Skill.Shooting: averageShooting,
                             Skill.Checking: averageChecking}

        expectedAvgPlayer = Player(squads.AVERAGEID, squads.AVERAGENAME,
                                   expectedAvgSkills)

        squad = squads.Squad(1, players)
        self.assertEqual(squad.averagePlayer, expectedAvgPlayer)

    def testToHTML(self):
        """
        Test outputting a squad to an HTML table.

        Verify that outputting the table adds the average row
        beneath the original table body.
        """
        skills1 = {Skill.Skating: 50, Skill.Shooting: 50,
                   Skill.Checking: 50}
        skills2 = {Skill.Skating: 99, Skill.Shooting: 99,
                   Skill.Checking: 99}
        skills3 = {Skill.Skating: 97, Skill.Shooting: 97,
                   Skill.Checking: 97}
        player1 = Player("123", "Ben Schreiber", skills1)
        player2 = Player("99", "Wayne Gretzky", skills2)
        player3 = Player("97", "Connor McDavid", skills3)
        squad = squads.Squad(1, [player1, player2, player3])

        expectedHTML = ('<table align="center" class="playerList">\n'
                        '<thead><tr><th>Name</th><th>Skating</th>'
                        '<th>Shooting</th><th>Checking</th></tr>'
                        '</thead>\n<tbody>\n<tr class="playerRow">'
                        '<td>Ben Schreiber</td><td>50</td><td>50</td>'
                        '<td>50</td></tr>\n<tr class="playerRow">'
                        '<td>Wayne Gretzky</td><td>99</td>'
                        '<td>99</td><td>99</td></tr>\n'
                        '<tr class="playerRow"><td>Connor McDavid</td>'
                        '<td>97</td><td>97</td><td>97</td></tr>\n'
                        '<tr class="avgRow"><td>Average</td><td>82</td>'
                        '<td>82</td><td>82</td></tr>\n</tbody>\n</table>')

        self.assertEqual(squad.toHTML(), expectedHTML)

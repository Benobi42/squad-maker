from enum import Enum

from players import Player, PlayerList, PlayerTable


AVERAGENAME = 'Average'
SQDKEY = "squad"


class Skills(Enum):
    skate = 1
    shoot = 2
    check = 3


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
        self.updateTable()

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
        return Player(None, AVERAGENAME, skateSum//pLen,
                      shootSum//pLen, checkSum//pLen)

    def toHTML(self):
        """
        Output the squad as a table to an HTML file with its corresponding
        squad number, and the average of all skills on the team at the
        bottom.
        """
        avgPlay = self.getAveragePlayer()
        self.updateTable()
        html = self.table.__html__()

        html = html.replace("</tbody>",
                            ("</tbody>\n<tbody class=avgRow>\n<tr>"
                             "<td><b>%s</b></td><td>%s</td><td>%s</td>"
                             "<td>%s</td></tr>\n</tbody>"
                             % (avgPlay.name, avgPlay.skate,
                                avgPlay.shoot, avgPlay.check)))

        return html


def getBalancedSquads(numSquads, playerList):
    """
    Dynamically generate closely-balanced squads of players from a given list

    The list of players is sorted on each of the three rankings into a separate
    list. During each iteration of the assignment loop, the current squad is
    the one with the lowest summation of one of the skills, and the available
    player with the highest skill in that category is added to the squad. Once
    a squad has the maximum number of players needed to get the desired number
    of squads from the player list, then no more players can be added.

    Errors if the number of desired squads is greater than the number of
    available players, or if number of desired squads is less than one.

    Special Cases:
        1 squad:    When only one squad is needed, all players are moved from
                    the waiting list into the squad.

        numPlayers squads:  When the number of players is equal to the number
                            of desired squads, each player is placed onto their
                            own squad, bypassing the need for calculations

    FUTURE OPTIMIZATION: Once a roughly balanced team is generated, go through
    and attempt to balance further by swapping players between teams
    """
    squads = []
    numPlayers = len(playerList.players)
    if(numSquads > numPlayers):
        raise ValueError(("Number of Squads cannot be greater then number of "
                          "players. %d squads attempted, %d players available."
                          % (numSquads, numPlayers)))
    elif(numSquads < 1):
        raise ValueError(("Number of Squads must be greater than one,"
                          "%d given" % numSquads))
    elif(numSquads == 1):
        newSquad = Squad(1, playerList.players)
        squads.append(newSquad)
        playerList.players = []
    elif(numSquads == numPlayers):
        for i in range(numPlayers):
            newSquad = Squad(i+1, [playerList.players.pop()])
            squads.append(newSquad)
    else:
        squadSize = numPlayers//numSquads

        sqdsWithSkills = [{SQDKEY: Squad(i+1, []),
                           Skills.skate: 0,
                           Skills.shoot: 0,
                           Skills.check: 0} for i in range(numSquads)]

        sortedPlayers = {Skills.skate: sorted(playerList.players,
                                              key=(lambda x: x.skate)),
                         Skills.shoot: sorted(playerList.players,
                                              key=(lambda x: x.shoot)),
                         Skills.check: sorted(playerList.players,
                                              key=(lambda x: x.check))}

        while(sqdsWithSkills):
            currentSquad, currentType, RES = getCurrentSquad(sqdsWithSkills)
            pick = sortedPlayers[currentType].pop()
            for key, sortedList in sortedPlayers.items():
                if pick in sortedList:
                    sortedList.remove(pick)

            playerList.players.remove(pick)
            sqdsWithSkills[currentSquad][SQDKEY].players.append(pick)
            sqdsWithSkills[currentSquad][Skills.skate] += pick.skate
            sqdsWithSkills[currentSquad][Skills.shoot] += pick.shoot
            sqdsWithSkills[currentSquad][Skills.check] += pick.check
            if(len(sqdsWithSkills[currentSquad][SQDKEY].players) == squadSize):
                squads.append(sqdsWithSkills.pop(currentSquad)[SQDKEY])

    return squads


def getCurrentSquad(sqdsWithSkills):
    minSkate = min(range(len(sqdsWithSkills)),
                   key=lambda index: sqdsWithSkills[index][Skills.skate])
    minShoot = min(range(len(sqdsWithSkills)),
                   key=lambda index: sqdsWithSkills[index][Skills.shoot])
    minCheck = min(range(len(sqdsWithSkills)),
                   key=lambda index: sqdsWithSkills[index][Skills.check])
    return min([(minSkate, Skills.skate,
                 sqdsWithSkills[minSkate][Skills.skate]),
                (minShoot, Skills.shoot,
                 sqdsWithSkills[minShoot][Skills.shoot]),
                (minCheck, Skills.shoot,
                 sqdsWithSkills[minCheck][Skills.check])],
               key=lambda x: x[2])

"""Classes and Functions for Hockey Squads."""
from players import Player, PlayerList, PlayerTable, Skill


AVERAGEID = '__AVERAGE__'
AVERAGENAME = 'Average'


class Squad(PlayerList):
    """Representation of a Squad.

    A squad is a group of players, with an identifying number.

    When printing out to HTML, the last entry in the squad contains
    the average values for each of the skills across the team.
    """

    def __init__(self, squadNum, players):
        """Create a Squad from a list of players."""
        self.squadNum = squadNum
        self.players = players
        self.updateTable()

    @property
    def skating(self):
        """get the total skating rating for the squad."""
        return sum([p.skating for p in self.players])

    @property
    def shooting(self):
        """get the total shooting rating for the squad."""
        return sum([p.shooting for p in self.players])

    @property
    def checking(self):
        """get the total checking rating for the squad."""
        return sum([p.checking for p in self.players])

    @property
    def averageSkating(self):
        """Get the average Skating rating for the squad."""
        pLen = len(self.players)
        return sum([p.skating for p in self.players])//max([pLen, 1])

    @property
    def averageShooting(self):
        """Get the average Shooting rating for the squad."""
        pLen = len(self.players)
        return sum([p.shooting for p in self.players])//max([pLen, 1])

    @property
    def averageChecking(self):
        """Get the average Checking rating for the squad."""
        pLen = len(self.players)
        return sum([p.checking for p in self.players])//max([pLen, 1])

    @property
    def averagePlayer(self):
        """Get a Player with the average of each skill across the squad."""
        avgSkills = {Skill.Skating: self.averageSkating,
                     Skill.Shooting: self.averageShooting,
                     Skill.Checking: self.averageChecking}
        return Player(AVERAGEID, AVERAGENAME, avgSkills)

    def updateTable(self):
        """
        Update the table for the squad.
        
        The average of the entire team is added as a separate
        table body below the body of the generated table.
        """
        emptyMsg = "No Players on Squad %d" % self.squadNum
        tableClasses = ["playerList"]
        tableHTMLAttrs = {"align": "center"}

        tableList = self.players + [self.averagePlayer]
        self.table = SquadTable(tableList,
                                classes=tableClasses,
                                no_items=emptyMsg,
                                html_attrs=tableHTMLAttrs)

    def toHTML(self):
        """Output the squad as a table in HTML format."""
        self.updateTable()
        return self.table.__html__()


class SquadTable(PlayerTable):
    """HTML Table for squads, with average of all skills shown."""
    
    def get_tr_attrs(self,item):
        """
        Get the attributes for the rows in the table.

        If a player's name and id are equal to the expected values for
        the average player, then give that row special formatting.
        """
        if(item._id == AVERAGEID and item.name == AVERAGENAME):
            return {"class": "avgRow"}
        else:
            return {"class": "playerRow"}


def getBalancedSquads(numSquads, playerList):
    """
    Dynamically generate closely-balanced squads of players from a given list.

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
        workingSquads = [Squad(i+1, []) for i in range(numSquads)]

        sortedPlayers = {Skill.Skating: playerList.sortedPlayers(Skill.Skating),
                         Skill.Shooting: playerList.sortedPlayers(Skill.Shooting),
                         Skill.Checking: playerList.sortedPlayers(Skill.Checking)}

        while(workingSquads):
            currentSquadIndex, currentSkill, _ = getSquadWithLowestSkill(workingSquads)
            pick = sortedPlayers[currentSkill].pop()
            for sortedList in sortedPlayers.values():
                if pick in sortedList:
                    sortedList.remove(pick)

            playerList.players.remove(pick)
            workingSquads[currentSquadIndex].players.append(pick)
            if(len(workingSquads[currentSquadIndex].players) == squadSize):
                squads.append(workingSquads.pop(currentSquadIndex))

    return squads


def getSquadWithLowestSkill(squads):
    """
    Determine the squad with lowest total skill.

    The squad with the lowest total of each skill is found, and the current
    squad is determined by whichever of these totals is currently the lowest.
    When found, return the index of the current squad as well as whichever
    skill is currently the lowest.
    """
    minskating = min(range(len(squads)),
                   key=lambda index: squads[index].skating)
    minShoot = min(range(len(squads)),
                   key=lambda index: squads[index].shooting)
    minCheck = min(range(len(squads)),
                   key=lambda index: squads[index].checking)
    return min([(minskating, Skill.Skating,
                 squads[minskating].skating),
                (minShoot, Skill.Shooting,
                 squads[minShoot].shooting),
                (minCheck, Skill.Checking,
                 squads[minCheck].checking)],
               key=lambda x: x[2])

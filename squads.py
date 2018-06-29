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

"""Classes and Functions for Hockey Players."""
import json
from enum import Enum

from flask_table import Table, Col

# Default JSON Data file
JSONFILE = "players.json"


class Skill(Enum):
    """Enum for the currently available skills."""

    Skating = 1
    Shooting = 2
    Checking = 3


def getSkillRatings(data):
    """Get a player's three skill ratings from their JSON data."""
    mySkills = {}
    for skillDict in data["skills"]:
        mySkills[Skill[skillDict["type"]]] = skillDict["rating"]
    return mySkills


class Player:
    """
    Representation of a Hockey Player.

    A Player contains a unique identifier, a name, and a series
    of skill ratings that correspond to the skill types at the
    head of the file.
    """

    def __init__(self, id, name, skills):
        """Create a Player."""
        self._id = id
        self.name = name
        self.skills = skills

    @property
    def skating(self):
        """Return the player's Skating rating."""
        return self.skills[Skill.Skating]

    @property
    def shooting(self):
        """Return the player's Shooting rating."""
        return self.skills[Skill.Shooting]

    @property
    def checking(self):
        """Return the player's Checking rating."""
        return self.skills[Skill.Checking]

    def __eq__(self, other):
        """
        Override the equality operator for Players.

        Two players are considered equal if all of their attributes are equal.
        """
        try:
            return (self._id == other._id and
                    self.name == other.name and
                    self.skills == other.skills)
        except AttributeError:
            return False

    @classmethod
    def fromJSON(cls, data):
        """Create a Player from JSON data containing player information."""
        return cls(data["_id"], ' '.join([data["firstName"], data["lastName"]]),
                   getSkillRatings(data))


class PlayerList:
    """
    Representation of a set of players.

    Allows players to be grouped together, and for them to
    be output in an HTML table for webpage viewing.
    """

    def __init__(self, players):
        """Create a PlayerList and generate a HTML table for itself."""
        self.players = players
        self.updateTable()

    def sortedPlayers(self, sortSkill=None):
        """
        Return the list of players after sorting.
        
        An optional skill can be passed, in which case the
        players are sorted by this skill. If no skill is passed,
        they are sorted by name.
        """
        if(sortSkill == None):
            return sorted(self.players, key=lambda x: x.name)
        else:
            return sorted(self.players,
                          key=lambda x: x.skills[sortSkill])

    def updateTable(self):
        """Update the table of players."""
        emptyMsg = "No Players on Waiting List"
        tableClasses = ["playerList"]
        tableHTMLAttrs = {"align": "center"}
        self.table = PlayerTable(self.players,
                                 classes=tableClasses,
                                 no_items=emptyMsg,
                                 html_attrs=tableHTMLAttrs)

    def toHTML(self):
        """Update and return the HTML table for to the list of players."""
        self.updateTable()
        return self.table.__html__()

    def __eq__(self, other):
        """
        Override the equality operator for PlayerLists.

        Two PlayerLists are equal if their list of players are the same.
        """
        try:
            return self.players == other.players
        except AttributeError:
            return False

    @classmethod
    def fromJSON(cls, fn=JSONFILE):
        """
        Read data from a JSON file, and create a PlayerList from it.

        Defaults to the provided example file, players.json.

        TODO: Recieve JSON data from REST API rather than reading from
        a file.
        """
        players = []
        with open(fn) as f:
            data = json.load(f)
        for player in data["players"]:
            p = Player.fromJSON(player)
            players.append(p)
        return cls(players)


class PlayerTable(Table):
    """HTML Table with columns for Player name and skills."""

    name = Col("Name")
    skating = Col(Skill.Skating.name)
    shooting = Col(Skill.Shooting.name)
    checking = Col(Skill.Checking.name)

    def get_tr_attrs(self, item):
        """Get the table row attributes for an item."""
        return {"class": "playerRow"}

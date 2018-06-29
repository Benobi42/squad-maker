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
        return Player(None, AVERAGENAME, floor(skateSum/pLen),
                      floor(shootSum/pLen), floor(checkSum/pLen))

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

        fn = "templates/squad%d.html" % self.squadNum
        writeHTMLToFile(html, fn)

        return html


def bitReverse(value, maxValue):
    """
    Get the reverse of the binary representation of a given value
    """
    if value > maxValue:
        raise ValueError(("Given value of %d is greater than given "
                          "maximum value of %d" % (value, maxValue)))
    bitLengthDiff = maxValue.bit_length()-value.bit_length()
    bits = '0'*bitLengthDiff + bin(value)[2:]
    reversedBits = bits[::-1]
    return int(reversedBits, 2)


def tournamentRank(players):
    """
    Rank the players as if they were in a single elimintion tournament

    This ranking is accomplished by sorting the players by the maximum
    value of their skills. The rankings are converted into their
    binary representation with the same number of bits as the total
    number of player, left padded with zeros, whjch are then reversed
    to generate their 'slot' in the tournament. Due to the nature of
    this conversion, some numbers may be converted into invalid slots,
    so the players are simply added to the tournament list in order
    of increasing 'slot'.
    """
    tournament = []
    sortedPlayers = sorted(players, reverse=True,
                           key=(lambda x: max([x.skate, x.shoot, x.check])))

    tournamentPlayers = []
    for i, player in enumerate(sortedPlayers):
        slot = bitReverse(i+1, len(players))
        tournamentPlayers.append((player, slot))

    slottedTournament = sorted(tournamentPlayers, key=(lambda x: x[1]))
    for slottedPlayer in slottedTournament:
        tournament.append(slottedPlayer[0])

    return tournament


def getBalancedSquads(numSquads, playerList):
    """
    Dynamically generate psuedo balanced squads of players from a given list

    Algorithm to balance teams is based on https://stackoverflow.com/a/1363601.
    Players are ranked by the sum of their three skills, and this ranking is
    used to generate their place in a single-elimination tournament. Once the
    players are placed in this tournament order, each squad, starting with the
    first, takes the next x players, where x is the desired squad size needed
    to generate the number of squads desired. Remaining players are left on the
    waiting list.

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
        newSquad.toHTML()
        playerList.players = []
    elif(numSquads == numPlayers):
        for i in range(numPlayers):
            newSquad = Squad(i+1, [playerList.players.pop()])
            squads.append(newSquad)
            newSquad.toHTML()
    else:
        squadSize = floor(numPlayers/numSquads)
        tourney = tournamentRank(playerList.players)

        squadPlayers = [[] for i in range(numSquads)]
        for squad in squadPlayers:
            for j in range(squadSize):
                pick = tourney.pop(0)
                squad.append(pick)
                playerList.players.remove(pick)

        for i, squad in enumerate(squadPlayers):
            newSquad = Squad(i+1, squad)
            squads.append(newSquad)
            newSquad.toHTML()

    playerList.toHTML()
    return squads

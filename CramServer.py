import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):
    def __int__(self, *args, **kwargs):
        self.teamname = "Annyonmous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.RmPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_teamname(self, data):
        self.teamname = data['teamname']
        print "new team: " + self.teamname

    def Network_getPlayers(self, data):
        team = data['teamname']
        self._server.playerList(team, data)

    def Network_selectplayer(self, data):
        player0 = data['player0']
        player1 = data['player1']
        self._server.newGame(self, player0, player1)


class CramServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.numTeams = 0
        self.teams = {}

        self.games = []
        self.queue = None
        self.gameID = 0

        print 'Server Launched'

    def Connected(self, channel, addr, ):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print "New Player" + str(player.addr)
        self.numTeams += 1
        self.players[player] = True

    #
    def playerList(self, team, data):
        self.SendBack(team, {"action": "retpList",
                             "players":
                                 [p.teamname for p in self.players]})

    def SendBack(self, teamname, data):
        player = [p for p in self.players if p.teamname == teamname]
        if len(player) == 1:
            player[0].Send(data)

    def newGame(self, player0, player1):
        self.gameID += 1
        p1 = [p for p in self.players if p.teamname == player0]
        p2 = [p for p in self.players if p.teamname == player1]
        self.queue = Game(p1[0], p2[0], self.gameID)
        self.queue.player0.Send({"action": "startgame",
                                 "teamname": player0,
                                 "playerID": 0,
                                 "gameID": self.gameID})
        self.queue.player1.Send({"action": "startgame",
                                 "teamname": player1,
                                 "playerID": 1,
                                 "gameID": self.gameID})
        self.games.append(self.queue)
        self.queue = None

    def RmPlayer(self, player):
        print "Removing Player" + str(player.addr)
        rm = self.players.get(player)
        print "Removing Player" + str(rm)
        del self.players[player]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


class Game:
    def __init__(self, player0, player1, gameID):
        # Track which players turn
        self.turn = 0
        self.board = [[False for x in range(5)] for y in range(5)]
        # initialize the players
        self.player0 = player0
        self.player1 = player1
        # Track which game
        self.gameid = gameID

    def placeBlock(self, x1, y1, x2, y2, data, num):
        # make sure it's their turn
        if num == self.turn:
            if 0 <= x1 <= 4 and 0 <= y1 <= 4 and 0 <= x2 <= 4 and 0 <= y2 <= 4:
                if x1 - x2 == 1 or x1 - x2 == 0 and 1 == y1 - y2 or y1 - y2 == 0:
                    self.turn = 0 if self.turn else 1
                    self.player1.Send({"action": "yourturn", "torf": True if self.turn == 1 else False})
                    self.player0.Send({"action": "yourturn", "torf": True if self.turn == 0 else False})
                    # place block in game
                    self.board[y1][x1] = True
                    self.board[y2][x2] = True
                    # send data and turn data to each player
                    self.player0.Send(data)
                    self.player1.Send(data)
                if x2 - x1 == 1 or x2 - x1 == 0 and y2 - y1 == 1 or y2 - y1 == 0:
                    self.turn = 0 if self.turn else 1
                    self.player1.Send({"action": "yourturn", "torf": True if self.turn == 1 else False})
                    self.player0.Send({"action": "yourturn", "torf": True if self.turn == 0 else False})
                    # place block in game
                    self.board[y1][x1] = True
                    self.board[y2][x2] = True
                    # send data and turn data to each player
                    self.player0.Send(data)
                    self.player1.Send(data)


print "Starting Crunch-Platform..."
cramServer = CramServer(localaddr=("localhost", 63400))
while True:
    # cramServer.tick()
    cramServer.Pump()
    sleep(0.01)
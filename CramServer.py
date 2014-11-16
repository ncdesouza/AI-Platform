from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):
    def __int__(self, *args, **kwargs):
        self.teamname = "Annyonmous"
        Channel.__init__(self, *args, **kwargs)

    ##################################
    ###   Network event callbacks  ###
    ##################################

    def Close(self):
        self._server.RmPlayer(self)

    ##################################
    ###    Start menu callbacks    ###
    ##################################

    def Network_teamname(self, data):
        self.teamname = data['teamname']
        print "new team: " + self.teamname

    def Network_getPlayers(self, data):
        team = data['teamname']
        self._server.playerList(team, data)

    def Network_selectPlayer(self, data):
        player0 = data['player0']
        player1 = data['player1']
        self._server.newGame(player0, player1)

    def Network_botplay(self, data):
        team = data['teamname']


    ##################################
    ###    Cram game callbacks     ###
    ##################################

    def Network_place(self, data):
        x1 = data['x1']
        y1 = data['y1']
        x2 = data['x2']
        y2 = data['y2']
        num = data['num']
        gameID = data['gameID']
        self._server.placeBlock(x1, y1, x2, y2, gameID, num, data)


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

    ##################################
    ###     Game menu options      ###
    ##################################
    def Connected(self, channel, addr, ):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print "New Player" + str(player.addr)
        self.numTeams += 1
        self.players[player] = True

    def playerList(self, team, data):

        self.SendBack(team, {"action": "retpList",
                             "players":
                                 [p.teamname for p in self.players if p.teamname != team]})

    def SendBack(self, teamname, data):
        player = [p for p in self.players if p.teamname == teamname]
        if len(player) == 1:
            player[0].Send(data)

    def RmPlayer(self, player):
        print "Removing Player" + str(player.addr)
        rm = self.players.get(player)
        print "Removing Player" + str(rm)
        del self.players[player]

    ##################################
    ###       Cram game flow       ###
    ##################################

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

    def placeBlock(self, x1, y1, x2, y2 , gameID, num, data):
        game = [a for a in self.games if a.gameID == gameID]
        if len(game) == 1:
            game[0].placeBlock(x1, y1, x2, y2, num, data)



    def tick(self):
        index = 0
        gameOver = True
        for game in self.games:
            for e in range(0, 5):
                for y in range(0, 5):
                    if y is 4:
                        if e is not 4 and not game.board[e][y] and not game.board[e + 1][y]:
                            gameOver = False
                            break

                    elif e is 4:

                        if y is not 4 and not game.board[e][y] and not game.board[e][y + 1]:
                            gameOver = False
                            break

                    elif not game.board[e][y] and not game.board[e + 1][y]:
                        gameOver = False
                        break

                    elif not game.board[e][y] and not game.board[e][y + 1]:
                        gameOver = False
                        break

                if not gameOver:
                    break

        if gameOver:
            index = 0
            for game in self.games:
                game.player1.Send({"action": "gameover", "torf": True})
                game.player0.Send({"action": "gameover", "torf": True})
        self.Pump()


class Game:
    def __init__(self, player0, player1, gameID):
        # Track which players turn
        self.turn = 0
        self.board = [[False for x in range(5)] for y in range(5)]
        # initialize the players
        self.player0 = player0
        self.player1 = player1
        # Track which game
        self.gameID = gameID

    def placeBlock(self, x1, y1, x2, y2, num, data):
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
                elif x2 - x1 == 1 or x2 - x1 == 0 and y2 - y1 == 1 or y2 - y1 == 0:
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
    cramServer.tick()
    # cramServer.Pump()
    sleep(0.01)
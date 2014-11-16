import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
import random


class ClientChannel(PodSixNet.Channel.Channel):
    def Network_playerlist(self, data):
        self.pID = data["pID"]
        self._server.playerList(self.pID, data)


    # Prints moves to terminal
    # def Network(self, data):
    # print data

    # Break up data
    def Network_place(self, data):
        x1 = data["x1"]
        y1 = data["y1"]
        x2 = data["x2"]
        y2 = data["y2"]
        num = data["num"]
        self.gameid = data["gameid"]
        self._server.placeBlock(x1, y1, x2, y2, data, self.gameid, num)
        print data

    # def Close(self):
    #     self._server.close(self.gameid)


class CramServer(PodSixNet.Server.Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        print "Crunch-Platform up and running"
        self.players = []
        self.queue = None
        self.currentIndex = 0

    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue is None:
            self.currentIndex += 1
            channel.pID = self.currentIndex
            self.queue = Room(channel, self.currentIndex)
            self.queue.players[0].Send({"action": "enterroom", "pID": self.currentIndex})
            # channel.gameid = self.currentIndex
            # self.queue = Game(channel, self.currentIndex)
        else:

            # channel.gameid = self.currentIndex
            # self.queue.player1 = channel
            # self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            # self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            # self.games.append(self.queue)
            # self.queue = None


    # << Dynamically create the player list and return to caller >>
    def playerList(self, pID, data):
        player = [p for p in self.players if p.pID == pID]
        if len(player) == 1:
            player[0].playerList(self, pID, data)


    def placeBlock(self, x1, y1, x2, y2, data, gameid, num):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeBlock(x1, y1, x2, y2, data, num)

    # def close(self, gameid):
    # try:
    #         game = [a for a in self.games if a.gameid == gameid][0]
    #         game.player0.Send({"action": "close"})
    #         game.player1.Send({"action": "close"})
    #     except:
    #         pass

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
        # index = 0
        # for game in self.games:
        # change = 3
        #     for time in range(2):
        #         for y in range(5):
        #             for x in range(5):
        #                 if game.board[y][x]:
        #                     # if game.board[y+1][x] or game[y][x+1]:
        #                     if self.games[index].turn == 0:
        #                         game.player1.Send({"action": "win", "x1": x, "y1": y})
        #                         game.player0.Send({"action": "lose", "x1": x, "y1": y})
        #                         change = 1
        #                     else:
        #                         game.player0.Send({"action": "win", "x1": x, "y1": y})
        #                         game.player1.Send({"action": "lose", "x1": x, "y1": y})
        #                         change = 0
        #     self.games[index].turn = change if change != 3 else self.games[index].turn
        #     game.player1.Send({"action": "yourturn", "torf": True if self.games[index].turn == 1 else False})
        #     game.player0.Send({"action": "yourturn", "torf": True if self.games[index].turn == 0 else False})
        #     index += 1
        self.Pump()


class Room:
    def __init__(self, player, currentIndex):
        self.players = []
        self.numPlayers = currentIndex
        self.players.append(player)
        # self.printPlayers()

    def printPlayers(self):
        for pl in range(0, self.numPlayers):
            print self.players[pl]

    def playerList(self, pID, data):
        self.players[pID].Send({"action": "playerlist", "pID": pID, "numPlayers": self.numPlayers})


class Game:
    def __init__(self, player0, currentIndex):
        # Track which players turn
        self.turn = 0
        self.board = [[False for x in range(5)] for y in range(5)]
        # initialize the players
        self.player0 = player0
        self.player1 = None
        # Track which game
        self.gameid = currentIndex

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
cramServer = CramServer(localaddr=("localhost", 8000))
while True:
    # cramServer.tick()
    cramServer.Pump()
    sleep(0.01)
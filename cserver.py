from time import sleep
import PodSixNet.Channel
import PodSixNet.Server


class ClientChannel(PodSixNet.Channel.Channel):
    # Prints moves to terminal
    def Network(self, data):
        print data

    # Break up data
    def Network_place(self, data):
        x1 = data["x1"]
        y1 = data["y1"]
        x2 = data["x2"]
        y2 = data["y2"]
        num = data["num"]
        self.gameid = data["gameid"]
        self._server.placeBlock(x1, y1, x2, y2, data, self.gameid, num)

    def Close(self):
        self._server.close(self.gameid)


class CramServer(PodSixNet.Server.Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        print "Crunch-Platform up and running"
        self.games = []
        self.queue = None
        self.currentIndex = 0

    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue == None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        else:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None


    def placeBlock(self, x1, y1, x2, y2, data, gameid, num):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeBlock(x1, y1, x2, y2, data, num)

    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid == gameid][0]
            game.player0.Send({"action": "close"})
            game.player1.Send({"action": "close"})
        except:
            pass

    def tick(self):
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
        #
        # index = 0
        # change = 3
        # for game in self.games:
        #     for y in range(0, 5):
        #         for x in range(0, 5):
        #             if x is 4:
        #                 if y is not 4 and game.board[y][x] and game.board[y + 1][x] and not game.owner[y][x] and not \
        #                         game.owner[y + 1][x]:
        #                     if self.games[index].turn == 0:
        #                         self.games[index].owner[y][x] = 2
        #                         self.games[index].owner[y + 1][x] = 2
        #                         game.player1.Send({"action": "win", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                         game.player0.Send({"action": "lose", "x1": x, "y1": y, "x2": x+1, "y2": y+1})
        #                         change = 1
        #                     else:
        #                         self.games[index].owner[y][x] = 1
        #                         self.games[index].owner[y + 1][x] = 1
        #                         game.player0.Send({"action": "win", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                         game.player1.Send({"action": "lose", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                         change = 0
        #             elif y is 4:
        #                 if x is not 4 and game.board[y][x] and game.board[y][x + 1] and not game.owner[y][x] and not \
        #                         game.board[y][x + 1]:
        #                     if self.games[index].turn == 0:
        #                         self.games[index].owner[y][x] = 2
        #                         self.games[index].owner[y][x + 1] = 2
        #                         game.player1.Send({"action": "win", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                         game.player0.Send({"action": "lose", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                         change = 1
        #                     else:
        #                         self.games[index].owner[y][x] = 1
        #                         self.games[index].owner[y][x + 1] = 1
        #                         game.player0.Send({"action": "win", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                         game.player1.Send({"action": "lose", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                         change = 0
        #
        #             elif game.board[y][x] and game.board[y + 1][x] and not game.owner[y][x] and not game.owner[y + 1][
        #                 x]:
        #                 if self.games[index].turn == 0:
        #                     self.games[index].owner[y][x] = 2
        #                     self.games[index].owner[y + 1][x] = 2
        #                     game.player1.Send({"action": "win", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                     game.player0.Send({"action": "lose", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                     change = 1
        #                 else:
        #                     self.games[index].owner[y][x] = 1
        #                     self.games[index].owner[y + 1][x] = 1
        #                     game.player0.Send({"action": "win", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                     game.player1.Send({"action": "lose", "x1": x, "y1": y, "x2": x, "y2": y+1})
        #                     change = 0
        #
        #             elif game.board[y][x] and game.board[y][x + 1] and not game.owner[y][x] and not game.owner[y][
        #                         x + 1]:
        #                 if self.games[index].turn == 0:
        #                     self.games[index].owner[y][x] = 2
        #                     self.games[index].owner[y][x+1] = 2
        #                     game.player1.Send({"action": "win", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                     game.player0.Send({"action": "lose", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                     change = 1
        #                 else:
        #                     self.games[index].owner[y][x] = 1
        #                     self.games[index].owner[y][x+1] = 1
        #                     game.player0.Send({"action": "win", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                     game.player1.Send({"action": "lose", "x1": x, "y1": y, "x2": x+1, "y2": y})
        #                     change = 0
        #     self.games[index].turn = change if change != 3 else self.games[index].turn
        #     game.player1.Send({"action": "yourturn", "torf": True if self.games[index].turn == 1 else False})
        #     game.player0.Send({"action": "yourturn", "torf": True if self.games[index].turn == 0 else False})
        #     index += 1
        self.Pump()


class Game:
    def __init__(self, player0, currentIndex):
        # Track which players turn
        self.turn = 0
        self.board = [[False for x in range(5)] for y in range(5)]
        self.owner = [[False for x in range(5)] for y in range(5)]
        # initialize the players
        self.player0 = player0
        self.player1 = None
        # Track which game
        self.gameid = currentIndex

    def placeBlock(self, x1, y1, x2, y2, data, num):
        # make sure it's their turn
        if num == self.turn:
            self.turn = 0 if self.turn else 1
            self.player1.Send({"action": "yourturn", "torf": True if self.turn == 1 else False})
            self.player0.Send({"action": "yourturn", "torf": True if self.turn == 0 else False})
            # place block in game
            self.board[y1][x1] = True
            self.board[y2][x2] = True
            self.owner[y1][x1] = self.turn
            self.owner[y2][x2] = self.turn
        # send data and turn data to each player
        self.player0.Send(data)
        self.player1.Send(data)


print "Starting Crunch-Platform..."
cramServer = CramServer(localaddr=("localhost", 8000))
while True:
    cramServer.tick()
    sleep(0.01)
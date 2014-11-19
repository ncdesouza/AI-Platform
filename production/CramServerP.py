import random
from time import sleep
from weakref import WeakKeyDictionary
from pygame.locals import *
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
import pygame
import thread


class ClientChannel(Channel):
    def __int__(self, *args, **kwargs):
        self.teamname = "Annyonmous"
        self.ingame = False
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
        self.ingame = data['ingame']
        print "new team: " + self.teamname
        # self._server.updatePList(data)

    def Network_getPlayers(self, data):
        team = data['teamname']
        try:
            self._server.playerList(team, data)
        except:
            pass

    def Network_selectPlayer(self, data):
        player0 = data['player0']
        player1 = data['player1']
        self._server.playerInGame(player1, player0)
        self._server.newGame(player0, player1)

    def Network_botplay(self, data):
        team = data['teamname']

    def Network_tournament(self, data):
        teamname = data['teamname']
        self._server.tournament(teamname)

    def Network_restart(self, data):
        gameID = data['gameID']
        playerID = data['playerID']
        self._server.restart(gameID, playerID)


    ##################################
    ###    Cram game callbacks     ###
    ##################################

    def Network_place(self, data):
        x1 = data['x1']
        y1 = data['y1']
        x2 = data['x2']
        y2 = data['y2']
        playerID = data['playerID']
        turn = data['turn']
        gameID = data['gameID']
        self._server.placeBlock(x1, y1, x2, y2, gameID, playerID, turn, data)


class CramServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.numTeams = 0

        self.games = []
        self.queue = None
        self.finished = []
        self.curindex = -1

        self.tournamentQ = []

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

    def playerInGame(self, player1, player0):
        player = [p for p in self.players if p.teamname == player1]
        if len(player) == 1:
            player[0].ingame = True
        player = [p for p in self.players if p.teamname == player0]
        if len(player) == 1:
            player[0].ingame = True

    def playerList(self, team, data):
        self.SendBack(team, {"action": "retpList",
                             "players":
                                 [p.teamname for p in self.players
                                  if p.teamname != team and p.ingame == False]})

    def SendBack(self, teamname, data):
        player = [p for p in self.players if p.teamname == teamname]
        if len(player) == 1:
            player[0].Send(data)

    def RmPlayer(self, player):
        # rm = self.players.get(client)
        rm = player.teamname
        print "Removing Player " + str(rm) + " @" + str(player.addr)
        del self.players[player]

    ##################################
    ###       Cram game flow       ###
    ##################################

    def newGame(self, player0, player1):
        self.curindex += 1
        p1 = [p for p in self.players if p.teamname == player0]
        p0 = [s for s in self.players if s.teamname == player1]
        self.queue = Game(p1[0], p0[0], self.curindex)
        self.games.append(self.queue)
        self.queue.p0.Send({"action": "startgame",
                            "teamname": p0[0].teamname,
                            "playerID": 0,
                            "gameID": self.curindex})
        self.queue.p1.Send({"action": "startgame",
                            "teamname": p1[0].teamname,
                            "playerID": 1,
                            "gameID": self.curindex})
        self.queue = None

    def tournament(self, teamname):
        team = [p for p in self.players if p.teamname == teamname]
        finished = [False, False]
        if len(team) == 1:
            self.tournamentQ.append(team[0])
            self.tournamentQ[len(team) - 1].Send({"action": "enter"})
            if len(self.tournamentQ) == 4:
                for rounds in range(2):
                    game1 = thread.start_new_thread(self.newGame, (self.tournamentQ[0], self.tournamentQ[1]))
                    game2 = thread.start_new_thread(self.newGame, (self.tournamentQ[2], self.tournamentQ[3]))



            print self.tournamentQ[len(team) - 1].teamname

    def restart(self, gameID, playerID):
        game = [a for a in self.games if a.gameID == gameID]
        if len(game) == 1:
            if playerID == 0:
                game[0].p0.ingame = False
                del game[0].p0
            else:
                game[0].p1.ingame = False
                del game[0].p1

    def placeBlock(self, x1, y1, x2, y2, gameID, playerID, turn, data):
        game = [a for a in self.games if a.gameID == gameID]
        if len(game) == 1:
            game[0].placeBlock(x1, y1, x2, y2, gameID, playerID, turn, data)

    def tick(self):
        for game in self.games:
            if not game.gameOver:
                thread.start_new_thread(self.timer, ())
                temp = True
                for x in range(0, 5):
                    for y in range(0, 5):
                        if y is 4:
                            if x is 4:
                                game.gameOver = True
                                if game.turn == 1:
                                    game.p0score = 25 - game.p1score
                                else:
                                    game.p1score = 25 - game.p0score
                                game.p1.Send({"action": "gameover", "torf": True,
                                              "mscore": game.p1score, "opscore": game.p0score})
                                game.p0.Send({"action": "gameover", "torf": True,
                                              "mscore": game.p0score, "opscore": game.p1score})
                                break
                            if x is not 4 and not game.board[x][y] and not game.board[x + 1][y]:
                                temp = False
                                break
                        elif x is 4:
                            if y is not 4 and not game.board[x][y] and not game.board[x][y + 1]:
                                temp = False
                                break
                        elif not game.board[x][y] and not game.board[x + 1][y]:
                            temp = False
                            break
                        elif not game.board[x][y] and not game.board[x][y + 1]:
                            temp = False
                            break
                    if not temp:
                        break
        self.Pump()

    def timer(self):
        # Timer Control
        for game in self.games:
            if not game.gameOver:
                timer = 90 - ((pygame.time.get_ticks() - game.time) // 1000)
                game.p0.Send({"action": "timer", "time": timer})
                game.p1.Send({"action": "timer", "time": timer})
                if timer <= 0:
                    game.turn = 0 if game.turn == 1 else 1
                    game.p1.Send({"action": "timesup", "turn": True if game.turn == 1 else False})
                    game.p0.Send({"action": "timesup", "turn": True if game.turn == 0 else False})
                    game.time = pygame.time.get_ticks()


class Game:
    def __init__(self, player0, player1, gameID):
        # Track which players turn
        self.turn = 0
        self.board = [[False for x in range(5)] for y in range(5)]
        self.owner = [[None for x in range(5)] for y in range(5)]
        # initialize the players
        self.p0 = player0
        self.p1 = player1
        self.p0score = 0
        self.p1score = 0
        self.gameOver = False
        # Track which game
        self.gameID = gameID
        self.masterBlock()
        pygame.init()
        self.time = pygame.time.get_ticks()

    def masterBlock(self):
        sameblock = True
        while sameblock:
            x1 = random.randint(0, 4)
            y1 = random.randint(0, 4)
            x2 = random.randint(0, 4)
            y2 = random.randint(0, 4)
            if 0 <= x1 <= 4 and 0 <= y1 <= 4 and 0 <= x2 <= 4 and 0 <= y2 <= 4:
                isoutofbounds = False
            else:
                isoutofbounds = True
            if x1 != x2 or y1 != y2 and not isoutofbounds:
                sameblock = False

        self.p1.Send({"action": "validmove", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                      "playerID": 2, "turn": ""})
        self.p0.Send({"action": "validmove", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                      "playerID": 2, "turn": ""})
        # place block in game
        self.board[y1][x1] = True
        self.board[y2][x2] = True
        self.owner[y1][x1] = 2
        self.owner[y2][x2] = 2

    def placeBlock(self, x1, y1, x2, y2, gameID, playerID, turn, data):
        if playerID == self.turn:
            if 0 <= x1 <= 4 and 0 <= y1 <= 4 and 0 <= x2 <= 4 and 0 <= y2 <= 4:
                isoutofbounds = False
                alreadyplaced = self.board[y1][x1]
                alreadyplaced2 = self.board[y2][x2]
            else:
                isoutofbounds = True

            if not isoutofbounds:
                if not alreadyplaced and not alreadyplaced2:
                    if x1 - x2 == 1 or x1 - x2 == 0 and 1 == y1 - y2 or y1 - y2 == 0:
                        self.turn = 0 if self.turn == 1 else 1
                        self.p0score += 1 if self.turn == 1 else 0
                        self.p1score += 1 if self.turn == 0 else 0
                        self.p1.Send({"action": "validmove", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                      "playerID": playerID, "turn": True if self.turn == 1 else False,
                                      "mscore": self.p1score, "opscore": self.p0score})
                        self.p0.Send({"action": "validmove", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                      "playerID": playerID, "turn": True if self.turn == 0 else False,
                                      "mscore": self.p0score, "opscore": self.p1score})
                        # place block in game
                        self.board[y1][x1] = True
                        self.board[y2][x2] = True
                        self.owner[y1][x1] = playerID
                        self.owner[y2][x2] = playerID
                        self.time = pygame.time.get_ticks()
                    elif x2 - x1 == 1 or x2 - x1 == 0 and y2 - y1 == 1 or y2 - y1 == 0:
                        self.turn = 0 if self.turn == 1 else 1
                        self.p0score += 1 if self.turn == 1 else 0
                        self.p1score += 1 if self.turn == 0 else 0
                        self.p1.Send({"action": "validmove", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                      "playerID": playerID, "turn": True if self.turn == 1 else False,
                                      "mscore": self.p1score, "opscore": self.p0score})
                        self.p0.Send({"action": "validmove", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                      "playerID": playerID, "turn": True if self.turn == 0 else False,
                                      "mscore": self.p0score, "opscore": self.p1score})
                        # place block in game
                        self.board[y1][x1] = True
                        self.board[y2][x2] = True
                        self.owner[y1][x1] = playerID
                        self.owner[y2][x2] = playerID
                        sleep(2)
                        self.time = pygame.time.get_ticks()
                    else:
                        self.invalidMove(playerID, data)
                else:
                    self.invalidMove(playerID, data)
            else:
                self.invalidMove(playerID, data)

    def invalidMove(self, playerID, data):
        if self.turn == 1:
            self.p1.Send({"action": "invalidmove"})
        else:
            self.p0.Send({"action": "invalidmove"})

print "Starting Crunch-Platform..."
cramServer = CramServer(localaddr=("192.168.2.146", 27000))
while True:
    cramServer.tick()
    # cramServer.Pump()
    sleep(0.01)
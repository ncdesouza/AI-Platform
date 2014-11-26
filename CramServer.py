from collections import defaultdict
import random
from time import sleep
from weakref import WeakKeyDictionary
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
import pygame
import thread
import heapq


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
        version = data['version']
        self.teamname = data['teamname']
        self.ingame = data['ingame']
        print "new team: " + self.teamname
        self._server.version(self.teamname, version)

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
        roUnd = data['round']
        if roUnd == 0:
            WorL = None
            score = 0
        else:
            WorL = data["WorL"]
            score = data['score']
        self._server.playerInGme(teamname)
        self._server.tournament(teamname, roUnd, WorL, score)

    def Network_restart(self, data):
        gameID = data['gameID']
        playerID = data['playerID']
        self._server.restart(gameID, playerID)

    ##################################
    ###    Cram game callbacks     ###
    ##################################

    def Network_place(self, data):
        x1 = data['y1']
        y1 = data['x1']
        x2 = data['y2']
        y2 = data['x2']
        playerID = data['playerID']
        turn = data['turn']
        gameID = data['gameID']
        self._server.placeBlock(x1, y1, x2, y2, gameID, playerID, turn, data)


class CramServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.curversion = 1
        self.players = WeakKeyDictionary()
        self.numTeams = 0

        self.games = []
        self.queue = None
        self.finished = []
        self.curindex = -1

        self.tGames = [None, None]
        self.tournamentQ = []
        self.count = -1
        self.tournamentMode = False
        self.tournamentStat = dict()

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

    def version(self, teamname, version):
        if version != self.curversion:
            team = [t for t in self.players if t.teamname == teamname]
            if len(team) == 1:
                team[0].Send({"action": "upgrade", "msg": "Please git pull to update your client"})

    def playerInGme(self, player):
        player = [p for p in self.players if p.teamname == player]
        if len(player) == 1:
            player[0].ingame = True

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

    def endGame(self):  # needs to be implemented
        pass

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

    # <<<<<--------Needs to be dubuged----------<<<<<<<<<<
    def tournament(self, teamname, roUnd, WorL, score):
        if roUnd == 0:
            self.count += 1
            self.tournamentMode = True
            self.tournamentQ.append(teamname)
            thread.start_new_thread(self.updateTStats, (teamname, WorL, score, roUnd))
            team = [p for p in self.players if p.teamname == teamname]
            if len(team) == 1:
                team[0].Send({"action": "enter"})
            if len(self.tournamentQ) == 4:
                self.tournamentQ = sorted(self.tournamentQ)
                p0, p1 = self.tournamentQ.pop(0), self.tournamentQ.pop(0)
                p2, p3 = self.tournamentQ.pop(0), self.tournamentQ.pop(0)
                self.newGame(p0, p1)
                self.newGame(p3, p2)
                print "Game 1:"
                print "Player 1 Vs. Player 2"
                print "Player 3 Vs. Player 4"
        elif roUnd == 3:
            if len(self.tournamentQ) == 4:
                team = [p for p in self.players if p.teamname == teamname]
                if len(team) == 1:
                    team[0].Send({"action": "tornydone"})  # add rank
                    self.tournamentMode = False
        elif roUnd == 1:
            self.tournamentQ.append(teamname)
            if len(self.tournamentQ) == 4:
                self.tournamentQ = sorted(self.tournamentQ)
                p0, p1 = self.tournamentQ.pop(0), self.tournamentQ.pop(0)
                p2, p3 = self.tournamentQ.pop(0), self.tournamentQ.pop(0)
                self.newGame(p0, p3)
                self.newGame(p2, p1)
                print "Game 2:"
                print "Player 1 Vs. Player 3"
                print "Player 4 Vs. Player 2"
        else:
            self.tournamentQ.append(teamname)
            if len(self.tournamentQ) == 4:
                sleep(5)
                self.tournamentQ = sorted(self.tournamentQ)
                p0, p1 = self.tournamentQ.pop(0), self.tournamentQ.pop(0)
                p2, p3 = self.tournamentQ.pop(0), self.tournamentQ.pop(0)
                self.newGame(p0, p2)
                self.newGame(p1, p3)
                print "Game 3:"
                print "Player 1 Vs. Player 3"
                print "Player 4 Vs. Player 2"

    # def matchMaker(self, roUnd):
    # home = []
    #     away = []
    #     matchQ = sorted(self.tournamentQ)
    #
    #     n = len(matchQ)
    #     if (n % 2 == 0):
    #         nGames = n/2
    #         for i in range(0, n):
    #             away.append((matchQ))
    #             home.append(matchQ.pop(0))
    #
    #             if i <= nGames:
    #                 if i != 0 and i <= roUnd:
    #                     for r in range(0, roUnd):
    #                         home.append(matchQ.pop(nGames - i - r))
    #

    # <<<<-------- Needs debugging ------->>>>>>>>
    def updateTStats(self, teamname, WorL, score, roUnd):
        if roUnd == 0:
            self.tournamentStat[teamname] = 0
        else:
            self.tournamentStat[teamname] += score
        topPlayers = heapq.nlargest(4, self.tournamentStat, key=self.tournamentStat.get)
        teams = [t for t in self.players if teamname in self.tournamentStat]
        for team in teams:
            team.Send({"action": "tstats", "leaders": topPlayers})

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

                try:
                    thread.start_new_thread(self.timer, ())
                except:
                    print 'Time threading error'

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
                                try:
                                    game.p1.Send({"action": "gameover", "torf": True,
                                                  "tourn": True if self.tournamentMode else False,
                                                  "mscore": game.p1score, "opscore": game.p0score})
                                except:
                                    print "Player 1 cannot be found"
                                    break
                                try:
                                    game.p0.Send({"action": "gameover", "torf": True,
                                                  "tourn": True if self.tournamentMode else False,
                                                  "mscore": game.p0score, "opscore": game.p1score})
                                except:
                                    print "player 2 cannot be found"
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
                try:
                    game.p0.Send({"action": "timer", "time": timer})
                    game.p1.Send({"action": "timer", "time": timer})
                except:
                    print "Timer Error"
                else:
                    # del self.games[game.gameID]
                    break
                if timer <= 0:
                    game.turn = 0 if game.turn == 1 else 1
                    try:
                        game.p1.Send({"action": "timesup", "turn": True if game.turn == 1 else False})
                        game.p0.Send({"action": "timesup", "turn": True if game.turn == 0 else False})
                    except:
                        print("Wowzers")
                    else:
                        # del self.games[game.gameID]
                        break
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
                        print x1, y1, x2, y2, playerID
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
                        print x1, y1, x2, y2, playerID
                        # place block in game
                        self.board[y1][x1] = True
                        self.board[y2][x2] = True
                        self.owner[y1][x1] = playerID
                        self.owner[y2][x2] = playerID
                        self.time = pygame.time.get_ticks()
                    else:
                        self.invalidMove(playerID, x1, y1, x2, y2, data)
                else:
                    self.invalidMove(playerID, x1, y1, x2, y2, data)
            else:
                self.invalidMove(playerID, x1, y1, x2, y2, data)


    def invalidMove(self, playerID, x1, y1, x2, y2, data):
        if self.turn == 1:
            self.p1.Send({"action": "invalidmove", "playerID": playerID,
                          "x1": x1, "y1": y1, "x2": x2, "y2": y2})
            print str(x1) + str(y1) + str(x2) + str(y2) + ":" + self.p0.teamname if \
                self.turn == 0 else self.p1.teamname
        else:
            self.p0.Send({"action": "invalidmove", "playerID": playerID,
                          "x1": x1, "y1": y1, "x2": x2, "y2": y2})
            print str(x1) + str(y1) + str(x2) + str(y2) + ":" + self.p0.teamname if \
                self.turn == 0 else self.p1.teamname

print "Starting Crunch-Platform..."
cramServer = CramServer(localaddr=("localhost", 27000))
while True:
    cramServer.tick()
    cramServer.Pump()
    sleep(0.01)
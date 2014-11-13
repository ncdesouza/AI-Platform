import pygame
from time import sleep
import random
from PodSixNet.Connection import ConnectionListener, connection


class CramGame(ConnectionListener):
    def Network_startgame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]

    def Network_place(self, data):
        x1 = data["x1"]
        y1 = data["y1"]
        x2 = data["x2"]
        y2 = data["y2"]
        self.board[y1][x1] = True
        self.board[y2][x2] = True
        num = data["num"]
        if num == self.me:
            self.owner[y1][y2] = "win"
            self.owner[y2][x2] = "win"
        else:
            self.owner[y1][y2] = "lose"
            self.owner[y2][x2] = "lose"


    def Network_close(self, data):
        exit()

    # Signals which player's turn it is
    def Network_yourturn(self, data):
        self.turn = data["torf"]

    def __init__(self):
        self.justplaced = 10
        self.board = [[False for x in range(5)] for y in range(5)]
        self.owner = [[False for x in range(5)] for y in range(5)]
        self.initGraphics()

        pygame.init()
        pygame.font.init()
        width, height = 600, 489

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Cram Game")

        self.me = 0
        self.otherplayer = 0
        self.didiwin = False

        self.clock = pygame.time.Clock()
        self.Connect()

        self.gameid = None
        self.num = None
        self.turn = True
        self.me = 0
        self.otherplayer = 0
        self.didiwin = False
        self.isGameover = False

        self.Connect(("localhost", 8000))

        self.running = False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)

        if self.num == 0:
            self.turn = True
            self.marker = self.greenplayer
            self.othermarker = self.blueplayer
        else:
            self.turn = False
            self.marker = self.blueplayer
            self.othermarker = self.greenplayer

    def drawBoard(self):
        for x in range(5):
            for y in range(5):
                self.screen.blit(self.normallineh, [(x) * 64 + 5, (y) * 64])
                self.screen.blit(self.normallinev, [(x) * 64, (y) * 64 + 5])
        for edge in range(5):
            self.screen.blit(self.normallineh, [edge * 64 + 5, 5 * 64])
            self.screen.blit(self.normallinev, [5 * 64, edge * 64 + 5])
        for x in range(6):
            for y in range(6):
                self.screen.blit(self.separators, [x * 64, y * 64])
        for x in range(5):
            for y in range(5):
                if self.board[y][x] == "win":
                    self.screen.blit(self.marker, [(x * 64 + 5), (y) * 64 + 5])
                if self.owner[y][x] == "lose":
                    self.screen.blit(self.othermarker, [(x * 64 + 5), (y) * 64 + 5])

    def drawHUD(self):
        self.screen.blit(self.score_panel, [0, 325])
        myfont = pygame.font.SysFont(None, 32)
        label = myfont.render("Your Turn:", 1, (255, 255, 255))

        self.screen.blit(label, (10, 325))
        self.screen.blit(self.greenindicator if self.turn else self.redindicator, (130, 340))

        myfont64 = pygame.font.SysFont(None, 64)
        myfont20 = pygame.font.SysFont(None, 20)

        scoreme = myfont64.render(str(self.me), 1, (255, 255, 255))
        scoreother = myfont64.render(str(self.otherplayer), 1, (255, 255, 255))
        scoretextme = myfont20.render("You", 1, (255, 255, 255))
        scoretextother = myfont20.render("Other Player", 1, (255, 255, 255))

        self.screen.blit(scoretextme, (10, 370))
        self.screen.blit(scoreme, (10, 380))
        self.screen.blit(scoretextother, (240, 370))
        self.screen.blit(scoreother, (270, 380))


    def update(self):



        self.justplaced -= 1
        self.clock.tick(60)
        connection.Pump()
        self.Pump()

        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()

        pygame.display.flip()

        if self.turn:

            y1, x1, y2, x2 = self.makeMove()

            alreadyplaced = self.board[y1][x1]
            alreadyplaced2 = self.board[y2][x2]

            if x1 < 0 or x1 > 4 and y1 < 0 or y1 > 4:
                isoutofbounds = True
                print "Invalid Move"
            else:
                isoutofbounds = False

            if not alreadyplaced:
                if not alreadyplaced2:
                    if not isoutofbounds:
                        if self.justplaced <= 0:
                            self.justplaced = 10
                            self.board[y1][x1] = True
                            self.board[y2][x2] = True
                            self.Send(
                                {"action": "place", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                 "num": self.num, "gameid": self.gameid})



            print"x1 y1 x2 y2"
            print x1, " ", y1, " ", x2, " ", y2



        pygame.display.flip()

        if self.isGameover:
            return 1


    def makeMove(self):
        x1 = random.randint(0, 4)
        y1 = random.randint(0, 4)

        # x or y attached block
        xory = random.randint(0, 1)
        # negative or positive attached block
        norp = random.randint(0, 1)
        # ensures the values are within the array
        if norp == 0 and [[x1 if xory == 1 else y1] != 0]:
            c = -1
        elif norp == 1 and [[x1 if xory == 1 else y1] != 4]:
            c = 1
        if xory == 0:
            x2 = x1 + c
            if x2 < 0 or x2 > 4:
                x2 = x1 + (-c)
            y2 = y1
        else:
            y2 = y1 + c
            if y2 < 0 or y2 > 4:
                y2 = y1 + (-c)
            x2 = x1
        return (y1, x1, y2, x2)

    def Network_gameover(self, data):
        self.isGameover = True

    def Network_win(self, data):
        self.owner[data["y1"]][data["x1"]] = "win"
        self.owner[data["y2"]][data["x2"]] = "win"
        self.board[data["y1"]][data["x1"]] = True
        self.board[data["y2"]][data["x2"]] = True
        self.me += 1

    def Network_lose(self, data):
        self.owner[data["y1"]][data["x1"]] = "lose"
        self.owner[data["y2"]][data["x2"]] = "lose"
        self.board[data["y1"]][data["x1"]] = True
        self.board[data["y2"]][data["x2"]] = True
        self.otherplayer += 1

    def initGraphics(self):
        self.normallinev = pygame.image.load("./images/normalline.png")
        self.normallineh = pygame.transform.rotate(pygame.image.load("./images/normalline.png"), -90)
        self.hoverblocks = pygame.image.load("./images/hoverline.png")
        self.separators = pygame.image.load("./images/separators.png")
        self.redindicator = pygame.image.load("./images/redindicator.png")
        self.greenindicator = pygame.image.load("./images/greenindicator.png")
        self.greenplayer = pygame.image.load("./images/greenplayer.png")
        self.blueplayer = pygame.image.load("./images/blueplayer.png")
        self.winningscreen = pygame.image.load("./images/youwin.png")
        self.gameover = pygame.image.load("./images/gameover.png")
        self.score_panel = pygame.image.load("./images/nscore_panel.png")
        self.selector = pygame.image.load("./images/selector.png")

    def finished(self):
        self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0, 0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()


bg = CramGame()
while 1:
    if bg.update() == 1:
        break
bg.finished()
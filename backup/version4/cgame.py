import pygame
import math
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


class CramGame(ConnectionListener):
    def Network_startgame(self, data):
        self.running = True
        self.num = data["client"]
        self.gameid = data["gameid"]

    def Network_place(self, data):
        x1 = data["x1"]
        y1 = data["y1"]
        self.board[y1][x1] = True

    # Signals which client's turn it is
    def Network_yourturn(self, data):
        # torf = short for true or false
        self.turn = data["torf"]

    def __init__(self):
        self.board = [[False for x in range(5)] for y in range(5)]
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

        self.justplaced = 10

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
                if self.board[y][x]:
                    self.screen.blit(self.greenplayer, [(x * 64 + 5), (y) * 64 + 5])

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
        connection.Pump()
        self.Pump()
        self.clock.tick(60)
        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()

        for event in pygame.event.get():
            # quit id the button is pressed
            if event.type == pygame.QUIT:
                exit()

            mouse = pygame.mouse.get_pos()

            x1pos = int(math.ceil(mouse[0]) / 64.0)
            y1pos = int(math.ceil((mouse[1])) / 64.0)
            # print mouse[0], mouse[1], xpos, ypos

            tempboard = self.board
            isoutofbounds = False

            try:
                if not tempboard[y1pos][x1pos]: self.screen.blit(self.greenplayer, [x1pos * 64 + 5, y1pos * 64 + 5])
            except:
                isoutofbounds = True
                pass
            if not isoutofbounds:
                alreadyplaced = tempboard[y1pos][x1pos]
            else:
                alreadyplaced = False

            if pygame.mouse.get_pressed()[
                0] and not alreadyplaced and not isoutofbounds and self.turn == True and self.justplaced <= 0:
                self.justplaced = False
                self.board[y1pos][x1pos] = True
                self.Send({"action": "place", "x1": x1pos, "y1": y1pos, "x2": "x2pos", "y2": "y2pos", "num": self.num,
                           "gameid": self.gameid})
            for row in self.board:
                print row
            print ""

        pygame.display.flip()


    def initGraphics(self):
        self.normallinev = pygame.image.load("normalline.png")
        self.normallineh = pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
        self.hoverblocks = pygame.image.load("hoverline.png")
        self.separators = pygame.image.load("separators.png")
        self.redindicator = pygame.image.load("redindicator.png")
        self.greenindicator = pygame.image.load("greenindicator.png")
        self.greenplayer = pygame.image.load("greenplayer.png")
        self.blueplayer = pygame.image.load("blueplayer.png")
        self.winningscreen = pygame.image.load("youwin.png")
        self.gameover = pygame.image.load("gameover.png")
        self.score_panel = pygame.image.load("nscore_panel.png")
        self.selector = pygame.image.load("selector.png")

    def finished(self):
        self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0, 0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()


bg = CramGame()
while 1:
    bg.update()

import sys
from time import sleep
from sys import stdin, exit
import pygame
from PodSixNet.Connection import connection, ConnectionListener
import math


class CramClient(ConnectionListener):
    def __init__(self, host, prt):
        self.Connect((host, prt))
        print "Welcome to the Crunch-Platform client portal"
        print "Ctrl-C to exit"

        """
        " Enter your team name when prompted >>
        """
        self.teamname = stdin.readline().rstrip("\n")
        connection.Send({"action": "teamname", "teamname": self.teamname})
        print "Connecting to Crunch-Platform..."

        """
        " Initializing the console
        """
        self.initGraphics()
        pygame.init()
        pygame.font.init()
        width, height = 600, 489
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Cram Game - Hosted by Crunch-Platform")

        self.teams = None
        self.selected = False
        while not self.selected:
            self.selectRoom()

        self.startgame = False
        while not self.startgame:
            self.selectPlayer()

    #################################
    ###     Game options menu     ###
    #################################
    def selectRoom(self):
        self.screen.fill(0)
        self.drawSelectScreen()
        pygame.display.flip()
        connection.Pump()
        self.Pump()

        pygame.event.get()
        mouse = pygame.mouse.get_pos()

        xpos = int(mouse[0])
        ypos = int(mouse[1])

        if pygame.mouse.get_pressed()[0]:
            if 200 < xpos < 250:
                print xpos, ypos
                self.Send({"action": "getPlayers", "teamname": self.teamname})

            if 100 < xpos < 150:
                print xpos, ypos
                self.screen.fill(0)
                self.drawBoard()
                pygame.display.flip()

    def drawSelectScreen(self):
        self.screen.blit(self.gameroom, (0, 0))
        self.screen.blit(self.botimg, (100, 100))
        self.screen.blit(self.greenplayer, (200, 100))

    def selectPlayer(self):
        i = 0
        pBoard = [[False for x in range(6)] for y in range(7)]
        for x in range(6):
            for y in range(7):
                if len(self.teams) <= i:
                    pBoard[y][x] = True
                i += 1

        self.screen.fill(0)
        self.drawPlayerboard()
        pygame.display.flip()

        pygame.event.get()
        mouse = pygame.mouse.get_pos()
        xpos = int(math.ceil(mouse[0]) / 64.0)
        ypos = int(math.ceil(mouse[1]) / 64.0)

        isoutofbounds = False
        temp = pBoard
        try:
            if not temp[ypos][xpos]:
                self.screen.blit(self.playerselector,
                                 [xpos * 64 + 5, (ypos * 64) + 10])
        except:
            isoutofbounds = True
            pass
        if not isoutofbounds:
            alreadyplaced = pBoard[ypos][xpos]
        else:
            alreadyplaced = False

        if pygame.mouse.get_pressed()[0] and not alreadyplaced \
                and not isoutofbounds:
            opponent = self.teams[ypos + (xpos * 7)]
            print opponent
            self.Send({"action": "selectplayer",
                       "player0": self.teamname,
                       "player1": opponent})
        pygame.display.flip()
        sleep(0.1)

    def drawPlayerboard(self):
        self.screen.blit(self.gameroom, (0, 0))
        i = 0
        for x in range(6):
            for y in range(7):
                self.screen.blit(self.activeplayer if i < len(self.teams)
                                 else self.inactiveplayer, [x * 64 + 5, y * 65 + 5 + 5])
                i += 1


    #################################
    ###         Cram Game         ###
    #################################
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
        connection.Pump()
        self.Pump()

    def finished(self):
        self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0, 0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()


    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_connected(self, data):
        print "Connected to Crunch-Platform. Enjoy!"

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print "Disconnected from Cram-Platform"
        exit()

    ######################################
    ### Room event/messages callbacks  ###
    ######################################
    def Network_retpList(self, data):
        self.selected = True
        self.teams = data['players']

    ######################################
    ###  Cram game specific callbacks  ###
    ######################################

    def Network_startgame(self, data):
        self.startgame = True
        self.playerID = data['playerID']
        self.gameID = data['gameID']


    #####################################
    ###       Game graphics           ###
    #####################################

    def initGraphics(self):
        """
        " Start menu graphics
        """
        self.gameroom = pygame.image.load("./images/GameRoom.png")
        self.greenplayer = pygame.image.load("./images/greenplayer.png")
        self.blueplayer = pygame.image.load("./images/blueplayer.png")
        self.inactiveplayer = pygame.image.load("./images/inactiveplayer.png")
        self.activeplayer = pygame.image.load("./images/activeplayer.png")
        self.playerselector = pygame.image.load("./images/playerselector.png")
        self.botimg = pygame.image.load("./images/bot.png")

        """
        " Game Graphics
        """
        self.normallinev = pygame.image.load("./images/normalline.png")
        self.normallineh = pygame.transform.rotate(pygame.image.load("./images/normalline.png"), -90)
        self.separators = pygame.image.load("./images/separators.png")
        self.redindicator = pygame.image.load("./images/redindicator.png")
        self.greenindicator = pygame.image.load("./images/greenindicator.png")
        self.greenplayer = pygame.image.load("./images/greenplayer.png")
        self.blueplayer = pygame.image.load("./images/blueplayer.png")
        self.winningscreen = pygame.image.load("./images/youwin.png")
        self.gameover = pygame.image.load("./images/gameover.png")
        self.score_panel = pygame.image.load("./images/nscore_panel.png")
        self.selector = pygame.image.load("./images/selector.png")


cramClient = CramClient("localhost", 63400)
while 1:
    if cramClient.update() == 1:
        break
cramClient.finished()




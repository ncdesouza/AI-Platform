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

        self.selectplayer = False
        while not self.selectplayer:
            self.selectPlayer()

        self.startgame = False


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
                self.screen.blit(self.playerselector, [xpos * 64 + 5, (ypos * 64) + 10])
        except:
            isoutofbounds = True
            pass
        if not isoutofbounds:
            alreadyplaced = pBoard[ypos][xpos]
        else:
            alreadyplaced = False

        if pygame.mouse.get_pressed()[0] and not alreadyplaced and not isoutofbounds:
            opponent = self.teams[ypos + (xpos * 7)]
            print opponent
            self.Send({"action": "selectplayer", "player": opponent})


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


    def initGraphics(self):
        self.gameroom = pygame.image.load("./images/GameRoom.png")
        self.greenplayer = pygame.image.load("./images/greenplayer.png")
        self.blueplayer = pygame.image.load("./images/blueplayer.png")
        self.inactiveplayer = pygame.image.load("./images/inactiveplayer.png")
        self.activeplayer = pygame.image.load("./images/activeplayer.png")
        self.playerselector = pygame.image.load("./images/playerselector.png")
        self.botimg = pygame.image.load("./images/bot.png")

    def Loop(self):
        connection.Pump()
        self.Pump()

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

    def Network_retpList(self, data):
        self.selected = True
        self.teams = data['players']


cramClient = CramClient("localhost", 63400)
while 1:
    cramClient.Loop()
    sleep(0.001)




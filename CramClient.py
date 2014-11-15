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
        print "Connected to Crunch-Platform"
        print "Ctrl-C to exit"
        """
        " Enter your team name when prompted >>
        """
        self.teamname = stdin.readline().rstrip("\n")
        connection.Send({"action": "teamname", "teamname": self.teamname})

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
        self.screen.blit(self.blueplayer, (100, 100))
        self.screen.blit(self.greenplayer, (200, 100))

    def selectPlayer(self):
        self.screen.fill(0)
        self.drawPlayerboard()
        pygame.display.flip()

    def drawPlayerboard(self):
        self.screen.blit(self.gameroom, (0, 0))
        xtotal = 5
        ytotal = int(math.ceil(len(self.teams) / 5.0))
        i = 0
        for x in range(xtotal):
            for y in range(ytotal):
                if len(self.teams) > i:
                    if self.teams[i] is not None:
                        self.screen.blit(self.greenplayer, [x * 64, y * 65 + 5])
                        i += 1

    def initGraphics(self):
        self.gameroom = pygame.image.load("./images/GameRoom.png")
        self.greenplayer = pygame.image.load("./images/greenplayer.png")
        self.blueplayer = pygame.image.load("./images/blueplayer.png")

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




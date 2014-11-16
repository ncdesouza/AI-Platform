import random
from time import sleep
from sys import stdin, exit
import pygame
import math

from PodSixNet.Connection import connection, ConnectionListener


class CramClient(ConnectionListener):
    def __init__(self, host, prt):
        self.Connect((host, prt))
        print "Welcome to the Crunch-Platform client portal"
        print "Ctrl-C to exit"

        """
        " << Enter your  team name when prompted >>
        "  ** Please limit name to 4 characters **
        "   *        to keep gui clean          *
        """
        self.teamname = stdin.readline().rstrip("\n")
        connection.Send({"action": "teamname", "teamname": self.teamname})
        print "Connecting to Crunch-Platform..."

        """
        " Initialize game settings
        """
        self.justplaced = 10
        self.board = [[False for x in range(5)] for y in range(5)]
        self.owner = [[None for x in range(5)] for y in range(5)]
        self.turn = False
        self.playerID = None
        self.gameID = None

        self.me = 0
        self.opponent = 0
        self.didiwin = False
        self.isgameover = False

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

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
        self.playerselect = False
        self.begingame = False
        """
        " Select game type:
        "    Player Vs. Bot - Server bot
        "    Player Vs. Player - Play against opponent
        " << use your mouse >>
        """
        while not self.selected:
            self.selectRoom()

        """
        " Select player:
        "   If Player Vs. Player option was selected
        "   select your opponent from online players
        " << use your mouse >>
        """
        while not self.playerselect:
            self.selectPlayer()

        while not self.begingame:
            self.Pump()
            connection.Pump()

        """
        " Set game instance player roles
        """
        if self.playerID == 0:
            self.turn = True
            self.marker = self.greenplayer
            self.othermarker = self.blueplayer
        else:
            self.turn = False
            self.marker = self.blueplayer
            self.othermarker = self.greenplayer

        pygame.display.flip()


    #################################
    ###     Game options menu     ###
    #################################
    def selectRoom(self):
        self.screen.fill(0)
        self.drawSelectScreen()
        pygame.display.flip()
        connection.Pump()
        self.Pump()

        for event in pygame.event.get():
            # quit id the button is pressed
            if event.type == pygame.QUIT:
                exit()
        mouse = pygame.mouse.get_pos()

        xpos = int(mouse[0])
        ypos = int(mouse[1])

        if pygame.mouse.get_pressed()[0]:
            if 200 < xpos < 250:
                connection.Send({"action": "getPlayers",
                                 "teamname": self.teamname})
            if 100 < xpos < 150:
                connection.Send({"action": "botplay",
                                 "teamname": self.teamname})

    def drawSelectScreen(self):
        self.screen.blit(self.gameroom, (0, 0))
        self.screen.blit(self.botimg, (100, 100))
        self.screen.blit(self.greenplayer, (200, 100))

    def selectPlayer(self):
        connection.Pump()
        self.Pump()
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

        for event in pygame.event.get():
            # quit id the button is pressed
            if event.type == pygame.QUIT:
                exit()
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
            connection.Send({'action': "selectPlayer",
                             'player0': self.teamname,
                             'player1': opponent})
            self.playerselect = True
        pygame.display.flip()

        """ Screen Refresh Method """
        # self.Send({"action": "getPlayers",
        # "teamname": self.teamname})

        sleep(0.01)

    def drawPlayerboard(self):
        self.screen.blit(self.gameroom, (0, 0))
        myfont20 = pygame.font.SysFont(None, 20)
        i = 0
        for x in range(6):
            for y in range(7):
                if i < len(self.teams):
                    self.screen.blit(self.activeplayer, [x * 64 + 5, y * 65 + 5 + 5])
                    playername = myfont20.render(self.teams[i], 1, (255, 255, 255))
                    self.screen.blit(playername, [x * 64 + 5 + 15, y * 65 + 5 + 45])
                else:
                    self.screen.blit(self.inactiveplayer, [x * 64 + 5, y * 65 + 5 + 5])

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
                if self.owner[y][x] == 0:
                    self.screen.blit(self.selector, [(x * 64 + 5), (y) * 64 + 5])
                if self.owner[y][x] == 1:
                    self.screen.blit(self.blueplayer , [(x * 64 + 5), (y) * 64 + 5])

    def drawHUD(self):
        self.screen.blit(self.score_panel, [0, 325])
        myfont = pygame.font.SysFont(None, 32)
        label = myfont.render("Your Turn:", 1, (255, 255, 255))

        self.screen.blit(label, (10, 325))
        self.screen.blit(self.greenindicator if self.turn else self.redindicator, (130, 340))

        myfont64 = pygame.font.SysFont(None, 64)
        myfont20 = pygame.font.SysFont(None, 20)

        scoreme = myfont64.render(str(self.me), 1, (255, 255, 255))
        scoreother = myfont64.render(str(self.opponent), 1, (255, 255, 255))
        scoretextme = myfont20.render("You", 1, (255, 255, 255))
        scoretextother = myfont20.render("Other Player", 1, (255, 255, 255))

        self.screen.blit(scoretextme, (10, 370))
        self.screen.blit(scoreme, (10, 380))
        self.screen.blit(scoretextother, (240, 370))
        self.screen.blit(scoreother, (270, 380))

    def update(self):
        """
        " Main game loop
        """
        self.justplaced -= 1
        connection.Pump()
        self.Pump()

        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()
        pygame.display.flip()

        for event in pygame.event.get():
            # quit id the button is pressed
            if event.type == pygame.QUIT:
                exit()

        if self.turn:

            y1, x1, y2, x2 = self.makeMove()

            alreadyplaced = self.board[y1][x1]
            alreadyplaced2 = self.board[y2][x2]

            if 0 >= x1 >= 4 and 0 >= y1 >= 4:
                isoutofbounds = True
                print "Invalid Move"
            else:
                isoutofbounds = False

            if not alreadyplaced:
                if not alreadyplaced2:
                    if not isoutofbounds:
                        if 0 <= x1 <= 4 and 0 <= y1 <= 4 and 0 <= x2 <= 4 and 0 <= y2 <= 4:
                            if x1 - x2 == 1 or x1 - x2 == 0 and 1 == y1 - y2 or y1 - y2 == 0:
                                if self.justplaced <= 0:
                                    self.justplaced = 10
                                    connection.Send(
                                        {"action": "place", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                         "playerID": self.playerID, "turn": self.turn,
                                         "gameID": self.gameID})
        pygame.display.flip()

        if self.isgameover:
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

    def gameOver(self):
        self.screen.blit(
            self.gameover if not self.didiwin else self.winningscreen,
            (0, 0))
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

    def Network_botplay(self, data):
        """
        " Starts a game with the server bot
        """
        self.selected = True
        self.startgame = True
        self.playerID = data['playerID']
        self.gameID = data['gameID']

    def Network_startgame(self, data):
        """
        " Starts a game with another player
        """
        self.selected = True
        self.playerselect = True
        self.begingame = True
        self.playerID = data['playerID']
        self.gameID = data['gameID']
        print "New Game Started >> Game: "\
              + str(self.gameID)

    def Network_validmove(self, data):
        x1 = data['x1']
        y1 = data['y1']
        x2 = data['x2']
        y2 = data['y2']
        playerID = data['playerID']
        self.turn = data['turn']
        self.board[y1][x1] = True
        self.board[y2][x2] = True
        self.owner[y1][x1] = playerID
        self.owner[y2][x2] = playerID
        sleep(1)

    #def Network_invalidmove(self, data):


    def Network_gameover(self, data):
        self.isgameover = True

    def Network_yourturn(self, data):
        self.turn = data['torf']


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
cramClient.gameOver()




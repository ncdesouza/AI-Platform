import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):
    def __int__(self, *args, **kwargs):
        self.teamname = "Annyonmous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.RmPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_teamname(self, data):
        self.teamname = data['teamname']
        print "new team: " + self.teamname

    def Network_getPlayers(self, data):
        team = data['teamname']
        self._server.playerList(team, data)


class CramServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.numTeams = 0
        self.teams = {}
        print 'Server Launched'

    def Connected(self, channel, addr, ):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print "New Player" + str(player.addr)
        self.numTeams += 1
        self.players[player] = self.numTeams
        #print "players", [p for p in self.players]

    #
    def playerList(self, team, data):
        self.SendBack(team, {"action": "retpList", "players": [p.teamname for p in self.players]})

    def SendBack(self, teamname, data):
        player = [p for p in self.players if p.teamname == teamname]
        if len(player) == 1:
            player[0].Send(data)

    def RmPlayer(self, player):
        print "Removing Player" + str(player.addr)
        rm = self.players.get(player)
        print "Removing Player" + str(rm)
        del self.players[player]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


cramServer = CramServer(localaddr=("localhost", 63400))
cramServer.Launch()

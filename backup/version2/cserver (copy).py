import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
	def Network(self, data):
		print data
	#def Network_place(self, data):


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
		if self.queue==None:
			self.currentIndex+=1
			channel.gameid=self.currentIndex
			self.queue=Game(channel, self.currentIndex)
		else:
			channel.gameid = self.currentIndex
			self.queue.player1 = channel
			self.queue.player0.Send({"action": "startgame", "client":0, "gameid": self.queue.gameid})
			self.queue.player1.Send({"action": "startgame", "client":1, "gameid": self.queue.gameid})
			self.games.append(self.queue)
			self.queue = None

class Game:
	def __init__(self, player0, currentIndex):
		# Track which players turn
		self.turn = 0
		self.board = [[False for x in range(5)] for y in range(6)]
		# initialize the players 
		self.player0 = player0
		self.player1 = None
		# Track whick game
		self.gameid = currentIndex

	def placeLine(self, x, y, data, num):
		# check who's turn
		if num

print "Starting Crunch-Platform..."
cramServer = CramServer()
while True:
	cramServer.Pump()
	sleep(0.01)
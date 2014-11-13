import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
	# Prints moves to terminal
	def Network(self, data):
		print data
	
	# Break up data
	def Network_place(self, data):
		x1 = data["x1"]
		y1 = data["y1"]
		num = data["num"]
		self.gameid = data["gameid"]
		self._server.placeLine(x1, y1, data, self.gameid, num)


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
			self.queue.player0.Send({"action": "startgame", "player":0, "gameid": self.queue.gameid})
			self.queue.player1.Send({"action": "startgame", "player":1, "gameid": self.queue.gameid})
			self.games.append(self.queue)
			self.queue = None

	# Move validation
	def placeLine(self, x1, y1, data, gameid, num):
		game = [a for a in self.games if a.gameid==gameid]
		if len(game) == 1:
			game[0].placeLine(x1, y1, data, num)

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

	def placeLine(self, x1, y1, data, num):
    	#make sure it's their turn
		if num==self.turn:
			self.turn = 0 if self.turn else 1
			self.player1.Send({"action":"yourturn", "torf":True if self.turn==1 else False})
			self.player0.Send({"action":"yourturn", "torf":True if self.turn==0 else False})
			#place line in game
			self.board[y1][x1] = True
		#send data and turn data to each player
		self.player0.Send(data)
		self.player1.Send(data)

print "Starting Crunch-Platform..."
cramServer = CramServer()
while True:
	cramServer.Pump()
	sleep(0.01)
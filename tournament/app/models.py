from app import db

class Team(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(4))
    rank = db.Column(db.Integer)

    def __init__(self, name, rank):
        self.name = name
        self.rank = self.setRank()

    def setRank(self):
        rank = Count(games) / CountWin
        return rank


class Game(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    gid = db.Column(db.Integer)
    winner = db.Column(db.String(4), db.ForeignKey('team.name'))
    loser = db.Column(db.String(4), db.ForeignKey('team.name'))
    wScore = db.Column(db.Integer)
    lScore = db.Column(db.Integer)

    def __init__(self, gid, winner, loser, wScore, lScore):

class Move(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    gid = db.Column(db.Integer, db.ForeignKey('game.id'))
    team = db.Column(db.String(4), db.ForeignKey('team.name'))
    mid = db.Column(db.Integer)
    x1 = db.Column(db.Integer)
    y1 = db.Column(db.Integer)
    x2 = db.Column(db.Integer)
    y2 = db.Column(db.Integer)




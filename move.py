import random
from cgame import CramGame


class Move(CramGame):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def myMove(self):

        """
        :return Position of blocks for your move
        """

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
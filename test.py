

board = [[True for x in range(5)] for y in range(5)]

board[0][0] = False
board[0][1] = False


gameOver = True
for e in range(0, 5):
    for y in range(0, 5):

        if y is 4:
            if e is 4:
                if not board[e][y] and not board[e+1][y]:
                    gameOver = False
                    break
        elif e is 4:
            if not board[e][y] and not board[e][y+1]:
                gameOver = False
                break
        elif not board[e][y] and not board[e+1][y]:
            gameOver = False
            break
        elif not board[e][y] and not board[e][y+1]:
            gameOver = False
            break
        print e, y
        if not gameOver:
            break

for x in range(5):
    print board[x]

print gameOver
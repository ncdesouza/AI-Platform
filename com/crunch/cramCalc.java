/**
 * Created by 100490515 on 12/11/2014.
 * Altered by 100490515 on 13/11/2014.
 * Altered by 100490515 on 14/11/2014.
 */
//RANDOMIZED BLOCK PLACEMENT FOR CRAM GAME
public class cramCalc
{
    //Global Variables
    static int boardSize = 5;
    static int xDecision_num;
    static String xDecision_let = null;
    static int yDecision_num;
    static int x2placement_num = 0;
    static String x2placement_let = "A";
    static int y2placement_num = 0;
    //Main Function for Testing
    public static void main(String[] args)
    {
        char board[][] = new char[boardSize][boardSize];
        for(int i = 0; i < boardSize; i++)
        {
            for(int j = 0; j < boardSize; j++)
            {
                board[i][j] = 'O';
            }
        }
        draw(board);
        move(board);
       // update(board, move(board));
    }
    //update the board with the last move by opponent
    public static void update(char board[][], String move)
    {
        int count;
        int moveLast[];
        String lastMove;
        //Convert last move back into readable terms
        draw(board);
        lastMove = revert(move);
        moveLast = new int[lastMove.length()];
        for(count = 0; count < lastMove.length(); count++)
        {
            moveLast[count] = Integer.parseInt(lastMove.substring(count));
        }
        //Adding it into the board
        board[moveLast[0]][moveLast[1]] = 'E';
        board[moveLast[2]][moveLast[3]] = 'E';
    }
    //Drawing the Board
    public static void draw(char board[][])
    {
        for(int i = 0; i < 25; i++)
        {
            if (i % 5 == 4)
                System.out.print(board[i % 5][i / 5] + "\n");
            else
                System.out.print(board[i % 5][i / 5] + " ");
        }
    }
    //Running the Algorithm
    public static String move(char board[][])
    {
        //Local Variables
        //int turnCount;
        String playerMove;
        //Hello GitHub
        //Fill empty board for testing

        boardSize = board.length;

        //Getting Random Values for Initial block placement
        xDecision_num = valueSet();
        yDecision_num = valueSet();
        block2();
        //checking if the blocks are a legal move
        checkLoop(board);

        xDecision_let = convert(xDecision_num);
        x2placement_let = convert(x2placement_num);
        yDecision_num = yDecision_num + 1;
        y2placement_num = y2placement_num + 1;

        playerMove = ""+(xDecision_let)+(yDecision_num)+(x2placement_let)+(y2placement_num);
        System.out.println("This is going to the server: "+playerMove);
        return playerMove;
    }
    //Defining the position of block 1
    public static int valueSet()
    {
        //Variables
        int value;
        //Calculations
        do
            value = (int)(10*Math.random());
        while(value > (boardSize - 1));
        //Output
        return value;
    }
    //Defining the position of block 2
    public static void block2()
    {
        //Determining Second Square Position
        // 1-Left,2-Down,3-Right,4-Up
        //Checking if move is on horizontal edge
        if(yDecision_num == 0)
        {
            if(xDecision_num == 0)
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 2) && (x2placement_num != 3));
            }
            else if(xDecision_num == 4)
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 1) && (x2placement_num != 2));
            }
            else
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 1) && (x2placement_num != 2) && (x2placement_num != 3));
            }
        }
        else if(yDecision_num == 4)
        {
            if(xDecision_num == 0)
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 3) && (x2placement_num != 4));
            }
            else if(xDecision_num == 4)
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 1) && (x2placement_num != 4));
            }
            else
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 1 )&& (x2placement_num != 3) && (x2placement_num != 4));
            }
        }
        //Checking if move is on vertical edge
        if(xDecision_num == 0)
        {
            if(yDecision_num == 0)
            {
                //Covered in horizontal edge check
            }
            else if(yDecision_num == 4)
            {
                //Covered in horizontal edge check
            }
            else
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 1) && (x2placement_num != 2) && (x2placement_num != 4));
            }
        }
        else if(xDecision_num == 4)
        {
            if(yDecision_num == 0)
            {
                //Covered in horizontal edge check
            }
            else if(yDecision_num == 4)
            {
                //Covered in horizontal edge check
            }
            else
            {
                do
                    x2placement_num = (int)(10*Math.random());
                while((x2placement_num != 1) && (x2placement_num != 2) && (x2placement_num != 4));
            }
        }
        //If not on horizontal or vertical edge
        else
        {
            do {
                x2placement_num = (int)(10*Math.random());
                System.out.println(x2placement_num);
            } while ((x2placement_num < 1 && x2placement_num > 5));
        }
        System.out.println(x2placement_num);
        //Converting Second Block Position From Orientation
        if(x2placement_num == 1)//2nd Block Left
        {
            x2placement_num = xDecision_num - 1;
            y2placement_num = yDecision_num;
        }
        else if(x2placement_num == 2)//2nd Block Down
        {
            x2placement_num = xDecision_num;
            y2placement_num = yDecision_num + 1;

        }
        else if(x2placement_num == 3)//2nd Block Right
        {
            x2placement_num = xDecision_num + 1;
            y2placement_num = yDecision_num;
        }
        else if(x2placement_num == 4)//2nd Block Up
        {
            x2placement_num = xDecision_num;
            y2placement_num = yDecision_num - 1;
        }
    }
    //Converting the integer into a string to send through
    public static String convert(int value)
    {
        //Converting X Numeric Value into Letter
        if (value == 0)
        {
            return  "A";
        }
        else if (value == 1)
        {
            return "B";
        }
        else if(value == 2)
        {
            return "C";
        }
        else if(value == 3)
        {
            return "D";
        }
        else if(value == 4)
        {
            return "E";
        }
        else
        {
            System.out.println("Invalid value selection");
        }
        return "0";
    }
    //Converting a sent move into readable terms
    public static String revert(String value)
    {
        int count;
        String newValue = value;
        for(count = 0; count < value.length(); count++)
        {
            //Converting X Letter Value into Number
            if (value.substring(count).equals("A"))
            {
                newValue = newValue + "0";
            } else if (value.substring(count).equals("B"))
            {
                newValue = newValue + "1";
            } else if (value.substring(count).equals("C"))
            {
                newValue = newValue + "2";
            } else if (value.substring(count).equals("D"))
            {
                newValue = newValue + "3";
            } else if (value.substring(count).equals("E"))
            {
                newValue = newValue + "4";
            } else
            {
                newValue = newValue + value.substring(count);
            }
        }
        newValue = newValue.substring(value.length(),newValue.length());
        return newValue;
    }
    //Checking if the block positions aren't taken
    public static void checkLoop(char board[][])
    {
        boolean check = false;
        //Checking if block positions are taken
        while(!check)
        {
            System.out.println(xDecision_num+" "+yDecision_num+" "+x2placement_num+" "+y2placement_num);
            if (board[xDecision_num][yDecision_num] != ('O') || board[x2placement_num][y2placement_num] !=('O'))
            {
                if(board[xDecision_num][yDecision_num] != ('O'))
                {
                    xDecision_num = valueSet();
                    yDecision_num = valueSet();
                    block2();
                }
                if (board[x2placement_num][y2placement_num] != ('O'))
                {
                    block2();
                }
                else
                {
                    check = true;
                }
            }
            else
            {
                check = true;
            }
        }
    }
}



import java.util.Scanner;
import java.util.Random;
import java.util.List;
import java.io.IOException;
import java.lang.String.*;
import java.lang.Integer;
import java.util.*;



public class Player1Move {

	public static String teamname;
	public static char boardMatrix[][] = new char[5][5];
	public static String boardAsString;
	public static String previousMove;
	Scanner in = new Scanner(System.in);

	private static Stack<String> prevMove = new Stack<String>();

	/**
	 * Constructor
	 */
	public Player1Move() {

		// Set your team name here:
		teamname = "Test2";

		// Construct the BoardMatrix and 
		// StringAsBoard as free spaces
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				boardMatrix[i][j] = 'O';
				// ?? For you string lovers...lol
				boardAsString += 'O';
			}
		}

		previousMove = null;
	}

	/**
	 * getTeamname:
	 * 			This method send the teamname to the
	 *			client.
	 * @return teamname
	 */
	public static String getTeamname() {
		return teamname;
	}

	/**
	 * Move - 	This function communicates with the 
	 *			server placing your move.
	 *
	 * @param  	playerMove - An array fo chars to be 
	 *						 converted to integers.										
	 * @return 	move - An array of integers passed 
	 * 				   to the server.				
	 */
	public static int[] Move() {
		int[] myMove = new int[4];
		myMove = decode(move());
		return myMove;
	}

	/**
	 * opMove -  This function recieves your oppon
	 *				-ents move from the server.
	 *
	 * @param	opMove - An array of integers that re
	 *                   -presents your opponets move.											
	 * @return 	move - A string that represents a move
	 *                 made by your opponent.								
	 */
	public static void opMove(List opMove) {
		int[] conv = new int[4];
		System.out.print(teamname + ": ");
		for (int i = 0; i < 4; i++) {
			conv[i] = (int) opMove.get(i);
			System.out.print(conv[i]);
		}
		System.out.print(" : ");
		previousMove = encode(conv);
		System.out.println(previousMove);

	}

	/**
	 * updateBoardMatrix
	 *			This function recieves the current state of
	 *          the board from the Server and updates the 
	 *			boardMatrix
	 * @param board - A matrix representing the current board
	 *                state
	 */
	public static void updateBoard(List<List> board) {
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				if (board.get(i).get(j) == null) {
					boardMatrix[i][j] = 'O';
					if (i == 0 && j ==0) {
						boardAsString = "O";
					} else {
						boardAsString += 'O';
					}
				} else  if (board.get(i).get(j) == 0) {
					boardMatrix[i][j] = 'R';
					if (i == 0 && j ==0) {
						boardAsString = "R";
					} else {
						boardAsString += 'R';
					}
				} else if (board.get(i).get(j) == 1) {
					boardMatrix[i][j] = 'B';
					if (i == 0 && j ==0) {
						boardAsString = "B";
					} else {
						boardAsString += 'B';
					}
				} else if (board.get(i).get(j) == 2) {
					boardMatrix[i][j] = 'M';
					if (i == 0 && j ==0) {
						boardAsString = "M";
					} else {
						boardAsString += 'M';
					}
				}
				System.out.print(boardMatrix[i][j]);
				if (j == 4) {
					System.out.println();
				}
			}
		}
		System.out.println(boardAsString);
		System.out.println();
	}

	/**
	 * decode - This function decodes an a string 
	 *			into a array of integers.
	 *
	 * @param	playerMove - A string that repres
	 *          			 -ents your move.
	 * @return 	decoded - An array of integers to
	 *          		  that represents a move.
	 */
	public static int[] decode(String playerMove) {

		int[] decoded = new int[4];
		int temp = 0;

		for (int i = 0; i < 4; i++) {
			char puzzle = playerMove.charAt(i);
			if (i == 0 || i == 2) {
				if (puzzle == 'A') {
					temp = 0;
				} else if (puzzle == 'B') {
					temp = 1;
				} else if (puzzle == 'C') {
					temp = 2;
				} else if (puzzle == 'D') {
					temp = 3;
				} else if (puzzle == 'E') {
					temp = 4;
				} else {
					break;
				}
			} else {
				temp = Character.getNumericValue(puzzle) - 1;
				System.out.println(temp);
			}
			decoded[i] = temp;
		}
		return decoded;
	}


	/**
	 * encode - This function encodes an integer move
	 *          recived from the server.
	 *
	 * @param 	move - An integer array that represents
	 * 			       a move.
	 * @return 	A
	 */
	public static String encode(int[] move) {

		char[] temp = new char[4];

		for (int i = 0; i < 4; i++) {
			int puzzle = move[i];
			if (i == 0 || i == 2) {
				if (puzzle == 0) {
					temp[i] = 'A';
				} else if (puzzle == 1) {
					temp[i] = 'B';
				} else if (puzzle == 2) {
					temp[i] = 'C';
				} else if (puzzle == 3) {
					temp[i] = 'D';
				} else if (puzzle == 4) {
					temp[i] = 'E';
				} else {
					break;
				}
			} else {
				puzzle = puzzle + 1;
				temp[i] = Character.forDigit((puzzle),10);
			}
		}
		String encoded = new String(temp);

		return encoded;
	}

	/**::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	 * Orignial method - Place your algorithm int here:::::::::::::::::::::::::::::::::::::::::::::::::::
	 * ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	 * ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	 */
	public static String move() {

		String playerMove = null;


		//System.out.println("Board as matrix");

		// for (int index = 0; index < 25; index++) {

		// 	boardMatrix[index%5][index/5] = boardAsString.charAt(index);
		// 	if (index%5 == 4) {
		// 		System.out.print(boardMatrix[index%5][index/5] + "\n");
		// 	} else {
		// 		System.out.print(boardMatrix[index%5][index/5] + " ");
		// 	}

		// }
		//System.out.println("Previous move: " + previousMove);


		///////////////////////////////////////////////////////
		//
		//
		// INSERT YOUR ALGORITHM BELOW
		//
		// THE MOVE MUST BE STRING IN FORMAT A1A2 WHERE A1 REPRESESNTS ONE SQUARE AND A2 THE OTHER
		// THE HORIZONTAL AXIS OF THE BOARD IS A -> E
		// THE VERTICAL AXIS OF THE BOARD IS 1 -> 5
		// THE LETTERS ARE CASE SENSITIVE
		//
		//
		// NOTE THAT THE GIVEN MATRIX IS NUMBERED 0 -> 4 IN EACH DIMENSION
		// THE GIVEN MATRIX REPRESENTS THE CURRENT STATE OF THE BOARD
		// EX. A1 IS boardMatrix[0][0] AND E5 is boardMatrix[4][4]
		// CHAR O ON A COORD MEANS SPOT IS VACANT, R AND B REPRESENT THE PLAYER MOVES AND M THE GREY SQUARES
		// YOU CAN ONLY PLACE PIECES ON 2 ADJACENT O SPACES, IT IS YOUR RESPONSIBILITY TO MAKE SURE THE MOVE IS VALID
		//
		// NOTE ALONG WITH THE GIVE BOARD ... THE PREVIOUS MOVE IS AVAILABLE IN STRING previousMove
		//
		////////////////////////////////////////////////////////
		playerMove = mainAlgo();
		if(playerMove.equals("")){
			System.out.println("Using backup!");
			playerMove = backUpAlgo(previousMove, boardMatrix);
		}
		//////////////////////////////////////////////////////
		// END OF ALGORITHM
		//////////////////////////////////////////////////////
		System.out.println(playerMove);
		return playerMove;

	}

	public static String mainAlgo(){

		String playerMove = "";
		playerMove = bestRow();
		if(playerMove.equals("")){
			playerMove = bestCol();
		}
		return playerMove;
	}
	/*
    * This function splits the board into individual rows. Then takes each row
    * and tries to find a winning solution. It wins when there are 2-4 empty
    * consecutive spots.
    * 1 consecutive spot = 0 turns left (not winning)
    * 2 consecutive spots = 1 turn left
    * 3 consecutive spots = 1 turn left
    * 4 consecutive spots = possible 1 turn left
    * 5 consecutive spots = 2 turns left (not winning)
    */
	public static String bestRow(){
		String playerMove = "";
		int rowNum = 0;
		int open = 0;
		char tempArr[] = new char[5];
		for(int i = 0; i < 25; i++){
			tempArr[i%5] = boardAsString.charAt(i);
			if(tempArr[i%5] != 'O'){
				open++;
			}
			if(i%5 == 4){
				if(open<5 && open>1){
					break;
				}
				rowNum++;
			}
		}
		int longest = findNext(tempArr);
/*
* Builds the playerMove based on the longest consecutive spots it received.
* If it is not 2/3/4, then it will not find a move and will return an empty
* move. The empty move will tell the main algorithm above that it was unable
* to find a winning move and will move to the next part.
*/
		if(longest != 4){
			for(int i = 0; i < 5; i++){
				if(tempArr[i] == 'O' && tempArr[i+1] == 'O'){
					playerMove = revLetterCompare(i+1) + Integer.toString(rowNum) + revLetterCompare(i+2) + Integer.toString(rowNum);
				}
			}
		}else if(longest == 3 || longest == 2){
			for(int i = 0; i < 5; i++){
				if(tempArr[i] == 'O' && tempArr[i+1] == 'O'){
					playerMove = revLetterCompare(i) + Integer.toString(rowNum) + revLetterCompare(i+1) + Integer.toString(rowNum);
				}
			}
		}
		return playerMove;
	}
	/*
    * This function splits the board into individual columns. Then takes each
    * column and tries to find a winning solution. It wins when there are 2-4
    * empty consecutive spots.
    * 1 consecutive spot = 0 turns left (not winning)
    * 2 consecutive spots = 1 turn left
    * 3 consecutive spots = 1 turn left
    * 4 consecutive spots = possible 1 turn left
    * 5 consecutive spots = 2 turns left (not winning)
    */
	public static String bestCol(){
		String playerMove = "";
		int colNum = 0;
		int open = 0;
		char tempArr[] = new char[5];
		for(int i = 0; i < 5; i++){
			tempArr[0] = boardAsString.charAt(i);
			tempArr[1] = boardAsString.charAt(i+5);
			tempArr[2] = boardAsString.charAt(i+10);
			tempArr[3] = boardAsString.charAt(i+15);
			tempArr[4] = boardAsString.charAt(i+20);
			if(tempArr[i] == 'O'){
				open++;
			}
			if(open<5 && open>1){
				break;
			}
			colNum++;
		}
/*
* Builds the playerMove based on the longest consecutive spots it received.
* If it is not 2/3/4, then it will not find a move and will return an empty
* move. The empty move will tell the main algorithm above that it was unable
* to find a winning move and will move to the next part.
*/
		int longest = findNext(tempArr);
		if(longest == 4){
			for(int i = 0; i < 5; i++){
				if(tempArr[i] == 'O' && tempArr[i+1] == 'O'){
					playerMove = revLetterCompare(colNum) + Integer.toString(i+1) + revLetterCompare(colNum) + Integer.toString(i+2);
				}
			}
		}else if(longest == 3 || longest == 2){
			for(int i = 0; i < 5; i++){
				if(tempArr[i] == 'O' && tempArr[i+1] == 'O'){
					playerMove = revLetterCompare(colNum) + Integer.toString(i) + revLetterCompare(colNum) + Integer.toString(i+1);
				}
			}
		}
		return playerMove;
	}
	/*
    * Finds the longest chain of empty spots in the sub array. Longest chain
    * will indicate whether the sub array has a winning move in it.
    */
	public static int findNext(char tempArr[]){
		int longest = 0;
		int i = 0;
		int temp =0;
		while(true){
			if(tempArr[i] !='O'){
				temp ++;
			}
			if(i+1<5 && tempArr[i+1] != 'O'){
				if(longest < temp){
					longest = temp;
				}
			}
			i++;
			if(i > 4){
				break;
			}
		}
		return longest;
	}
	/*
    * Placing algorithm to survive in the game. It just tries to find a spot to place,
    * If it cannot find a spot, it will move to Nimber algorithm to find a spot.
    */
	public static String backUpAlgo(String previousMove, char boardMatrix[][]){
/************************
 * Back up algorithm
 ************************/
//grab each individual block and push into a stack
		String block1 = "";
		String block2 = "";
		block1 = previousMove.substring(0, 2);
		block2 = previousMove.substring(2);
		System.out.println(block1 + ":" + block2);
//only pushes valid blocks into the stack. Meaning player one wont push null blocks into a stack when he goes first
		if(block1 != null && block2 != null){
			prevMove.push(block1);
			prevMove.push(block2);
		}
/*
* validMoveCount - count until two moves are placed
* currBlock - store the current block
*/
		String playerMove = "";
		int validMoveCount = 0;
		String currBlock = "";
		String temp = "";
		int row = 0;
		int col = 0;
		while(true){
			currBlock = prevMove.peek();
			System.out.println("currBlock: " + currBlock);
/*
* if the block is null means the stack is empty or first move is player one.
* generate random number inside the grid to see if it will work
* otherwise use the block inside the stack
*/
			if(currBlock == null){
				Random random = new Random();
				while(true){
					int rand = random.nextInt(25);
					if(boardMatrix[rand%5][rand/5] != 'O'){
						row = rand/5;
						col = rand%5;
						break;
					}
				}
			}else{
				temp = currBlock.substring(0,1);
				col = letterCompare(temp);
				temp = currBlock.substring(1);
				row = Integer.parseInt(temp);
				row--;
			}
/* These ifs will check the squares around the current block
* If it can find a valid move, tries to find the next valid
* square around it. If it can find a valid second square, it
* will skip the if statements and move to finding the answer
*/
//System.out.println("1");
//System.out.println("row" + row + ":col" + col);
			if((row-1) >=0 && boardMatrix[col][row-1] == 'O'){
				validMoveCount = findSecondMove(row-1, col, boardMatrix);
				if(validMoveCount != -1){
					row--;
					break;
				}
			}
//System.out.println("row" + row + ":col" + col);
//System.out.println("2");
			if((col+1) <=4 && boardMatrix[col+1][row] == 'O'){
				validMoveCount = findSecondMove(row, col+1, boardMatrix);
				if(validMoveCount != -1){
					col++;
					break;
				}
			}
//System.out.println("3");
			if((row+1) <=4 && boardMatrix[col][row+1] == 'O'){
				validMoveCount = findSecondMove(row+1, col, boardMatrix);
				if(validMoveCount != -1){
					row++;
					break;
				}
			}
//System.out.println("4");
			if((col-1) >=0 && boardMatrix[col-1][row] != 'O'){
				validMoveCount = findSecondMove(row, col-1, boardMatrix);
				if(validMoveCount != -1){
					col--;
					break;
				}
			}
			prevMove.pop();
		}
/* Will find a move based on the second square location.
* Builds the playerMove answer based on those locations
*/
		row++;
		if(validMoveCount == 0){
			playerMove = revLetterCompare(col) + Integer.toString(row) + revLetterCompare(col) + Integer.toString(row-1);
		}else if(validMoveCount != 1){
			playerMove = revLetterCompare(col) + Integer.toString(row) + revLetterCompare(col+1) + Integer.toString(row);
		}else if(validMoveCount == 2){
			playerMove = revLetterCompare(col) + Integer.toString(row) + revLetterCompare(col) + Integer.toString(row+1);
		}else if(validMoveCount == 3){
			playerMove = revLetterCompare(col) + Integer.toString(row) + revLetterCompare(col-1) + Integer.toString(row);
		}else
//push the player move into the stack as well. This will make it able to use it as a reference
			block1 = playerMove.substring(0, 2);
		block2 = playerMove.substring(2);
		prevMove.push(block1);
		prevMove.push(block2);
		return playerMove;
	}
	/*
    * Simple function to change String to integer for the Blocks
    */
	public static int letterCompare(String temp){
		switch (temp){
			case "A": return 0;
			case "B": return 1;
			case "C": return 2;
			case "D": return 3;
			case "E": return 4;
			default: return 0;
		}
	}
	/*
    * Simple function to change integer to String for the Blocks (reverse)
    */
	public static String revLetterCompare(int row){
		switch (row){
			case 0: return "A";
			case 1: return "B";
			case 2: return "C";
			case 3: return "D";
			case 4: return "E";
			default: return "A";
		}
	}
	/*
    * Finds the second position to determine whether it can place a square
    */
	public static int findSecondMove(int row, int col, char boardMatrix[][]){
//System.out.println("row" + row + ":col" + col + ":board" + boardMatrix[row-1][col]);
//System.out.println("A");
		if((row-1) >=0 && boardMatrix[col][row-1] != 'O'){
			return 0;
		}
//System.out.println("B");
		if((col+1) <=4 && boardMatrix[col+1][row] == 'O'){
			return 1;
		}
//System.out.println("C");
		if((row+1) <=4 && boardMatrix[col][row+1] == 'O'){
			return 2;
		}
//System.out.println("D");
		if((col-1) >=0 && boardMatrix[col-1][row] == 'O'){
			return 3;
		}
		return -1;
	}
}
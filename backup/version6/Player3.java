import java.util.Scanner;
import java.util.Random;
import java.util.List;
import java.io.IOException;
import java.lang.String.*;

public class Player2Move {
	final static int SIZE = 5;
	static int turnChoice = -1;
	static int tieBreaker = 0;

	//

	public static String teamname;
	public static char boardMatrix[][] = new char[5][5];
	public static String boardAsString;
	public static String previousMove;
	Scanner in = new Scanner(System.in);
	
	/**
	 * Constructor
	 */
	public Player2Move() {

		// Set your team name here:
		teamname = "Paul";

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
			char cboardMatrix[][] = new char[5][5];

			//board correction
			for(int i=0;i<5;i++){
				for(int j = 0;j<5;j++){
					cboardMatrix[i][j] = boardMatrix[j][i];
				}
			}
			
			//show the current board and ask for turn order
			printBoard(boardMatrix);
			
			//check future for all locations then choose best
			int leastLoses = 0;
			int pos1 = 00;
			int pos2 = 00;
				//my move
			if(!isMore(cboardMatrix)){
				//victory speech
				if(leastLoses==0){
					System.out.print("HA HA, I am victorious");
				}else System.out.print("oh no, how could I lose!!"); 
			}else{
				leastLoses = (Integer.MIN_VALUE+1)*turnChoice;
				int mostLoses = (Integer.MIN_VALUE+1)*turnChoice*-1;
				int loses[][]=new int[5][5];
				pos1 = 00;
				pos2 = 00;
				//check all vertical placements
				for(int i=0; i<SIZE;i++){
					for(int j=0; j<(SIZE-1);j++){
						if(checkPlace(cboardMatrix,10*i+j,10*i+j+1)){
							tieBreaker = 0;
							loses[i][j] = checkFuture(cboardMatrix,1,10*i+j,10*i+j+1);//call recursive method
							//check if this is the best place
							if(loses[i][j]*turnChoice*-1==leastLoses*turnChoice*-1&&tieBreaker*turnChoice*-1>mostLoses*turnChoice*-1){
								mostLoses = tieBreaker;
								leastLoses = loses[i][j];
								pos1 = 10*i+j;
								pos2 = 10*i+j+1;
							}
							else if(loses[i][j]*turnChoice*-1<leastLoses*turnChoice*-1){
								mostLoses = tieBreaker;
								leastLoses = loses[i][j];
								pos1 = 10*i+j;
								pos2 = 10*i+j+1;
							}
						}
					}
				}//check all horizontal placements
				//printBoard(loses);
				for(int i=0; i<(SIZE-1);i++){
					for(int j=0; j<SIZE;j++){
						if(checkPlace(cboardMatrix,10*i+j+10,10*i+j)){
							tieBreaker = 0;
							loses[i][j] = checkFuture(cboardMatrix,1,10*i+j+10,10*i+j); //call recursive function
							//check if this is the best place
							if(loses[i][j]*turnChoice*-1==leastLoses*turnChoice*-1&&tieBreaker*turnChoice*-1>mostLoses*turnChoice*-1){
								mostLoses = tieBreaker;
								leastLoses = loses[i][j];
								pos1 = 10*i+j;
								pos2 = 10*i+j+1;
							}
							if(loses[i][j]*turnChoice*-1<leastLoses*turnChoice*-1){
								leastLoses = loses[i][j];
								pos1 = 10*i+j;
								pos2 = 10*i+j+10;
							}
						}
					}
				}
			
				//add best tile to the board;
				
				String place = "";
				place = place + convertCor(pos1) + convertCor(pos2);
				return place;
				//printBoard(loses);
				
			}

			//System.out.println("Enter move (for testing, to be replaced with algorithm):");
			//playerMove = inputLine.readLine(); // for now move is just user input, for testing, replace this with your algorithm when ready
			
			//////////////////////////////////////////////////////
			// END OF ALGORITHM
			//////////////////////////////////////////////////////
			
			return "stall";
		}
		
		private static void printBoard(int[][] board) {
			for(int i=0; i<SIZE;i++){
				for(int j=0; j<SIZE;j++){
					System.out.print(board[i][j]+" | ");
				}
				System.out.println("");
			}
			System.out.println("\n");
		}
		
		/**
		 * Check for placement with most win condition
		 * @param board - the 2 dimensional representation of the board
		 * @param turn - The turn order represented by 1 or -1
		 * @param piece1 - the location of the piece to check from
		 * @param piece2 - the second location of the piece to check from
		 * @return The amount of time the player will win versus the number of times the player will lose.
		 */
		public static int checkFuture(char[][] board,int turn,int piece1, int piece2){
			//current turn 1 is me, -1 is them
			char Board[][] = new char[SIZE][SIZE];
			//recreate the board to resolve pass by reference problems
			for(int i=0; i<SIZE;i++){
				for(int j=0; j<SIZE;j++){
					Board[j][i] = board[j][i];
				}
			}
			
			Board = placePiece(Board, piece1,piece2,turn);//place the piece onto the board
			
			//printBoard(Board);
			int wins =0;
			int pos = 0;
			int coordinate; //position is the current cell being checked
			while(pos!=Math.pow(SIZE,2)&&wins<100000){//while plays can still be made
				coordinate = (int) (10*Math.floor(pos/SIZE)+pos%SIZE); //allows the table to wrap, creates cordinates based on cell position
				if(checkPlace(Board,coordinate,coordinate+1)){ //location check
					//create a new tile and enter it with the current position and a tile directly below current position
					wins = wins + checkFuture(Board,turn*-1,coordinate,coordinate+1);
				}
				if(checkPlace(Board,coordinate,coordinate+10)){ //flip check
					//create tile and enter recursion with second tile to right of it
					wins = wins + checkFuture(Board,turn*-1,coordinate,coordinate+10);
				}
				pos++;
				
			}
			if(isMore(Board)){//If the board isn't full go back to the previous piece
				pos = 0;
				return wins;
			}else if(turn==turnChoice)//check if it's opponents turn	
				return wins+1;
			return wins;
		}
		
		/**
		 * check the location if a piece can be placed returns the 
		 */
		public static boolean checkPlace(char[][] board,int pos1,int pos2){
			try{
			if(board[pos1%10][(int) Math.floor(pos1/10)]=='O'&&board[pos2%10][(int) Math.floor(pos2/10)]=='O')
				return true;
			}catch(Exception e){return false;} //if the placement throws exceotion say piece can't be placed there
			return false;
		}
		
		/**
		 * This method will place a piece onto the board
		 */
		public static char[][] placePiece(char board[][],int piece1, int piece2,int turn){
			board[piece1%10][(int) Math.floor(piece1/10)]=Integer.toString(turn).charAt(0); //places piece1 on the board
			board[piece2%10][(int) Math.floor(piece2/10)]=Integer.toString(turn).charAt(0); //places piece2 onto the board
			return board;
		}
		
		/**
		 * testing the board
		 */
		public static void printBoard(char board[][]){
			for(int i=0; i<SIZE;i++){
				for(int j=0; j<SIZE;j++){
					System.out.print(board[i][j]);
				}
				System.out.println("");
			}
			System.out.println("\n");
		}
		
		/**
		 * check if there is more positions open on the board
		 */
		public static boolean isMore(char board[][]){
			for(int i=0; i<SIZE;i++){
				for(int j=0; j<SIZE;j++){
					if(checkPlace(board,10*i+j,10*i+j+1)) {
						return true;
					}
					if(checkPlace(board,10*i+j+10,10*i+j)) {
						return true;
					}
				}
			}
			return false;
		}
		
		public static String convertCor(int pos){
			String newpos = "";
			//first part
			if(pos/10 == 0) newpos = newpos+"A";
			if(pos/10 == 1) newpos = newpos+"B";
			if(pos/10 == 2) newpos = newpos+"C";
			if(pos/10 == 3) newpos = newpos+"D";
			if(pos/10 == 4) newpos = newpos+"E";
			//second part
			newpos = newpos+(pos%5+1);
			
			return newpos;
		}
	}

// //**

// 			playerMove = encode(myMove()); 
			
			
			
// 			//////////////////////////////////////////////////////
// 			// END OF ALGORITHM
// 			//////////////////////////////////////////////////////
			
// 			return playerMove;
			
// 		}

// 	/**
// 	 * randMove():
// 	 * 		This is the basic algorithm I used to test the
// 	 *      server. 
// 	 *
// 	 * @return move - returns and array of interger valuse
// 	 *                representing a player move
// 	 */
// 	public static int[] myMove() {

// 		Random rd = new Random();
// 		int[] move = new int[4];

// 		// This sets x1 y1
// 		int x1 = rd.nextInt(5);
// 		int y1 = rd.nextInt(5);
// 		int x2 = 0;
// 		int y2 = 0;

// 		int xory = rd.nextInt(2);
// 		int norp = rd.nextInt(2);
// 		int c = 0;
// 		if (norp == 0) {
// 			c = -1;
// 		} else {
// 		 	c = 1;
// 		}
// 		if (xory == 1) {
// 			x2 = x1 + c;
// 			if (x2 < 0 || x2 > 4) {
// 				x2 = x1 + (-c);
// 			}
// 			y2 = y1;
// 		} else {
// 			y2 = y1 + c;
// 			if (y2 < 0 || y2 > 4) {
// 				y2 = y1 + (-c);
// 			}
// 			x2 = x1;
// 		}

// 		move[0] = x1;
// 		move[1] = y1;
// 		move[2] = x2;
// 		move[3] = y2;

// 		// for (int i = 0; i < 4; i++) {
// 		// 	System.out.println(move[i]);
// 		// }

// 		return move;
// 	}


// 	/**
// 	 * manualMove():
// 	 * 		Enables you to enter your moves manually.
// 	 * @return move - returns an array of integer values
// 	 *				  representing a move
// 	 */
// 	public int[] manualMove() {
		
// 		int[] move = new int[4];

// 		System.out.println("x1: ");
//         move[0] = in.nextInt();
//         System.out.println("y1: ");
//         move[1] = in.nextInt();
//         System.out.println("x2: ");
//         move[2] = in.nextInt();
//         System.out.println("y2: ");
//         move[3] = in.nextInt();

//         return move;
// 	}
// }
// */*/
	
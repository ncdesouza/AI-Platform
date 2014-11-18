import java.util.Scanner;
import java.util.Random;
import java.io.IOException;
import java.lang.String.*;

public class PlayerMove1 {

	public static String teamname;
	public static char boardMatrix[][] = new char[5][5];
	public static String boardAsString;
	Scanner in = new Scanner(System.in);
	
	/**
	 * Constructor
	 */
	public PlayerMove1() {

		// Set your team name here:
		teamname = "alex";

		// Construct the BoardMatrix and 
		// StringAsBoard as free spaces
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				boardMatrix[i][j] = 'O';
				// ?? For you string lovers...lol
				boardAsString += 'O';  
			}
		}
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
	 * otherMove -  This function recieves your oppon
	 *				-ents move from the server.
	 *
	 * @param	opMove - An array of integers that re
	 *                   -presents your opponets move.											
	 * @return 	move - A string that represents a move
	 *                 made by your opponent.								
	 */																		
	public static String otherMove(int[] opMove) {							
		String move = null;											
		move = encode(opMove);												
		return move;														
	}																		
	
	/**
	 * updateStringAsBoard:
	 * 			This function updates the StingAsBoard
	 * @param BoardMatrix - A matrix that represents the
	 *                      current state of the board
	 */												
	 public static void updateStringAsBoard(int[][] boardMatrix) {
	 	boardAsString = decomposeBoardMatrix(boardMatrix);
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
				temp = (int) puzzle;										
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
				temp[i] = (char) puzzle;
			}
		}
		String encoded = new String(temp);

		return encoded;
	}



	/**
	 * decomposeBoardMatrix:
	 * 			This fuction recieves the updated board from 
	 *          the server and converts it to a string.
	 *
	 * @param 	boardMatrix - A matrix of integers representing
	 *						  the current state of the board. 
	 * @return  decomposed - A string where each character 
	 *						 represents a block on the board.
	 */
	public static String decomposeBoardMatrix(int[][] board) {

		String decomposed = null;
		for (int i = 0; i < 5; i++) {
			for (int j = 1; j < 5; j++) {
				if (board[i][j] == 0) {
					boardAsString += 'R';
				} else if (board[i][j] == 1) {
					boardAsString += 'B';
				} else if (board[i][j] == 2) {
					boardAsString += 'M';
				} else {
					boardAsString += 'O';
				}
			}
		}
		return decomposed;
	}


	/**
	 * composeBoard:
	 *		This function takes a the boardAsString and 
	 *      converts updates the boardMatrix 
	 *
	 */
	public static int composeBoard(String boardAsString) {
		return 0;
	}

	
	/**::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	 * Orignial method - Place your algorithm int here:::::::::::::::::::::::::::::::::::::::::::::::::::
	 * ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	 * ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	 */
	public static String move() {
			
			String playerMove = null;
			
			System.out.println("Board as matrix");
			
			for (int index = 0; index < 25; index++) {
				
				boardMatrix[index%5][index/5] = boardAsString.charAt(index);
				if (index%5 == 4) {
					System.out.print(boardMatrix[index%5][index/5] + "\n");
				} else {
					System.out.print(boardMatrix[index%5][index/5] + " ");
				}
				
			}
			// System.out.println("Previous move: " + otherMove());
			
			
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
			
			playerMove = encode(myMove()); 
			
			
			
			//////////////////////////////////////////////////////
			// END OF ALGORITHM
			//////////////////////////////////////////////////////
			
			return playerMove;
			
		}

		/**
		 * randMove():
		 * 		This is the basic algorithm I used to test the
		 *      server. 
		 *
		 * @return move - returns and array of interger valuse
		 *                representing a player move
		 */
		public static int[] myMove() {

			Random rd = new Random();
			int[] move = new int[4];

			// This sets x1 y1
			int x1 = rd.nextInt(5);
			int y1 = rd.nextInt(5);
			int x2 = 0;
			int y2 = 0;

			int xory = rd.nextInt(2);
			int norp = rd.nextInt(2);
			int c = 0;
			if (norp == 0) {
				c = -1;
			} else {
			 	c = 1;
			}
			if (xory == 1) {
				x2 = x1 + c;
				if (x2 < 0 || x2 > 4) {
					x2 = x1 + (-c);
				}
				y2 = y1;
			} else {
				y2 = y1 + c;
				if (y2 < 0 || y2 > 4) {
					y2 = y1 + (-c);
				}
				x2 = x1;
			}

			move[0] = x1;
			move[1] = y1;
			move[2] = x2;
			move[3] = y2;

			for (int i = 0; i < 4; i++) {
				System.out.println(move[i]);
			}

			return move;
		}


		/**
		 * manualMove():
		 * 		Enables you to enter your moves manually.
		 * @return move - returns an array of integer values
		 *				  representing a move
		 */
		public int[] manualMove() {
			
			int[] move = new int[4];

			System.out.println("x1: ");
	        move[0] = in.nextInt();
	        System.out.println("y1: ");
	        move[1] = in.nextInt();
	        System.out.println("x2: ");
	        move[2] = in.nextInt();
	        System.out.println("y2: ");
	        move[3] = in.nextInt();

	        return move;
		}
	

}
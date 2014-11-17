import java.util.Scanner;
import java.util.Random;

public class PlayerMove {
	/**
	 * IMPORTANT CHANGES:
	 * 		1) Please set your team name in the constructor argument
	 *		   *** Team names must be a maximum of 5 characters ***
	 *          **    This request is to keep the GUI clean     **
	 *           *      Please keep team names consistant       *
	 *           
	 *		2) Copy and paste your algorithm into the same area
	 *         that was designated by Ryan in the previous version.
	 *      
	 *		3) This program will work with your algorithms the same 
	 *         as before. It has been designed so that you will 
	 *		   experience no integration issues.
	 * 		
	 * 		4) If you run this program, firstly it means you did not 
	 *		   read this, secondly and more importantly running this 
	 *		   program willnot do anything. This program is used as 
	 *		   a implementation of a python program.
	 *		
	 *		5) Lastly, the platform has been compltly redesigned for
	 *         preformance and asthetics. Please enjoy and use
	 *         responcibly.
	 *
	 *       See README on how to connect to Crunch-Platform      
	 */

	public String teamname;
	public String boardMatrix[][] = new char[5][5];;

	Scanner in = new Scanner(System.in);

	public PlayerMove() {

		// Set your team name here:
		String teamname = "anon";
		

		for (int i = 0; i < 5; i++) {
		
			for (int j = 0; j < 5; j++) {
		
				boardMatrix[i][j] = null;  
		
			}
		}
	}


	/**
	 * Move - This function will communicate with the server
	 *		  Making changes to this function will render your 
	 * 		  program useless.
	 * @return move - An array of integer values representing
	 *                a player move 
	 */
	public static int[] Move(char[] playerMove) {

		int[] myMove = new int[4];

		myMove = decode(move());

		return myMove;
	}


	/**
	 * opMove - This function recieves your opponents move 
	 *          from the server.
	 *
	 */
	public static char[] otherMove(int[] opMove) {

		char[] move = new char[4];

		move = encode(opMove);

		return move;

	}

	public static int[] decode(char[] playerMove) {

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


	public static char[] encode(int[] move) {
		char[] encoded = new char[4];
		char temp = Null;
		 
		for (int i = 0; i < 4; i++) {
			int puzzle = move[i];
			if (i == 0 || i == 2) {
				if (puzzle == 0) {
					temp = 'A';
				} else if (puzzle == 1) {
					temp = 'B';
				} else if (puzzle == 2) {
					temp = 'C';
				} else if (puzzle == 3) {
					temp = 'D';
				} else if (puzzle == 4) {
					temp = 'E';
				} else {
					break;
				}
			} else {
				temp = puzzle;
			}

			encoded[i] = temp;
		}

		return encoded;
	}



	/**
	 * Not implemented yet
	 *
	 */
	public String boardAsString(int[][] board) {
		for (int i = 0; i < 25; i++) {

		}
	}



	
	/**
	 * Orignial method - Place your algorithm int here
	 *
	 *
	 */
	public static char[] move() throws IOException{ // can remove exception when user input is removed
			
			char[] playerMove = null;
			
			// System.out.println("Board as matrix");
			
			// for(int index = 0; index < 25; index++){
				
			// 	boardMatrix[index%5][index/5] = boardAsString.charAt(index);
			// 	if(index%5 == 4)
			// 		System.out.print(boardMatrix[index%5][index/5] + "\n");
			// 	else
			// 		System.out.print(boardMatrix[index%5][index/5] + " ");
				
			// }
			//ystem.out.println("Previous move: " + otherMove());
			
			
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
			
			System.out.println("Enter move (for testing, to be replaced with algorithm):");
			playerMove = encode(myMove()); // for now move is just user input, for testing, replace this with your algorithm when ready
			
			
			
			//////////////////////////////////////////////////////
			// END OF ALGORITHM
			//////////////////////////////////////////////////////
			
			return playerMove;
			
		}

		/**
		 * randMove():
		 * 		This is the basic algorithm I used to test the
		 *      server. 
		 * @return move - returns and array of interger valuse
		 *                representing a player move
		 */
		public static int[] myMove() {

			int[] move = new int[4];

			Random rd = new Random();


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

			return move;
		}


		/**
		 * manualMove():
		 * 		
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
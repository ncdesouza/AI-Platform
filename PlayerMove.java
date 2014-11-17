import java.util.Scanner;
import java.util.Random;

public class PlayerMove {

	Scanner in = new Scanner(System.in);

	public int[] manMove() {
		int[] move = new int[4];

		System.out.println("x1: ");
        move[0] = in.nextInt();
        System.out.println("x2: ");
        move[1] = in.nextInt();
        System.out.println("x2: ");
        move[2] = in.nextInt();
        System.out.println("x2: ");
        move[3] = in.nextInt();

        return move;
	}

	public int[] Move() {

		Random rd = new Random();

		int x1 = rd.nextInt(5);
		int y1 = rd.nextInt(5);

		int xory = rd.nextInt(2);
		int norp = rd.nextInt(2);

		if (xory == 1 && ) {
			x1
		}
		if (norp == 0) {
		

		}




	}
}
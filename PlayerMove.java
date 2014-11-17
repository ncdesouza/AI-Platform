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

		int[] move = new int[4];

		Random rd = new Random();

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
}
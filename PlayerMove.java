import java.util.Scanner;

public class PlayerMove {

	Scanner in = new Scanner(System.in);

	public int[] Move() {
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
}
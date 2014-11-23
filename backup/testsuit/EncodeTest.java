import java.lang.System;

public class EncodeTest {

    public static void main(String[] args) {

        int[] test = {0, 0, 1, 0};
        System.out.println(encode(test));

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

}
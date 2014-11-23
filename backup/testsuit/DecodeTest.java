import java.lang.Character;

public class DecodeTest {

        public static void main(String[] args) {
                int[] test = new int[4];
                test = decode("A1B1");

                for (int i = 0; i < 4; i++) {
                        System.out.print(test[i]);
                }

        }

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

}
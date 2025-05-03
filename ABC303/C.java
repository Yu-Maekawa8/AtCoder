/**
 *5/3
 * 途中　HashSetを用いた解法　pairで回復アイテム管理 で訂正してみる　pairをテンプレートに追加
 * 
 */


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int moveNum = sc.nextInt();
            int item = sc.nextInt();
            int hp = sc.nextInt();
            int std = sc.nextInt();

            String s = sc.next();

            int[][] loc = new int[3][item];

            for (int i = 0; i < item; i++) {
                loc[0][i] = sc.nextInt();
                loc[1][i] = sc.nextInt();
            }

            boolean alive = true;

            int curx = 0, cury = 0;
            for(int i = 0; i < moveNum; i++) {
                if (s.charAt(i) == 'R') {
                    curx++;
                }else if (s.charAt(i) == 'L') {
                    curx--;
                }else if (s.charAt(i) == 'U') {
                    cury++;
                }else if (s.charAt(i) == 'D') {
                    cury--;
                }
                hp--;
                System.out.println(hp);
                if (hp <= 0 && i != moveNum - 1) {
                    alive = false;
                    break;
                }else {
                    for (int j = 0; j < item; j++) {
                        if (curx == loc[0][j] && cury == loc[1][j]  && loc[2][j] == 0 && hp < std) {
                            hp = std;
                            loc[2][j] = 1;
                            break;
                        }
                    }
                    
                }
            }



            if (alive) {
                System.out.println("Yes");
            } else {
                System.out.println("No");
            }

            

        }
    }
}

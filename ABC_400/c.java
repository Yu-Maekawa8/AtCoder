import java.util.*;

public class Main {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            long n = sc.nextLong();
            long cnt = 0;

            long[] base2 = new long[59];
            long[] basex = new long[(int) 4e5];
            List<Long> good = new ArrayList<>();
            for(int i = 1; i <= 59; i++) {
                // if(base2[i]+ (long) Math.pow(2, i) > 1e18) {
                //     break;
                // }
                base2[i-1] = (long) Math.pow(2, i);
                //System.out.println(base2[i-1]);
            }
            for(int i = 1; i <= 4e5; i++) {
                basex[i-1] =(long) Math.pow(i, 2);
            }

            for(int i = 0 ; i < 59 ; i++){
                if(base2[i] > n) {
                    break;
                }
                for(int j = 0 ; j < 4e5 ; j++){
                    if(basex[j] > n) {
                        break;
                    }
                    good.add(base2[i] * basex[j]);
                }
            }

            //Collections.sort(good);
            HashSet<Long> set = new HashSet<>();
            for(int i = 0 ; i < good.size() ; i++){
                //System.out.println(good.get(i));
                if(good.get(i) > n) {
                    continue;
                }
                set.add(good.get(i));
            }
            System.out.println(set.size());

        }
    }
}
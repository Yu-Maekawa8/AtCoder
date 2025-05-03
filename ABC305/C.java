//未完成

import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int h = sc.nextInt();
            int w = sc.nextInt();
            char[][] grid = new char[h][w];
            for (int i = 0; i < h; i++) {
                
                grid[i] = sc.next().toCharArray();
                
            }
            int fx = 0,fy = 0;
            int lx = 0,ly = 0;

            for (int i = 0; i < h; i++) {
                for (int j = 0; j < w; j++) {
                    if(grid[i][j] =='#'){
                        fx = i;
                        fy = j;
                        break;
                    }
                }
            }
            for (int i = h-1; i >= 0; i--) {
                for (int j = w-1; j >= 0; j--) {
                    if(grid[i][j] =='#'){
                        lx = i;
                        ly = j;
                        break;
                    }
                }
            }
            
            for (int i = fx; i <= lx; i++) {
                for (int j = fy; j <=ly ; j++) {
                    if(grid[i][j] == '.') {
                        System.out.println(i+1 + " " + (j+1));
                        break;
                    } 
                }
            }
        }
    }
}

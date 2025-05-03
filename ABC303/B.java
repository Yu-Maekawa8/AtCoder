import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int m = sc.nextInt();
            long cnt = 0;
            int[][] grid = new int[m][n];
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < n; j++) {
                    grid[i][j] = sc.nextInt();
                }
            }
            int[][] flag = new int[n][n];　　//隣接同士の記憶(回数で)

            for(int i = 0 ; i < m ; i++){
                for(int j = 0 ; j < n-1 ; j++){
                    flag[grid[i][j]-1][grid[i][j+1]-1]++;
                    flag[grid[i][j+1]-1][grid[i][j]-1]++;
                }
            }
            for (int i = 0; i < n; i++) {
                for (int j = i+1; j < n; j++) {
                    if(flag[i][j] <1) {
                        cnt++;
                    }
                }
            }
            System.out.println(cnt);
        }
    }
}

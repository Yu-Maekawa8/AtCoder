import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            char[][] grid = new char[n][n];
            char[][] rotated = new char[n][n];
            char[][] rotated2 = new char[n][n];
            char[][] rotated3 = new char[n][n];
            int[] kind = {0,1,2,3};
            int cnt = 0;
            for (int i = 0; i < n; i++) {
                grid[i] = sc.next().toCharArray();
            }
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    rotated[j][n - 1 - i] = grid[i][j];
                }
            }
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    rotated2[j][n - 1 - i] = rotated[i][j];
                }
            }
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    rotated3[j][n - 1 - i] = rotated2[i][j];
                }
            }

            char[][] grid2 = new char[n][n];
            for (int i = 0; i < n; i++) {
                grid2[i] = sc.next().toCharArray();
            }


            
            for(int j = 0 ; j < n ; j++){
                for (int k = 0; k < n; k++) {
                    if(grid2[j][k] != grid[j][k]){
                        kind[0]++;
                    }
                }
            }
            for(int j = 0 ; j < n ; j++){
                for (int k = 0; k < n; k++) {
                    if(grid2[j][k] != rotated[j][k]){
                        kind[1]++;
                    }
                }
            }
            for(int j = 0 ; j < n ; j++){
                for (int k = 0; k < n; k++) {
                    if(grid2[j][k] != rotated2[j][k]){
                        kind[2]++;
                    }
                }
            }
            for(int j = 0 ; j < n ; j++){
                for (int k = 0; k < n; k++) {
                    if(grid2[j][k] != rotated3[j][k]){
                        kind[3]++;
                    }
                }
            }
            int min = Integer.MAX_VALUE;

            for(int i = 0 ; i < 4 ; i++){
                if(kind[i] < min){
                    min = kind[i];
                }
            }
            System.out.println(min);

            
        }
    }
}

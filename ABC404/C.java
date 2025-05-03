/**
 * DFS BFS Union-find  を用いて解く問題
 * 
 * 本番はバグ修正間に合わず
 */ 

import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int m = sc.nextInt();

            int[][] grid = new int[m][2];
            for (int i = 0; i < m ; i++) {
                for (int j = 0; j < 2; j++) {
                    grid[i][j] = sc.nextInt();
                }
            }
            int[][] edge = new int[n][n];
            for (int i = 0; i < m; i++) {
                edge[grid[i][0]-1][grid[i][1]-1]++;
                edge[grid[i][1]-1][grid[i][0]-1]++;
            }
            boolean[] visited = new boolean[n];
            Arrays.fill(visited, false);

            int cnt = 0;
            int fi = 0;
            int fj = 0;

            for (int i = 0; i < n; i++) {
                for (int j = i+1; j < n; j++) {
                    if(edge[i][j] >= 1) {
                        fi = i;
                        fj = j;
                        visited[i] = true;
                        //System.out.println(fi + " " + fj);
                        break;
                    }
                }
                if(visited[fi] == true) {
                    break;
                }
            }
            int tmp = fj;
            int tmp2 = 0;
            for (int j = 0; j < n; j++) {
                
                cnt = 0;
                System.out.println("fl: "+ fj);
                for (int i = j; i < n; i++) {
                    // System.out.println("fl: "+ fj + " " + i);
                    // System.out.println("edge: "+ edge[fj][i]);
                    // System.out.println("visited: "+ visited[i]);
                    if(edge[fj][i] == 1 && visited[i] == false) {
                        cnt++;
                        tmp2 = i;
                        System.out.println(fj + " " + i);
                    }
                }
                if(cnt >= 3) {
                    //System.out.println(1);
                    System.out.println("No");
                    return;
                }else if(cnt == 0){
                    //System.out.println(2);
                    System.out.println("No");
                    return;
                }else{
                    //System.out.println(3);
                    //System.out.println("tmp: " + tmp);
                    visited[tmp] = true;
                    tmp = tmp2;
                }

            }
            System.out.println("Yes");
        }
    }
}


//----------------------これより下は本番後の解答-----------------


import java.util.*;
import java.math.*;

/*方針(２通り)
*
*１、DFSを使用する
*２、単純にクロスの中心から、４方向に伸びた５つの＃を認識させカウントする
*/

public class Main {
    boolean[][] visited;
    int[][] grid;
    int h, w;
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int h = sc.nextInt();
            int w = sc.nextInt();
            int n = Math.min(h, w);
            char[][] grid = new char[h][w];
            int[][] visited = new int[h][w];
            for (int i = 0; i < h; i++) {
                grid[i] = sc.next().toCharArray();
            }
            int[] ar = new int[n];
            for (int i = 0; i < ar.length; i++) {
                ar[i] = 0;
            }
            for (int i = 0; i < h; i++) {
                for (int j = 0; j <w; j++) {
                    ar[bfs(i, j, grid, new boolean[h][w])]++;
                }
            }


        }

    }
    static int bfs(int i , int j, char[][] graph,boolean[][] visited) {
        Queue<int[]> queue = new LinkedList<>();
        int[] dx = {1, -1, -1, 1};
        int[] dy = {-1, -1, 1, 1};
        queue.add(new int[]{i, j});
        visited[i][j] = true;
        int x, y;
        int cnt = 0;
    
        while (!queue.isEmpty()) {
            int[] node = queue.poll();
            x = node[0];
            y = node[1];
            cnt++;
            // Do something with node
            for (int k = 0; k < 4; k++) {
                if (!visited[x][y] && graph[x + dx[k]][y + dy[k]] == '#' &&
                    x + dx[k] >= 0 && x + dx[k] < graph.length && y + dy[k] >= 0 && y + dy[k] < graph[0].length) {
                    visited[x][y] = true;
                    queue.add(new int[]{x + dx[k], y + dy[k]});
                }else{
                    break;
                }
            }
        }
        return cnt;
    }
}

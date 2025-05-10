import java.util.*;

public class Main {
    static int[] dx = {1, 0, -1, 0};              
    static int[] dy = {0, 1, 0, -1};
    static char[] dirChar = {'^', '<', 'v', '>'}; 

    public static void bfsFromGoals(char[][] grid, int h, int w) {
        int[][] toGoalDir = new int[h][w];
        for (int[] row : toGoalDir) Arrays.fill(row, -1);

        Queue<int[]> queue = new LinkedList<>();

        // 複数のゴールからスタート（逆向きBFS）
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                if (grid[i][j] == 'E') {
                    queue.add(new int[]{i, j});
                    toGoalDir[i][j] = -2; // ゴール地点マーク
                }
            }
        }

        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            int x = cur[0], y = cur[1];

            for (int d = 0; d < 4; d++) {
                int nx = x + dx[d];
                int ny = y + dy[d];
                if (0 <= nx && nx < h && 0 <= ny && ny < w && grid[nx][ny] == '.' && toGoalDir[nx][ny] == -1) {
                    queue.add(new int[]{nx, ny});
                    toGoalDir[nx][ny] = d; // 来た方向（逆から見る）
                }
            }
        }

        // 矢印を記録、未到達は空白にする
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                int d = toGoalDir[i][j];
                if (grid[i][j] == '.' && d >= 0) {
                    grid[i][j] = dirChar[d]; // 進行方向に矢印
                } else if (grid[i][j] == '.' && d == -1) {
                    grid[i][j] = ' '; // ゴールにたどり着けないマス
                }
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int h = sc.nextInt();
        int w = sc.nextInt();

        char[][] grid = new char[h][w];

        for (int i = 0; i < h; i++) {
            grid[i] = sc.next().toCharArray();
        }
        sc.close();

        bfsFromGoals(grid, h, w);

        for (char[] row : grid) {
            for (char c : row) {
                System.out.print(c);
            }
            System.out.println();
        }

        
    }
}

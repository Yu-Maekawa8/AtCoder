import java.util.Arrays;

public class example {
    static final int INF = 1_000_000_000; // 到達不可能な距離はINFで表す
    static int[][] dist;

    public static void main(String[] args) {
        int n = 4; // 頂点数（0〜3）

        // 距離行列を初期化（自分自身は0、それ以外はINF）
        dist = new int[n][n];
        for (int i = 0; i < n; i++) {
            Arrays.fill(dist[i], INF);
            dist[i][i] = 0;
        }

        // 辺の追加（u → v のコストが cost）
        addEdge(0, 1, 2);
        addEdge(0, 2, 6);
        addEdge(1, 2, 3);
        addEdge(2, 3, 1);
        addEdge(1, 3, 7);

        // ワーシャルフロイド法
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (dist[i][k] < INF && dist[k][j] < INF) {
                        dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                    }
                }
            }
        }

        // 結果の出力
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][j] >= INF) {
                    System.out.print("INF ");
                } else {
                    System.out.print(dist[i][j] + " ");
                }
            }
            System.out.println();
        }
    }

    static void addEdge(int u, int v, int cost) {
        dist[u][v] = cost;
    }
}

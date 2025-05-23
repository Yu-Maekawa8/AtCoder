import java.util.*;

public class DijkstraUtil {

    // 辺の情報（行き先とコスト）
    static class Edge {
        int to, cost;
        Edge(int to, int cost) {
            this.to = to;
            this.cost = cost;
        }
    }

    // 優先度付きキューに入れるノード情報（頂点と距離）
    static class Node implements Comparable<Node> {
        int vertex, distance;
        Node(int vertex, int distance) {
            this.vertex = vertex;
            this.distance = distance;
        }

        // 距離が小さい順に並ぶよう比較
        @Override
        public int compareTo(Node other) {
            return Integer.compare(this.distance, other.distance);
        }
    }

    // ダイクストラ法の本体メソッド
    public static int[] dijkstra(List<List<Edge>> graph, int start) {
        int n = graph.size();                        // 頂点数
        int[] dist = new int[n];                     // 各頂点への最短距離
        Arrays.fill(dist, Integer.MAX_VALUE);        // 初期値は無限大
        dist[start] = 0;                             // 始点の距離は0

        PriorityQueue<Node> pq = new PriorityQueue<>();
        pq.offer(new Node(start, 0));                // 始点をキューに追加

        while (!pq.isEmpty()) {
            Node current = pq.poll();                // 現在のノードを取得
            int u = current.vertex;

            if (current.distance > dist[u]) continue; // 古い情報はスキップ

            for (Edge edge : graph.get(u)) {         // 隣接ノードを確認
                int v = edge.to;
                int cost = edge.cost;

                if (dist[v] > dist[u] + cost) {      // より短い経路が見つかれば更新
                    dist[v] = dist[u] + cost;
                    pq.offer(new Node(v, dist[v]));  // キューに追加
                }
            }
        }

        return dist; // 最短距離配列を返す
    }
}

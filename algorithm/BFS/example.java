import java.util.*;
import java.math.*;

public class Main {
    boolean[] visited = new boolean[100];
    int[][] graph = new int[100][100];
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            
        }
    }
    void bfs(int start, int[][] graph) {
        //boolean[] visited = new boolean[graph.length];
        Queue<Integer> queue = new LinkedList<>();
        queue.add(start);          //対象の開始始点を格納しておく(先に)　問題によれば for文などで2個以上入れておくなど
        visited[start] = true;
    
        while (!queue.isEmpty()) {
            int node = queue.poll();
            // Do something with node
            for (int neighbor : graph[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.add(neighbor);
                }
            }
        }
    }
}

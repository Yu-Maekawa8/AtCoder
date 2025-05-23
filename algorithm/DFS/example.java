import java.util.*;
import java.math.*;

public class Main {
    int[] visited = new int[100];
    int[][] graph = new int[100][100];
    public static void example(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
          //関数呼び出し&出力結果
        }
    }
    void dfs(int node, boolean[] visited, int[][] graph) {
        visited[node] = true;        //対象である始点,
        // Do something with node
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                dfs(neighbor, visited, graph);
            }
        }
    }
}

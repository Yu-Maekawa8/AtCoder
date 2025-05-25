/**
 * ABC 231 - D Neighbors
 * 
 * Union-Find practice.
 */


import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int m = sc.nextInt();

            int[][] ar = new int[m][2];
            int[] cnt = new int[n];     //次数の加算(頂点から出ている線の本数)
            for (int i = 0; i < m; i++) {
                ar[i][0] = sc.nextInt()-1;
                ar[i][1] = sc.nextInt()-1;
            }

            UnionFind uf = new UnionFind(n);

            for (int i = 0; i < m; i++) {
                int a = ar[i][0];
                int b = ar[i][1];
                if(uf.same(a, b)) {
                //同じグループに属しているなら、サイクルがある(サイクルになる前に属している親の部分が等しいことを判定)
                    System.out.println("No");
                    return;
                }
                uf.union(a, b);
                cnt[a]++;
                cnt[b]++;
            }
            for(int i = 0; i < n; i++) {
                //次数が3以上の頂点があれば、No
                if (cnt[i] >2) {
                    System.out.println("No");
                    return;
                }
            }

            System.out.println("Yes");
        }
    }
    static class UnionFind {
        int[] parent, size;
    
        UnionFind(int n) {
            parent = new int[n];
            size = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                size[i] = 1;
            }
        }
    
        int find(int x) {
            if (x != parent[x]) parent[x] = find(parent[x]);
            return parent[x];
        }
    
        void union(int x, int y) {
            int xr = find(x), yr = find(y);
            if (xr == yr) return;
            if (size[xr] < size[yr]) {
                parent[xr] = yr;
                size[yr] += size[xr];
            } else {
                parent[yr] = xr;
                size[xr] += size[yr];
            }
        }
    
        boolean same(int x, int y) {
            return find(x) == find(y);
        }
    }
}

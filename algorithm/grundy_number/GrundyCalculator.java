import java.util.*;

public class GrundyCalculator {

    // grundy(0) ～ grundy(n) の配列を返すメソッド
    public static int[] calculateGrundyArray(int n) {
        int[] dp = new int[n + 1];                       // grundy 数列を保存する配列
        dp[0] = dp[1] = 0;                               // 初期条件: grundy(0) = grundy(1) = 0

        // grundy(2) 以降を計算
        for (int x = 2; x <= n; x++) {
            HashSet<Integer> set = new HashSet<>();      // 各 i に対して grundy(i) ^ grundy(x - i - 2) を保存

            for (int i = 0; i <= x - 2; i++) {
                set.add(dp[i] ^ dp[x - i - 2]);          // 遷移先の Grundy 数の xor を集合に追加
            }

            // mex（最小の使われていない非負整数）を求める
            int g = 0;
            while (set.contains(g)) g++;

            dp[x] = g;                                   // grundy(x) を確定
        }

        return dp;                                       // Grundy 数列を返す
    }

    // grundy(n) だけを返すメソッド
    public static int grundy(int n) {
        return calculateGrundyArray(n)[n];             // 上のメソッドを使って配列から値を取得
    }

    // メイン関数
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 
        int n = sc.nextInt(); 

        int[] grundyArray = calculateGrundyArray(n);     // grundy(0)～grundy(n) を求める

        // 結果を出力
        for (int i = 0; i <= n; i++) {
            System.out.printf("grundy(%2d) = %d%n", i, grundyArray[i]);
        }

        // 必要なら grundy(n) のみを出力することも可能
        // System.out.println("grundy(" + n + ") = " + grundy(n));
    }
}

  import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            String str = sc.next();
            int[] ar = new int[str.length()];
            HashSet<Integer> set = new HashSet<>(); // 重複削除用
            for (int i = 0; i < ar.length; i++) {
                ar[i] = str.charAt(i);
            }

            List<Integer> list = Arrays.stream(ar).boxed().collect(Collectors.toList());
            List<Integer> list2 = new ArrayList<>(); // '(' のインデックス記録

            for (int i = 0; i < list.size(); i++) {
                Integer ch = list.get(i);
                if (ch >= 'a' && ch <= 'z') {
                    if(set.contains(ar[i]) && ar[i] != '(' && ar[i] != ')') {
                        System.out.println("No");
                        return;
                    } else {
                        set.add(ar[i]);
                    }
                    list.set(i, null);  // 小文字を削除マーク
                } else if (ch == ')') {
                    if (list2.size() > 0) {
                        int openIdx = list2.remove(list2.size() - 1); // 最後の '(' のインデックス
                        list.set(openIdx, null); // '(' を削除マーク
                        list.set(i, null);       // ')' を削除マーク
                    } else {
                        System.out.println("No");
                        return;
                    }
                } else if (ch == '(') {
                    list2.add(i);
                }
                //System.out.println(list);
                //System.out.println(list2);
            }

            // nullを一括削除
            list.removeIf(Objects::isNull);

            if (list.size() == 0) {
                System.out.println("Yes");
            } else {
                System.out.println("No");
            }
        }
    }
}

# 📚 Java ハッシュ関連データ構造メモ

ハッシュ関数を使ったデータ構造 `HashMap` と `HashSet` の基本的な使い方。

---

## ✅ HashMap（キーと値のペア）

```java
import java.util.*;

HashMap<String, Integer> map = new HashMap<>();

// 要素追加
map.put("apple", 100);
map.put("banana", 200);

// 要素取得
int applePrice = map.get("apple"); // 100

// 存在チェック
if (map.containsKey("banana")) {
    System.out.println("Banana is available.");
}

// 要素削除
map.remove("apple");

// 空チェック
if (map.isEmpty()) {
    System.out.println("The map is empty.");


}
```
# 📚 Java `getOrDefault()` を使ってカウントを +1

`getOrDefault()` を使って、Map でキーの存在をチェックし、もしキーが存在しなければデフォルト値を設定して、その後の処理で値を更新する方法。

---

## ✅ `getOrDefault()` でカウント +1 の例

```java
import java.util.*;

HashMap<String, Integer> countMap = new HashMap<>();

// アイテムカウント
countMap.put("apple", 5);
countMap.put("banana", 3);

// キーが存在する場合はその値を +1
countMap.put("apple", countMap.getOrDefault("apple", 0) + 1);  // apple → 6
countMap.put("banana", countMap.getOrDefault("banana", 0) + 1); // banana → 4

// キーが存在しない場合、デフォルト 0 から +1 される
countMap.put("orange", countMap.getOrDefault("orange", 0) + 1); // orange → 1

// 結果表示
System.out.println(countMap);

```

## HashSet(追加重複なし)
```Java
import java.util.*;

HashSet<Integer> set = new HashSet<>();

// 要素追加
set.add(10);
set.add(20);

// 要素確認
if (set.contains(10)) {
    System.out.println("10 is in the set.");
}

// 要素削除
set.remove(20);

// 空チェック
if (set.isEmpty()) {
    System.out.println("The set is empty.");
}
```

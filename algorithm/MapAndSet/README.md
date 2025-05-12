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

# Java データ構造メモ：Queue / Deque / Stack

競技プログラミングやアルゴリズム実装でよく使う基本構造。

---

## ✅ Queue（FIFO）

```java
import java.util.*;

Queue<Integer> q = new LinkedList<>();
q.offer(1);         // 追加（末尾）
int val = q.poll(); // 取り出し（先頭）
int peek = q.peek(); // 先頭確認
```


## ✅ Deque（両端対応／高速スタック代替）

```java
import java.util.*;

Deque<Integer> dq = new ArrayDeque<>();
dq.addFirst(1);      // 先頭に追加
dq.addLast(2);       // 末尾に追加
int f = dq.removeFirst(); // 先頭取り出し
int l = dq.removeLast();  // 末尾取り出し

// Stack風
dq.push(3);         // = addFirst
int s = dq.pop();   // = removeFirst
```

## ✅ Stack（非推奨：古い）

```java
import java.util.*;

Stack<Integer> st = new Stack<>();
st.push(10);            //追加
int top = st.pop();　　 //取り出し
int peek = st.peek();   //先頭見る
```

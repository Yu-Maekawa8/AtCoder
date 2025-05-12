📚 Java キュー・デック・スタックまとめ（競技プログラミング用）
このドキュメントでは、Javaでよく使う Queue、Deque、Stack の使い方とサンプルコードを簡潔に紹介します。AtCoder や競技プログラミングで頻出の構造です。

✅ Queue（先入れ先出し FIFO）
java
コピーする
編集する
import java.util.*;

Queue<Integer> queue = new LinkedList<>();

// 要素追加（末尾）
queue.offer(10);
queue.offer(20);

// 要素取得＆削除（先頭）
int front = queue.poll(); // → 10

// 先頭を見るだけ（削除しない）
int peek = queue.peek(); // → 20

// 空チェック
if (queue.isEmpty()) {
    System.out.println("Queue is empty.");
}
📌 主な用途：

幅優先探索（BFS）

待ち行列処理

✅ Deque（両端キュー／スタック代用）
java
コピーする
編集する
import java.util.*;

Deque<Integer> deque = new ArrayDeque<>();

// 両端に要素追加
deque.addFirst(1);  // 先頭に追加
deque.addLast(2);   // 末尾に追加

// 両端から取得＆削除
int first = deque.removeFirst(); // → 1
int last = deque.removeLast();   // → 2

// 両端から取得（削除しない）
int peekFirst = deque.peekFirst();
int peekLast = deque.peekLast();

// スタックとして使う（DequeはStackの代替に最適）
deque.push(3);      // = addFirst
int popped = deque.pop(); // = removeFirst

// 空チェック
if (deque.isEmpty()) {
    System.out.println("Deque is empty.");
}
📌 主な用途：

スライディングウィンドウ

スタックとキューの両方の用途

高速なLIFO（Stackの代替）

✅ Stack（LIFO構造・今は非推奨）
java
コピーする
編集する
import java.util.*;

Stack<Integer> stack = new Stack<>();

// 要素追加
stack.push(100);

// 要素取得＆削除（LIFO）
int top = stack.pop(); // → 100

// 要素取得（削除しない）
int peek = stack.peek();

// 空チェック
if (stack.isEmpty()) {
    System.out.println("Stack is empty.");
}
⚠️ Stack クラスはスレッドセーフの影響で 遅いため、競プロでは非推奨
➡️ 代わりに ArrayDeque を使うのが主流です

📝 補足：使い分けまとめ
操作の目的	構造	実装クラス例	備考
FIFO	Queue	LinkedList, ArrayDeque	幅優先探索（BFS）など
LIFO	Deque	ArrayDeque	スタックとして使用
両端操作	Deque	ArrayDeque	スライディングウィンドウ等
古いStack構造	Stack	Stack	非推奨、ArrayDeque推奨

🏁 おすすめ
スタックが必要なときは ArrayDeque を使おう

Stack クラスは避ける（遅い）

Queue として使うときも ArrayDeque の方が速くて安定

📚 Java キュー・デック・スタックまとめ（競技プログラミング用）
このドキュメントでは、Javaでよく使う Queue、Deque、Stack の使い方とサンプルコードを簡潔に紹介します。AtCoder や競技プログラミングで頻出の構造です。

✅ Queue（先入れ先出し FIFO）
java
コピーする
編集する
import java.util.*;

Queue<Integer> queue = new LinkedList<>();

// 要素追加（末尾）
queue.offer(10);
queue.offer(20);

// 要素取得＆削除（先頭）
int front = queue.poll(); // → 10

// 先頭を見るだけ（削除しない）
int peek = queue.peek(); // → 20

// 空チェック
if (queue.isEmpty()) {
    System.out.println("Queue is empty.");
}
📌 主な用途：

幅優先探索（BFS）

待ち行列処理

✅ Deque（両端キュー／スタック代用）
java
コピーする
編集する
import java.util.*;

Deque<Integer> deque = new ArrayDeque<>();

// 両端に要素追加
deque.addFirst(1);  // 先頭に追加
deque.addLast(2);   // 末尾に追加

// 両端から取得＆削除
int first = deque.removeFirst(); // → 1
int last = deque.removeLast();   // → 2

// 両端から取得（削除しない）
int peekFirst = deque.peekFirst();
int peekLast = deque.peekLast();

// スタックとして使う（DequeはStackの代替に最適）
deque.push(3);      // = addFirst
int popped = deque.pop(); // = removeFirst

// 空チェック
if (deque.isEmpty()) {
    System.out.println("Deque is empty.");
}
📌 主な用途：

スライディングウィンドウ

スタックとキューの両方の用途

高速なLIFO（Stackの代替）

✅ Stack（LIFO構造・今は非推奨）
java
コピーする
編集する
import java.util.*;

Stack<Integer> stack = new Stack<>();

// 要素追加
stack.push(100);

// 要素取得＆削除（LIFO）
int top = stack.pop(); // → 100

// 要素取得（削除しない）
int peek = stack.peek();

// 空チェック
if (stack.isEmpty()) {
    System.out.println("Stack is empty.");
}
⚠️ Stack クラスはスレッドセーフの影響で 遅いため、競プロでは非推奨
➡️ 代わりに ArrayDeque を使うのが主流です

📝 補足：使い分けまとめ
操作の目的	構造	実装クラス例	備考
FIFO	Queue	LinkedList, ArrayDeque	幅優先探索（BFS）など
LIFO	Deque	ArrayDeque	スタックとして使用
両端操作	Deque	ArrayDeque	スライディングウィンドウ等
古いStack構造	Stack	Stack	非推奨、ArrayDeque推奨

🏁 おすすめ
スタックが必要なときは ArrayDeque を使おう

Stack クラスは避ける（遅い）

Queue として使うときも ArrayDeque の方が速くて安定


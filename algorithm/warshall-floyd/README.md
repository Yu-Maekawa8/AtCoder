# ワーシャルフロイド法(Warshall-Floyd)

## 全ペアの最短経路を求めるアルゴリズム

### 動的計画法を使って解く

## 手順

１　dp[k][i][j]という 0から k-1までの頂点を使って iから jまで移動するときの最小コスト、と定義<br>

２　dp[0][i][j]は、直接つながった距離を求める<br>

３　dp[1][i][j]～dp[k-1][i][j]は、　それぞれ1～k-1 を経由したiからjまでの最小距離を求める

例<br>

![image](https://github.com/user-attachments/assets/707ed45b-a692-4942-81be-bd1ad0ca8005)

### 解き方
１　直接つながってるもの<br>
![image](https://github.com/user-attachments/assets/f5637f32-0494-46a5-8881-51f1476e8efd)

2-1  ノード１を経由したもの<br>
![image](https://github.com/user-attachments/assets/a1a9a823-d326-446f-a25e-09039754156c)=><br>
ベース更新
![image](https://github.com/user-attachments/assets/759093e2-d083-4562-9491-59ebaa613dbc)

2-2 ノード２を経由したもの<br>
![image](https://github.com/user-attachments/assets/4a6d88bf-ea8c-410a-bd71-5cfc60d75e1a)=><br>
ベース更新
![image](https://github.com/user-attachments/assets/f66bfc29-79f3-4e81-a597-ac5f9173c60e)

2-3 ノード3を経由したもの<br>
![image](https://github.com/user-attachments/assets/2ddc0148-cca4-4578-b7b7-e078d72858ba)=><br>
ベース更新
![image](https://github.com/user-attachments/assets/107f73bc-04a8-433a-95bd-4c638510c941)

2-4 ノード4を経由したもの<br>
![image](https://github.com/user-attachments/assets/5bae6063-39e4-4ea5-8990-d4ea54f1461b)=><br>
ベース更新
![image](https://github.com/user-attachments/assets/1395c512-1492-40e4-8e03-61a3c43b5de0)


答え<br>
![image](https://github.com/user-attachments/assets/114eb6a3-8a8d-47b6-bafb-ff7ac2d4f973)



## 参考

https://www.youtube.com/watch?v=qUICO9qz5E8




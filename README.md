# AtCoder Beginner Contest A〜D問題 解答リポジトリ（ABC126〜）

このリポジトリは、AtCoder Beginner Contest（ABC）における **A〜D問題の解答コード**を収録したものです。  
対象は **ABC126 〜 ** です。

---

## 目的

-AtCoderでの継続的な成長をGitHub上で可視化することで、学習の軌跡を記録・発信しています。
競技プログラミングの積み重ねと、それを通じた実装力向上が目標です。
---
## 📌 対象範囲

- **コンテストシリーズ**：AtCoder Beginner Contest（ABC）
- **問題範囲**：各コンテストの A / B / C / D 問題
- **ABC番号**：ABC126 〜（継続追加中）
- **使用言語**：主に Java（茶色コーダーになって随時　C++/Python での実装進めていきたい）

---

## 📁 ディレクトリ構成（例）

ABC/

├─ ABC126/

│ ├─ A.java

│ ├─ B.java

│ ├─ C.java

│ └─ D.java


- 各ディレクトリは `ABC+番号` で管理。
- 問題ごとに `A.java` ～ `D.java` を分割保存。

---

## 📘 解法メモと方針

- 各問題に対し、ソースコード冒頭または別ファイルで簡潔な解法メモを記載。
- 主要なアルゴリズム：全探索、累積和、二分探索、貪欲法、動的計画法（DP）、Union-Find、セグ木など。

---

## 🧰 環境・前提

- Java: JDK 17 
- 開発環境：VSCode / WSL Ubuntu
- 入力出力：標準IO形式（Scanner 使用）

---

## 🔧 進捗管理 & 自動同期

このリポジトリでは、次のようなタスク管理ルールで運用しています：

| 状態        | 説明                             |
|-------------|----------------------------------|
| ✅ 完了     | A〜D問題すべて解答＆整理済       |
| 🔄 作業中   | 一部問題の解答・整理進行中       |
| ⏳ 未着手   | フォルダのみ作成済               |

### 🤖 自動同期機能

**NEW!** AtCoder Problems APIと連携した自動同期機能を実装しました：

#### 🌟 主な機能
- **自動コード取得**: AtCoderでACした提出を自動でGitHubに同期
- **進捗自動更新**: 毎日自動で進捗表を更新
- **GitHub草生成**: ACするたびに自動コミットでContributionを蓄積
- **多言語対応**: Java, C++, Python, C#等の主要言語をサポート

#### ⏰ 実行スケジュール
- **進捗更新**: 毎日 日本時間 朝6時 (GitHub Actions)
- **AC同期**: 毎日 日本時間 朝7時 (GitHub Actions)
- **手動実行**: GitHub Actionsページから随時実行可能

#### 🔧 設定・使用方法

1. **基本設定**: `config.py`でユーザーIDや対象言語をカスタマイズ

2. **初回セットアップ（全履歴同期）**:
   ```bash
   # 既存フォルダと提出履歴を照合して一括同期
   python history_sync.py
   
   # または自動同期スクリプトで全履歴を対象
   python auto_sync_submissions.py --all-history
   ```

3. **日常的な同期**:
   ```bash
   # 過去7日間の新しいAC提出を同期
   python auto_sync_submissions.py
   
   # 過去30日間を対象
   python auto_sync_submissions.py --days-back 30
   ```

4. **テスト実行**:
   ```bash
   # 実際のファイル作成なしで動作確認
   python auto_sync_submissions.py --dry-run
   ```

#### 💡 既存ファイルとの統合

- **A.java, B.cpp等の標準ファイル**を優先的に利用
- **空ファイルやプレースホルダー**は自動で実際のコードに更新
- **既にコードがあるファイル**はスキップ（重複回避）
- **新しい提出**はタイムスタンプ付きファイルとして保存

#### 📊 同期状況の確認

- GitHub Actionsの実行ログで詳細確認
- `history_sync.py`実行時に詳細レポート生成
- 進捗表（`progress.md`）も自動更新

※詳細な進捗は GitHub Projects または issue を参照。

### ※AtCoder Problems で解いたものとGitHubで格納しているコード数が異なることがあります(2025/4以前のGithubを本格的に使い始める前に解いたやつが大半なため)

📊 [ABC進捗一覧はこちら](./progress.md)


---

## 🗂 今後の予定

- [ ] ABC405 以降の継続追加
- [ ] E問題以降も一部収録（余裕があったら）
- [ ] 問題タグ分類／アルゴリズム別 README の追加(学習も含め)
- [ ] レートの節目でQiita等で更新

---

## 🔗 参考リンク

- [AtCoder コンテスト一覧](https://atcoder.jp/contests/)
- [AtCoder Problems（進捗管理）](https://kenkoooo.com/atcoder/#/table/Y_maekawa)

---

## 📝 注意事項

このリポジトリは個人の学習・復習目的で運用しています。  
参考利用・転用は自由ですが、コピペでの無断提出は禁止です。




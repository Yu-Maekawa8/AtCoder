# AtCoder自動同期 使用ガイド

## 🚀 クイックスタート

### 1️⃣ セットアップ
```bash
# 必要パッケージのインストール
python setup.py

# 設定ファイルでユーザーID確認
# config.py の ATCODER_USER_ID を自分のIDに変更
```

### 2️⃣ 初回同期（推奨）
```bash
# 既存フォルダと提出履歴を照合
python history_sync.py

# テストモードで動作確認
python auto_sync_submissions.py --dry-run
```

### 3️⃣ 日常使用
```bash
# 最新のAC提出を自動同期
python auto_sync_submissions.py

# GitHub Actionsが毎日自動実行するので手動実行は不要
```

## 📋 各スクリプトの詳細

### `auto_sync_submissions.py` - メイン同期スクリプト
```bash
# 基本実行（過去7日間）
python auto_sync_submissions.py

# 期間指定
python auto_sync_submissions.py --days-back 30

# 全履歴同期（初回のみ推奨）
python auto_sync_submissions.py --all-history

# ドライラン（ファイル作成なし）
python auto_sync_submissions.py --dry-run

# ユーザーID指定
python auto_sync_submissions.py --user-id your_id
```

### `history_sync.py` - 既存フォルダとの統合
```bash
# 対話式で既存構造を分析して同期
python history_sync.py
```
- ABC126-406フォルダの分析
- 空ファイルやプレースホルダーの自動更新
- 既存コードとの重複回避

### `test_sync.py` - 動作テスト
```bash
# API接続やフォルダ作成機能のテスト
python test_sync.py
```

## 🔧 GitHub Actions設定

### 自動実行スケジュール
- **進捗更新**: 毎日朝6時（日本時間）
- **AC同期**: 毎日朝7時（日本時間）

### 手動実行
1. GitHubリポジトリの「Actions」タブ
2. 「Sync AtCoder Submissions」を選択
3. 「Run workflow」をクリック
4. オプション設定：
   - `days_back`: 何日前まで同期するか
   - `full_history`: 全履歴同期するか

## 📊 ファイル管理ルール

### 既存ファイルとの統合
| 状況 | 動作 |
|------|------|
| `A.java`等の標準ファイルが空 | 実際のコードで上書き |
| 標準ファイルにプレースホルダー | 実際のコードで更新 |
| 標準ファイルに有効なコード | スキップ（重複回避） |
| 標準ファイルなし | 新規作成 |
| 標準ファイル既存 + 新しい提出 | タイムスタンプ付きで保存 |

### ファイル命名規則
- **標準**: `A.java`, `B.cpp`, `C.py`, `D.java`
- **タイムスタンプ付き**: `a_20250625_140323.java`

## ⚙️ 設定のカスタマイズ

### `config.py`
```python
# AtCoderユーザーID（必須）
ATCODER_USER_ID = "your_atcoder_id"

# 対応言語の追加
SUPPORTED_LANGUAGES["Kotlin"] = ".kt"

# API呼び出し間隔の調整
RATE_LIMIT_DELAY = 2.0  # 秒

# コミットメッセージのカスタマイズ
COMMIT_MESSAGES = {
    "single": "✨ AC: {contest_problem}",
    # ...
}
```

## 🐛 トラブルシューティング

### よくある問題

#### ❌ API接続エラー
```bash
# 動作テストで確認
python test_sync.py

# ネットワーク接続確認
ping kenkoooo.com
```

#### ❌ ソースコード取得失敗
- AtCoderのサイト構造変更が原因の可能性
- `scraper.py`の更新が必要かも

#### ❌ ファイル保存エラー
- フォルダの書き込み権限確認
- ディスク容量確認

#### ❌ GitHub Actions失敗
- Actions画面でログ確認
- シークレット設定確認

### デバッグモード
```python
# config.py で設定
DEBUG = True
VERBOSE = True
```

## 📞 サポート

- **Issues**: GitHubのIssuesで報告
- **ログ**: GitHub Actionsの実行ログを確認
- **テスト**: `test_sync.py`で基本動作確認

## 🎯 活用のコツ

1. **初回**: `history_sync.py`で既存ファイルと統合
2. **日常**: GitHub Actionsの自動実行に任せる
3. **確認**: `progress.md`で同期状況をチェック
4. **草生成**: ACするたびに自動コミットで継続的に草が生える！

---

Happy Coding! 🎉

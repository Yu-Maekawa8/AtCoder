import os  # OS操作用モジュール（フォルダ内のファイル一覧取得など）
import re  # 正規表現モジュール（フォルダ名の形式チェック用）

# プログレス表を生成するメイン関数
def generate_progress(base_path='.', output_file='progress.md'):
    contests = []  # コンテストごとの状態・進捗情報を保存するリスト

    # フォルダ一覧を調べ、ABCコンテストに該当するものを処理
    for folder in sorted(os.listdir(base_path)):
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):  # フォルダ名が ABC123 の形式か判定
            problems = ['a', 'b', 'c', 'd']  # 対象の問題（A〜D）
            path = os.path.join(base_path, folder)  # コンテストフォルダのフルパス
            files = os.listdir(path)  # そのフォルダ内のファイル一覧を取得
            status = {}  # 各問題ごとの状態を記録（✅, ❌, 🚫）

            for p in problems:
                # 問題名（a, b, c, d）で始まるファイルをすべて抽出
                matched_files = [f for f in files if f.lower().startswith(p)]
                status[p] = '🚫'  # 初期状態：未実装

                # マッチしたファイルの中で状態を判定
                for fname in matched_files:
                    full_path = os.path.join(path, fname)  # ファイルのフルパス
                    if os.path.getsize(full_path) == 0:
                        continue  # 空ファイルの場合は「未実装」のままスキップ

                    if 'no' in fname.lower():
                        status[p] = '❌'  # noが含まれていれば「未AC」
                    else:
                        status[p] = '✅'  # noが含まれず、中身がある＝AC済み
                        break  # ✅が優先されるので、他のファイルは調べなくてよい

            # コンテスト全体の進捗ステータスを判定
            symbols = list(status.values())  # 各問題の記号だけ取り出す
            if all(s == '🚫' for s in symbols):
                overall = '⌛'  # 全部未実装（空ファイル）→ 未着手
            elif all(s == '✅' for s in symbols):
                overall = '✅'  # 全部AC済み → 完了
            else:
                overall = '🔄'  # それ以外 → 作業中

            # コンテスト名と状態、問題ごとの記号を記録
            contests.append((overall, folder.upper(), status))

    # Markdown形式でファイル出力（READMEなどに貼れる形式）
    lines = [
        "### 凡例\n",
        "- ABCD各問題：",
        "  - ✅ = AC済み",
        "  - ❌ = 実装済みだが未AC",
        "  - 🚫 = 未実装",
        "",
        "- コンテストの状態：",
        "  - ✅ 完了：A〜D問題すべて解答＆整理済",
        "  - 🔄 作業中：一部問題の解答・整理進行中",
        "  - ⌛ 未着手：フォルダのみ作成済（またはすべて空ファイル）",
        "",
        "| 状態 | コンテスト | A | B | C | D |",
        "|------|------------|---|---|---|---|"
    ]

    # 収集したコンテスト情報をMarkdownの行に変換
    for mark, name, status in contests:
        row = f"| {mark} | {name} | {status['a']} | {status['b']} | {status['c']} | {status['d']} |"
        lines.append(row)

    # 最終的に `progress.md` ファイルとして書き出す
    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))  # 改行で結合して保存

# このスクリプトが直接実行されたときのみ generate_progress を呼び出す
if __name__ == "__main__":
    generate_progress()
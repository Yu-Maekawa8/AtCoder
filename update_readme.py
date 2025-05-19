import os  # OS操作用モジュール（フォルダ内のファイル一覧取得など）
import re  # 正規表現モジュール（フォルダ名の形式チェック用）

def generate_progress(base_path='.', output_file='progress.md'):
    contests = []  # コンテスト名と各問題の状態を格納するリスト

    # 指定されたパス内のフォルダを確認
    for folder in sorted(os.listdir(base_path)):
        # "ABCxxx" の形式（大文字・小文字どちらもOK）だけ対象とする
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):
            problems = ['a', 'b', 'c', 'd']  # A〜D問題を対象とする
            path = os.path.join(base_path, folder)

            # フォルダ内のファイル名をすべて小文字で取得（拡張子含む）
            files_lower = [f.lower() for f in os.listdir(path)]

            status = {}  # 各問題の状態を記録する辞書
            for p in problems:
                # 問題ごとのファイル（小文字）を抽出（例: a.java, a(no).javaなど）
                problem_files = [f for f in files_lower if f.startswith(p)]

                if any("no" in f for f in problem_files):
                    status[p] = "❌"  # 「no」が含まれる場合 → 実装済みだが未AC
                elif f"{p}.java" in problem_files:
                    status[p] = "✅"  # 完全一致するファイルがある場合 → AC済み
                else:
                    status[p] = "🚫"  # 上記いずれにも当てはまらない → 未実装

            # コンテスト名（大文字）とステータスをリストに追加
            contests.append((folder.upper(), status))

    # Markdown 出力内容を構築
    lines = [
        "## ✅ AtCoder ABC進捗一覧（A〜D問題）",
        "",
        "凡例：✅ = AC済み / ❌ = 実装済みだが未AC / 🚫 = 未実装",
        "",
        "| 状態 | コンテスト | A | B | C | D |",  # ヘッダー行
        "|:-----:|:-----------|:-:|:-:|:-:|:-:|"  # 中央寄せ
    ]

    # 各コンテストの進捗を表に追記
    for name, status in contests:
        # すべての問題がACされていれば ✅、そうでなければ 🔄
        contest_mark = "✅" if all(v == "✅" for v in status.values()) else "🔄"

        # 1行分のMarkdown表記を生成
        row = f"| {contest_mark} | {name} | {status['a']} | {status['b']} | {status['c']} | {status['d']} |"
        lines.append(row)

    # 生成した行をMarkdownファイルに書き出し
    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# スクリプトを直接実行したときだけ実行
if __name__ == "__main__":
    generate_progress()

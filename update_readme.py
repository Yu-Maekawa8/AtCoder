import os  # OS操作（ディレクトリ走査など）に必要
import re  # 正規表現を使うために必要

def generate_progress(base_path='.', output_file='progress.md'):
    contests = []  # ABCコンテストごとの進捗情報を格納するリスト

    for folder in sorted(os.listdir(base_path)):  # 指定フォルダ内のすべてのディレクトリを取得
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):  # "ABCxxx" 形式にマッチするもののみ対象（大文字小文字問わず）
            problems = ['a', 'b', 'c', 'd']  # A〜D問題を対象
            path = os.path.join(base_path, folder)  # コンテストフォルダへのパスを作成
            files_lower = [f.lower() for f in os.listdir(path)]  # ファイル名をすべて小文字にして保持（大文字小文字を無視するため）

            status = {}  # 各問題の状態を格納する辞書
            for p in problems:
                # 指定問題に該当するファイルを取得（例："a.java", "a_no.java"など）
                problem_files = [f for f in files_lower if f.startswith(p)]

                # "no" が含まれていれば未AC、そうでなければAC済み、存在しなければ未実装
                if any("no" in f for f in problem_files):
                    status[p] = "❌"  # 実装済みだが未AC（例: a_no.java）
                elif any(f == f"{p}.java" for f in problem_files):
                    status[p] = "✅"  # AC済み（例: a.java）
                else:
                    status[p] = "☐"  # 未実装

            contests.append((folder.upper(), status))  # フォルダ名を大文字化して格納

    # Markdown出力の準備
    lines = [
        "## ✅ AtCoder ABC進捗一覧（A〜D問題）\n",
        "<details>\n<summary>凡例を表示</summary>\n",
        "\n- ✅：すべてのテストケースにAC（Accepted）",
        "- ❌：提出済みだが一部テストケース未AC（例：`A_no.java` など）",
        "- 🚫：未実装（コードが存在しない）\n",
        "</details>\n"
    ]

    symbol_map = {"❌": "❌", "☐": "🚫"}  # 表示用のシンボルマップ（☐→🚫）

    for name, status in contests:
        # すべてAC済みなら [x] をつける
        if all(v == "✅" for v in status.values()):
            lines.append(f"- [x] {name}（A〜D）")
        else:
            lines.append(f"- [ ] {name}")  # 未完了ならチェックなし
            for p in ['a', 'b', 'c', 'd']:
                symbol = "x" if status[p] == "✅" else " "  # チェックマーク用
                label = f"（{symbol_map.get(status[p], '')}）" if status[p] != "✅" else ""  # 凡例シンボル追加
                lines.append(f"  - [{symbol}] {p.upper()} {label}")  # 個別問題の行を追加

    # ファイルに書き出す
    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# スクリプトを直接実行したときのみ generate_progress を呼び出す
if __name__ == "__main__":
    generate_progress()

import os  # OS操作用モジュール（フォルダ内のファイル一覧取得など）
import re  # 正規表現モジュール（フォルダ名の形式チェック用）

def generate_progress(base_path='.', output_file='progress.md'):
    contests = []  # コンテストごとの進捗状況を格納するリスト

    for folder in sorted(os.listdir(base_path)):  # フォルダをアルファベット順に走査
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):  # フォルダ名がABC + 数字3桁かどうかを確認
            problems = ['a', 'b', 'c', 'd']  # 対象問題：A～D
            path = os.path.join(base_path, folder)  # 対象フォルダのパス作成
            files_lower = [f.lower() for f in os.listdir(path)]  # ファイル名をすべて小文字で取得（大文字小文字を無視）

            status = {}  # 各問題ごとのステータス（✅❌🚫）を格納

            for p in problems:  # A〜Dそれぞれの問題について
                problem_files = [f for f in files_lower if f.startswith(p)]  # 問題名で始まるファイルを抽出
                if any("no" in f for f in problem_files):  # 「no」がファイル名に含まれていれば未AC
                    status[p] = "❌"  # 実装済みだがACではない（例：D_no.java）
                elif f"{p}.java" in problem_files:  # 通常のファイル名（例：a.java）があればAC済み
                    status[p] = "✅"  # AC通過済み
                else:
                    status[p] = "🚫"  # ファイルが見つからない＝未提出

            contests.append((folder.upper(), status))  # コンテスト名とステータスを保存（フォルダ名は大文字に統一）

    # Markdown 出力部分
    lines = [
        "## ✅ AtCoder ABC進捗一覧（A〜D問題）\n",  # タイトル行
        "<details>\n<summary>凡例</summary>\n\n",  # 折りたたみ可能な凡例セクション開始
        "- ✅：AC（すべて通過）\n",                # 意味一覧（AC）
        "- ❌：提出済みだがACでない（例：D_no.java）\n",  # 意味一覧（未AC）
        "- 🚫：未提出\n\n",                         # 意味一覧（未提出）
        "</details>\n"  # 折りたたみ終了
    ]

    for name, status in contests:  # 各コンテストについて
        if all(v == "✅" for v in status.values()):  # A〜DすべてAC済みの場合
            lines.append(f"- ✅ {name}（A〜D）")  # チェック付きで表示
        else:
            lines.append(f"- 🚧 {name}")  # 進捗中の印として🚧
            for p in ['a', 'b', 'c', 'd']:  # 各問題について個別にマークを付ける
                label = status[p]  # ✅ or ❌ or 🚫
                lines.append(f"  - {p.upper()}：{label}")  # 例：  - A：✅

    # 最終的に progress.md に書き出し
    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))  # 改行で区切って出力

# スクリプトが直接実行されたときに実行される
if __name__ == "__main__":
    generate_progress()

import os  # OS操作用モジュール（フォルダ内のファイル一覧取得など）
import re  # 正規表現モジュール（フォルダ名の形式チェック用）

# プログレス表を生成するメイン関数
def generate_progress(base_path='.', output_file='progress.md'):
    contests = []  # コンテストデータを格納
    ac_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0}  # 各問題のAC数をカウント
    full_ac_count = 0  # コンテスト全AC数をカウント
    total_contest_count = 0  # コンテスト総数

    for folder in sorted(os.listdir(base_path)):
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):  # ABC形式のみ処理
            problems = ['a', 'b', 'c', 'd']
            path = os.path.join(base_path, folder)
            files = os.listdir(path)
            status = {}
            for p in problems:
                matched_files = [f for f in files if f.lower().startswith(p)]
                status[p] = '🚫'  # デフォルトは未実装
                for fname in matched_files:
                    full_path = os.path.join(path, fname)
                    if os.path.getsize(full_path) == 0:
                        continue
                    if 'no' in fname.lower():
                        status[p] = '❌'
                    else:
                        status[p] = '✅'
                        break  # ✅が見つかれば優先

            # 状態判定
            symbols = list(status.values())
            if all(s == '🚫' for s in symbols):
                overall = '⌛'  # 全未実装
            elif all(s == '✅' for s in symbols):
                overall = '✅'  # 全部AC済み
                full_ac_count += 1
            else:
                overall = '🔄'  # 一部解答中

            total_contest_count += 1  # コンテスト数カウント

            # AC数を加算
            for p in problems:
                if status[p] == '✅':
                    ac_counts[p] += 1

            contests.append((overall, folder.upper(), status))

    # Markdown出力行の生成
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
        "### 🧮 現在の進捗状況",
        f"- ✅ A問題AC数：{ac_counts['a']}",
        f"- ✅ B問題AC数：{ac_counts['b']}",
        f"- ✅ C問題AC数：{ac_counts['c']}",
        f"- ✅ D問題AC数：{ac_counts['d']}",
        f"- ✅ 全問題AC済みのコンテスト数：{full_ac_count}",
        f"- 📦 計コンテスト数：{total_contest_count}",
        "",
        "| 状態 | コンテスト | A | B | C | D |",
        "|------|------------|---|---|---|---|"
    ]

    # コンテスト行を追加（⌛のものはABCDを表示しない）
    for mark, name, status in contests:
        if mark == '⌛':
            lines.append(f"| {mark} | {name} | - | - | - | - |")
        else:
            row = f"| {mark} | {name} | {status['a']} | {status['b']} | {status['c']} | {status['d']} |"
            lines.append(row)

    # ファイル書き出し
    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# スクリプトが直接実行されたときのみ動作
if __name__ == "__main__":
    generate_progress()
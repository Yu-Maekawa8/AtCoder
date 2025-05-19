import os  # OS操作用モジュール（フォルダ内のファイル一覧取得など）
import re  # 正規表現モジュール（フォルダ名の形式チェック用）

# プログレス表を生成するメイン関数
def generate_progress(base_path='.', output_file='progress.md'):
    contests = []  # コンテストごとのデータ（状態・名前・問題ごとの進捗）を保存するリスト
    ac_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'full': 0}  # A〜DのAC数と、全完了コンテスト数を集計する辞書

    # フォルダ一覧を調べて、ABC形式（例: ABC123）にマッチするものだけ処理
    for folder in sorted(os.listdir(base_path)):
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):  # フォルダ名がABC形式かどうかを判定
            problems = ['a', 'b', 'c', 'd']  # 対象の問題：A〜D
            path = os.path.join(base_path, folder)  # コンテストフォルダのフルパスを作成
            files = os.listdir(path)  # フォルダ内のファイル一覧を取得
            status = {}  # 各問題の進捗状態を記録する辞書

            # 各問題（a〜d）について状態を判定
            for p in problems:
                matched_files = [f for f in files if f.lower().startswith(p)]  # 該当するファイルを抽出
                status[p] = '🚫'  # 初期状態は「未実装」

                for fname in matched_files:
                    full_path = os.path.join(path, fname)  # ファイルのフルパスを取得

                    if os.path.getsize(full_path) == 0:
                        continue  # 空ファイルは未実装としてスキップ

                    if 'no' in fname.lower():
                        status[p] = '❌'  # ファイル名に "no" を含む → 実装済だが未AC
                    else:
                        status[p] = '✅'  # 中身があり "no" を含まない → AC済み
                        break  # ✅ が見つかったらそれを優先して終了

            symbols = list(status.values())  # 状態（✅, ❌, 🚫）の一覧を取得

            # コンテスト全体の進捗ステータスを判定
            if all(s == '🚫' for s in symbols):
                overall = '⌛'  # 全部未実装 → 未着手
            elif all(s == '✅' for s in symbols):
                overall = '✅'  # 全部AC済み → 完了
                ac_counts['full'] += 1  # 全完了コンテスト数を加算
            else:
                overall = '🔄'  # 一部解答済み → 作業中

            # ✅の数を問題ごとに加算
            for p in problems:
                if status[p] == '✅':
                    ac_counts[p] += 1

            # コンテストごとの結果を保存
            contests.append((overall, folder.upper(), status))

    # Markdown出力用の行を準備（凡例などを記載）
    lines = [
        "### 凡例\n",  # タイトル
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
        # 現在のAC状況（A〜D、全完了コンテスト数）を追加表示
        f"- 現在のAC数：A={ac_counts['a']} / B={ac_counts['b']} / C={ac_counts['c']} / D={ac_counts['d']} / 全完了コンテスト={ac_counts['full']}",
        "",
        # Markdown形式の表ヘッダー
        "| 状態 | コンテスト | A | B | C | D |",
        "|------|------------|---|---|---|---|"
    ]

    # コンテストごとの進捗をMarkdown表の行として追加
    for mark, name, status in contests:
        if mark == '⌛':  # 未着手のときは A〜D を「-」で表示
            lines.append(f"| {mark} | {name} | - | - | - | - |")
        else:  # それ以外は通常通り表示
            lines.append(f"| {mark} | {name} | {status['a']} | {status['b']} | {status['c']} | {status['d']} |")

    # 最終的に progress.md ファイルとして保存
    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))  # 各行を改行で結合して書き込む

# このスクリプトが直接実行されたときのみ実行
if __name__ == "__main__":
    generate_progress()
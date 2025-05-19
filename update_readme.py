import os
import re

def generate_progress(base_path='.', output_file='progress.md'):
    contests = []
    for folder in sorted(os.listdir(base_path)):
        if re.match(r"abc\d{3}", folder):
            problems = ['a', 'b', 'c', 'd']
            path = os.path.join(base_path, folder)
            solved = {p: any(
                os.path.isfile(os.path.join(path, f"{p}.{ext}"))
                for ext in ['java']
            ) for p in problems}
            contests.append((folder.upper(), solved))

    # Markdown 出力
    lines = ["## ✅ AtCoder ABC進捗一覧（A〜D問題）\n"]
    for name, solved in contests:
        if all(solved.values()):
            lines.append(f"- [x] {name}（A〜D）")
        else:
            lines.append(f"- [ ] {name}")
            for p in ['a', 'b', 'c', 'd']:
                mark = 'x' if solved[p] else ' '
                lines.append(f"  - [{mark}] {p.upper()}")

    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# 実行
if __name__ == "__main__":
    generate_progress()

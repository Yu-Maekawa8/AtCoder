import os
import re

def generate_progress(base_path='.', output_file='progress.md'):
    contests = []
    for folder in sorted(os.listdir(base_path)):
        if re.match(r"ABC\d{3}", folder, re.IGNORECASE):
            problems = ['a', 'b', 'c', 'd']
            path = os.path.join(base_path, folder)
            files_lower = [f.lower() for f in os.listdir(path)]

            status = {}
            for p in problems:
                problem_files = [f for f in files_lower if f.startswith(p)]
                if any("no" in f for f in problem_files):
                    status[p] = "❌"  # 実装済みだが未AC（noが含まれる）
                elif any(f == f"{p}.java" for f in problem_files):
                    status[p] = "✅"  # AC済み（no含まない .java）
                else:
                    status[p] = "☐"  # 未実装

            contests.append((folder.upper(), status))

    # Markdownの出力準備
    lines = [
        "## ✅ AtCoder ABC進捗一覧（A〜D問題）\n",
        "### 凡例：",
        "- ✅：すべてのテストケースにAC（Accepted）",
        "- ❌：提出済みだが一部テストケース未AC（例：`A_no.java` など）",
        "- 🚫：未実装（コードが存在しない）\n"
    ]

    symbol_map = {"❌": "❌", "☐": "🚫"}
    for name, status in contests:
        if all(v == "✅" for v in status.values()):
            lines.append(f"- [x] {name}（A〜D）")
        else:
            lines.append(f"- [ ] {name}")
            for p in ['a', 'b', 'c', 'd']:
                symbol = "x" if status[p] == "✅" else " "
                label = f"（{symbol_map.get(status[p], '')}）" if status[p] != "✅" else ""
                lines.append(f"  - [{symbol}] {p.upper()} {label}")

    with open(os.path.join(base_path, output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# 実行
if __name__ == "__main__":
    generate_progress()

import os
import re

# ABCフォルダの最大番号を取得し、次のフォルダを作る
def create_next_abc_folder(base='.'):
    abc_folders = [f for f in os.listdir(base) if re.match(r'ABC\d{3}$', f)]
    numbers = [int(f[3:]) for f in abc_folders]
    next_number = max(numbers, default=406) + 1

    folder_name = f"ABC{next_number:03d}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        for p in ['A', 'B', 'C', 'D']:
            with open(os.path.join(folder_name, f"{p}.java"), 'w') as f:
                pass
        print(f"✅ Created {folder_name}")
    else:
        print(f"🟦 Already exists: {folder_name}")

# 実行
if __name__ == "__main__":
    create_next_abc_folder()

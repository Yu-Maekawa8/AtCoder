import os

# フォルダを作成する関数
def create_abc_folders(start=126, end=406):
    for num in range(start, end + 1):
        folder_name = f"ABC{num:03d}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            for p in ['A', 'B', 'C', 'D']:
                with open(os.path.join(folder_name, f"{p}.java"), 'w') as f:
                    pass  # 空ファイル作成
            print(f"✅ Created {folder_name}")
        else:
            print(f"🟦 Skipped {folder_name} (already exists)")

# 実行
if __name__ == "__main__":
    create_abc_folders()
# 使い方
# 上記のコードをファイルに保存して実行することで、指定した範囲のフォルダとファイルを作成できます。
#!/usr/bin/env python3
"""
AtCoder自動同期機能のセットアップスクリプト
"""

import os
import sys
import subprocess

def install_requirements():
    """必要なパッケージをインストール"""
    print("📦 必要なパッケージをインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ パッケージインストール完了")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ パッケージインストール失敗: {e}")
        return False

def setup_config():
    """設定ファイルの確認"""
    print("\n⚙️  設定ファイル確認中...")
    
    if os.path.exists("config.py"):
        print("✅ config.py が見つかりました")
        
        # config.pyからユーザーIDを読み取り
        try:
            import config
            user_id = config.ATCODER_USER_ID
            print(f"📋 設定されたユーザーID: {user_id}")
            
            # ユーザーIDが正しく設定されているか確認
            if user_id and user_id != "your_atcoder_id":
                print("✅ ユーザーIDは適切に設定されています")
                return True
            else:
                print("⚠️  config.pyでATCODER_USER_IDを正しく設定してください")
                return False
        except Exception as e:
            print(f"❌ config.py読み込みエラー: {e}")
            return False
    else:
        print("❌ config.py が見つかりません")
        return False

def run_test():
    """テストスクリプトを実行"""
    print("\n🧪 動作テスト実行中...")
    try:
        result = subprocess.run([sys.executable, "test_sync.py"], 
                              capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.stderr:
            print("エラー出力:")
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ テストがタイムアウトしました")
        return False
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        return False

def main():
    """セットアップメイン処理"""
    print("🚀 AtCoder自動同期機能セットアップ開始")
    print("=" * 50)
    
    steps = [
        ("パッケージインストール", install_requirements),
        ("設定ファイル確認", setup_config),
        ("動作テスト", run_test)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 ステップ: {step_name}")
        if not step_func():
            print(f"\n❌ セットアップ失敗: {step_name}")
            print("\n修正後に再度実行してください:")
            print("python setup.py")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 セットアップ完了！")
    print("\n📝 次のステップ:")
    print("1. config.pyでATCODER_USER_IDを自分のIDに変更")
    print("2. 手動実行でテスト:")
    print("   python auto_sync_submissions.py --dry-run")
    print("3. GitHub Actionsで自動実行開始")
    print("\n📚 詳細な使用方法はREADME.mdを参照してください")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

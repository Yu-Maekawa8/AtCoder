import requests
import json
import time
from config import ATCODER_USER_ID

def test_atcoder_problems_api():
    """AtCoder Problems APIの接続テストを行う"""
    print("🔍 AtCoder Problems API 接続テスト開始")
    print("=" * 50)
    
    base_url = "https://kenkoooo.com/atcoder/atcoder-api"
    
    # 1. 基本接続テスト
    print("1️⃣ 基本接続テスト...")
    try:
        response = requests.get(f"{base_url}/info", timeout=10)
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 基本接続: 成功")
        else:
            print(f"   ❌ 基本接続: 失敗 ({response.status_code})")
    except Exception as e:
        print(f"   ❌ 基本接続: エラー - {e}")
    
    time.sleep(1)
    
    # 2. 問題データ取得テスト
    print("\n2️⃣ 問題データ取得テスト...")
    try:
        # 正しいエンドポイントを試す
        endpoints = [
            "/problems",
            "/v3/problems", 
            "/info/problems"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                print(f"   試行中: {url}")
                response = requests.get(url, timeout=10)
                print(f"   ステータス: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ 問題データ取得成功: {len(data)}件")
                    print(f"   サンプル: {data[0] if data else 'データなし'}")
                    break
                else:
                    print(f"   ❌ {endpoint}: 失敗 ({response.status_code})")
            except Exception as e:
                print(f"   ❌ {endpoint}: エラー - {e}")
                
        time.sleep(1)
                
    except Exception as e:
        print(f"   ❌ 問題データ取得: エラー - {e}")
    
    # 3. ユーザー提出履歴テスト
    print(f"\n3️⃣ ユーザー提出履歴テスト (ユーザー: {ATCODER_USER_ID})...")
    try:
        # 複数のエンドポイントを試す
        user_endpoints = [
            f"/results?user={ATCODER_USER_ID}",
            f"/v3/user/submissions?user={ATCODER_USER_ID}",
            f"/user/submissions?user={ATCODER_USER_ID}",
            f"/submissions/user/{ATCODER_USER_ID}"
        ]
        
        for endpoint in user_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                print(f"   試行中: {url}")
                response = requests.get(url, timeout=10)
                print(f"   ステータス: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ 提出履歴取得成功: {len(data)}件")
                    if data:
                        latest = data[0]
                        print(f"   最新提出: {latest.get('problem_id', 'N/A')} - {latest.get('result', 'N/A')}")
                    break
                else:
                    print(f"   ❌ {endpoint}: 失敗 ({response.status_code})")
                    if response.status_code == 400:
                        print(f"   レスポンス: {response.text[:200]}")
                        
            except Exception as e:
                print(f"   ❌ {endpoint}: エラー - {e}")
                
        time.sleep(1)
            
    except Exception as e:
        print(f"   ❌ ユーザー提出履歴: エラー - {e}")
    
    # 4. AC提出のみフィルタリングテスト
    print(f"\n4️⃣ AC提出フィルタリングテスト...")
    try:
        # AC提出のみを取得するエンドポイントを試す
        ac_endpoints = [
            f"/results?user={ATCODER_USER_ID}&result=AC",
            f"/v3/user/ac?user={ATCODER_USER_ID}",
            f"/user/ac?user={ATCODER_USER_ID}"
        ]
        
        for endpoint in ac_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                print(f"   試行中: {url}")
                response = requests.get(url, timeout=10)
                print(f"   ステータス: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ AC提出取得成功: {len(data)}件")
                    if data:
                        # ABC問題のみカウント
                        abc_problems = [d for d in data if d.get('problem_id', '').startswith('abc')]
                        print(f"   ABC問題AC数: {len(abc_problems)}件")
                    break
                else:
                    print(f"   ❌ {endpoint}: 失敗 ({response.status_code})")
                    
            except Exception as e:
                print(f"   ❌ {endpoint}: エラー - {e}")
                
    except Exception as e:
        print(f"   ❌ AC提出フィルタリング: エラー - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 AtCoder Problems API テスト完了")

def test_direct_atcoder_access():
    """直接AtCoderサイトへのアクセステスト"""
    print("\n🌐 AtCoder直接アクセステスト開始")
    print("=" * 50)
    
    # 1. AtCoderサイト基本接続
    print("1️⃣ AtCoderサイト接続テスト...")
    try:
        response = requests.get("https://atcoder.jp/", timeout=10)
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ AtCoderサイト接続: 成功")
        else:
            print(f"   ❌ AtCoderサイト接続: 失敗 ({response.status_code})")
    except Exception as e:
        print(f"   ❌ AtCoderサイト接続: エラー - {e}")
    
    # 2. ユーザーページアクセス
    print(f"\n2️⃣ ユーザーページアクセステスト (ユーザー: {ATCODER_USER_ID})...")
    try:
        user_url = f"https://atcoder.jp/users/{ATCODER_USER_ID}"
        response = requests.get(user_url, timeout=10)
        print(f"   URL: {user_url}")
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ ユーザーページアクセス: 成功")
        else:
            print(f"   ❌ ユーザーページアクセス: 失敗 ({response.status_code})")
    except Exception as e:
        print(f"   ❌ ユーザーページアクセス: エラー - {e}")
    
    # 3. 提出履歴ページアクセス（要ログイン）
    print(f"\n3️⃣ 提出履歴ページアクセステスト...")
    try:
        submissions_url = f"https://atcoder.jp/users/{ATCODER_USER_ID}/history"
        response = requests.get(submissions_url, timeout=10)
        print(f"   URL: {submissions_url}")
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 提出履歴ページアクセス: 成功")
        elif response.status_code == 403:
            print("   ⚠️  提出履歴ページアクセス: 要ログイン")
        else:
            print(f"   ❌ 提出履歴ページアクセス: 失敗 ({response.status_code})")
    except Exception as e:
        print(f"   ❌ 提出履歴ページアクセス: エラー - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 AtCoder直接アクセステスト完了")

if __name__ == "__main__":
    print("🚀 AtCoder API・サイト接続テスト開始")
    print(f"🆔 テスト対象ユーザー: {ATCODER_USER_ID}")
    print()
    
    # AtCoder Problems API テスト
    test_atcoder_problems_api()
    
    time.sleep(2)
    
    # 直接AtCoderサイトアクセステスト
    test_direct_atcoder_access()
    
    print("\n🎉 全テスト完了!")
    print("結果を確認して、動作するエンドポイントを特定してください。")
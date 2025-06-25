import requests
from bs4 import BeautifulSoup
from config import ATCODER_USER_ID

def debug_atcoder_page():
    """AtCoderページの構造をデバッグ"""
    print("🔍 AtCoderページ構造デバッグ開始")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # 1. ユーザーページの確認
    print(f"1️⃣ ユーザーページ確認: {ATCODER_USER_ID}")
    try:
        url = f"https://atcoder.jp/users/{ATCODER_USER_ID}"
        response = session.get(url, timeout=10)
        print(f"   URL: {url}")
        print(f"   ステータス: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ページタイトル確認
            title = soup.find('title')
            print(f"   タイトル: {title.get_text() if title else 'なし'}")
            
            # ユーザー情報確認
            user_info = soup.find('div', class_='row')
            if user_info:
                print("   ✅ ユーザー情報が見つかりました")
            else:
                print("   ❌ ユーザー情報が見つかりません")
                
        else:
            print(f"   ❌ ユーザーページアクセス失敗: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ ユーザーページ確認エラー: {e}")
    
    # 2. 提出履歴ページの詳細確認
    print(f"\n2️⃣ 提出履歴ページ詳細確認...")
    try:
        url = f"https://atcoder.jp/users/{ATCODER_USER_ID}/history"
        response = session.get(url, timeout=10)
        print(f"   URL: {url}")
        print(f"   ステータス: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ページタイトル確認
            title = soup.find('title')
            print(f"   タイトル: {title.get_text() if title else 'なし'}")
            
            # テーブル構造を詳しく調査
            print("   📊 テーブル構造調査...")
            tables = soup.find_all('table')
            print(f"   テーブル数: {len(tables)}")
            
            for i, table in enumerate(tables):
                print(f"   テーブル{i+1}:")
                print(f"     クラス: {table.get('class', 'なし')}")
                
                # ヘッダーを確認
                headers = table.find('thead')
                if headers:
                    header_texts = [th.get_text(strip=True) for th in headers.find_all('th')]
                    print(f"     ヘッダー: {header_texts}")
                
                # 最初の数行を確認
                tbody = table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')[:3]  # 最初の3行のみ
                    print(f"     データ行数: {len(tbody.find_all('tr'))}行")
                    
                    for j, row in enumerate(rows):
                        cols = row.find_all('td')
                        col_texts = [td.get_text(strip=True)[:20] + '...' if len(td.get_text(strip=True)) > 20 
                                   else td.get_text(strip=True) for td in cols]
                        print(f"     行{j+1}: {col_texts}")
                else:
                    print("     データ行: なし")
            
            # ページネーション確認
            print("   📄 ページネーション調査...")
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                print("   ✅ ページネーションが見つかりました")
                links = pagination.find_all('a')
                print(f"   ページリンク数: {len(links)}")
            else:
                print("   📄 ページネーションなし")
                
            # 非公開メッセージを確認
            error_messages = soup.find_all('div', class_='alert')
            if error_messages:
                for msg in error_messages:
                    print(f"   ⚠️ アラート: {msg.get_text(strip=True)}")
                    
        else:
            print(f"   ❌ 提出履歴ページアクセス失敗: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 提出履歴ページ確認エラー: {e}")
    
    # 3. 公開されている他のページを確認
    print(f"\n3️⃣ 公開情報ページ確認...")
    
    # AtCoder Problemsサイトでの確認
    print("   AtCoder Problems確認...")
    try:
        url = f"https://kenkoooo.com/atcoder/#/user/{ATCODER_USER_ID}"
        response = session.get(url, timeout=10)
        print(f"   AtCoder Problems URL: {url}")
        print(f"   ステータス: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ AtCoder Problemsでユーザーが見つかりました")
        else:
            print(f"   ❌ AtCoder Problemsアクセス失敗: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ AtCoder Problems確認エラー: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 デバッグ完了")

def test_alternative_endpoints():
    """代替エンドポイントのテスト"""
    print("\n🔄 代替エンドポイントテスト開始")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # AtCoder Problems API の別のベースURL試行
    alternative_apis = [
        "https://kenkoooo.com/atcoder/resources",
        "https://kenkoooo.com/atcoder/internal-api",
        "https://atcoder-api.vercel.app",
        "https://atcoder.jp/contests/abc300/submissions?f.User=Y_maekawa"  # 特定コンテストの提出履歴
    ]
    
    for api_url in alternative_apis:
        try:
            print(f"   試行中: {api_url}")
            response = session.get(api_url, timeout=10)
            print(f"   ステータス: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ 成功: {api_url}")
                # 少しだけ内容を確認
                content = response.text[:200]
                print(f"   内容サンプル: {content}...")
            else:
                print(f"   ❌ 失敗: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ エラー: {e}")
        
        print()

if __name__ == "__main__":
    debug_atcoder_page()
    test_alternative_endpoints()
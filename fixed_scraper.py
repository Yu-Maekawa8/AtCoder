import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from config import ATCODER_USER_ID

class AtCoderDataScraper:
    def __init__(self, user_id=None):
        self.user_id = user_id or ATCODER_USER_ID
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_contest_history(self):
        """コンテスト参加履歴を取得"""
        print(f"🏆 {self.user_id}のコンテスト履歴を取得中...")
        
        try:
            url = f"https://atcoder.jp/users/{self.user_id}/history"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ コンテスト履歴取得失敗: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='table')
            
            if not table:
                print("❌ コンテスト履歴テーブルが見つかりません")
                return []
            
            contests = []
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        date = cols[0].get_text(strip=True)
                        contest_link = cols[1].find('a')
                        if contest_link:
                            contest_name = contest_link.get_text(strip=True)
                            contest_url = contest_link.get('href')
                            contests.append({
                                'date': date,
                                'name': contest_name,
                                'url': contest_url
                            })
            
            print(f"✅ コンテスト履歴取得完了: {len(contests)}件")
            return contests
            
        except Exception as e:
            print(f"❌ コンテスト履歴取得エラー: {e}")
            return []
    
    def get_submissions_from_vercel_api(self):
        """Vercel APIから提出データを取得"""
        print(f"🔄 Vercel APIから提出データを取得中...")
        
        try:
            # Vercel APIを使用してAtCoderデータを取得
            api_url = "https://atcoder-api.vercel.app"
            
            # APIの仕様を確認
            response = self.session.get(f"{api_url}/api/submissions/{self.user_id}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Vercel API: 提出データ取得成功")
                return data
            else:
                print(f"❌ Vercel API失敗: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Vercel API エラー: {e}")
            return None
    
    def get_atcoder_problems_alternative(self):
        """AtCoder Problems の代替手段を試行"""
        print(f"🔍 AtCoder Problems 代替手段を試行中...")
        
        # 複数のベースURLを試行
        base_urls = [
            "https://kenkoooo.com/atcoder/atcoder-api",
            "https://atcoder.jp/users/" + self.user_id
        ]
        
        for base_url in base_urls:
            try:
                print(f"   試行中: {base_url}")
                
                if "kenkoooo.com" in base_url:
                    # AtCoder Problems APIの様々なエンドポイントを試行
                    endpoints = [
                        f"/v3/user/submissions?user={self.user_id}",
                        f"/results?user={self.user_id}",
                        f"/submissions?user={self.user_id}"
                    ]
                    
                    for endpoint in endpoints:
                        url = base_url + endpoint
                        response = self.session.get(url, timeout=10)
                        
                        if response.status_code == 200:
                            try:
                                data = response.json()
                                print(f"   ✅ 成功: {endpoint} ({len(data)}件)")
                                return data
                            except:
                                pass
                        elif response.status_code != 404:
                            print(f"   ⚠️  {endpoint}: {response.status_code}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ {base_url}: {e}")
        
        return None
    
    def get_abc_contests_from_history(self):
        """コンテスト履歴からABC系のコンテストを抽出"""
        contests = self.get_contest_history()
        abc_contests = []
        
        for contest in contests:
            name = contest['name']
            if 'AtCoder Beginner Contest' in name or 'ABC' in name:
                # ABC番号を抽出
                import re
                match = re.search(r'(\d+)', name)
                if match:
                    abc_num = int(match.group(1))
                    if 126 <= abc_num <= 406:  # 既存フォルダの範囲
                        abc_contests.append({
                            'contest_id': f'ABC{abc_num}',
                            'contest_name': name,
                            'date': contest['date'],
                            'url': contest['url']
                        })
        
        print(f"🎯 ABC対象コンテスト: {len(abc_contests)}件")
        return abc_contests
    
    def test_all_methods(self):
        """全ての手段をテスト"""
        print("🧪 全データ取得手段テスト開始")
        print("=" * 50)
        
        results = {}
        
        # 1. コンテスト履歴
        print("1️⃣ コンテスト履歴取得テスト...")
        contests = self.get_contest_history()
        results['contest_history'] = len(contests)
        
        # 2. ABC抽出
        print("\n2️⃣ ABC コンテスト抽出テスト...")
        abc_contests = self.get_abc_contests_from_history()
        results['abc_contests'] = len(abc_contests)
        
        if abc_contests:
            print("   📋 ABC コンテスト例:")
            for contest in abc_contests[:3]:
                print(f"   - {contest['contest_id']}: {contest['date']}")
        
        # 3. Vercel API
        print("\n3️⃣ Vercel API テスト...")
        vercel_data = self.get_submissions_from_vercel_api()
        results['vercel_api'] = 'success' if vercel_data else 'failed'
        
        # 4. AtCoder Problems 代替
        print("\n4️⃣ AtCoder Problems 代替手段テスト...")
        alt_data = self.get_atcoder_problems_alternative()
        results['atcoder_problems_alt'] = 'success' if alt_data else 'failed'
        
        print("\n" + "=" * 50)
        print("📊 テスト結果サマリー:")
        for method, result in results.items():
            print(f"   {method}: {result}")
        
        return results

def main():
    scraper = AtCoderDataScraper()
    results = scraper.test_all_methods()
    
    print("\n🎯 次のステップ:")
    if results.get('contest_history', 0) > 0:
        print("✅ コンテスト履歴から参加したABCを特定可能")
        print("✅ 各ABCコンテストページから個別に提出履歴を取得する方式を実装")
    
    if results.get('vercel_api') == 'success':
        print("✅ Vercel APIが利用可能 - 提出データの代替取得源として使用")
    
    if results.get('atcoder_problems_alt') == 'success':
        print("✅ AtCoder Problems 代替手段が利用可能")
    
    print("\n💡 推奨アプローチ:")
    print("1. コンテスト履歴からABC参加リストを作成")
    print("2. 各ABCの提出ページから個別データを取得")
    print("3. 既存フォルダ構造と照合してファイル更新")

if __name__ == "__main__":
    main()
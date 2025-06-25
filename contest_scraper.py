import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime
from config import ATCODER_USER_ID, SUPPORTED_LANGUAGES

class AtCoderContestScraper:
    def __init__(self, user_id=None):
        self.user_id = user_id or ATCODER_USER_ID
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_participated_abcs(self):
        """参加したABCコンテスト一覧を取得"""
        print(f"🏆 {self.user_id}の参加ABCコンテスト取得中...")
        
        try:
            url = f"https://atcoder.jp/users/{self.user_id}/history"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='table')
            
            abc_contests = []
            if table and table.find('tbody'):
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        contest_link = cols[1].find('a')
                        if contest_link:
                            contest_name = contest_link.get_text(strip=True)
                            contest_url = contest_link.get('href')
                            
                            # ABC番号を抽出
                            if 'AtCoder Beginner Contest' in contest_name:
                                match = re.search(r'(\d+)', contest_name)
                                if match:
                                    abc_num = int(match.group(1))
                                    if 126 <= abc_num <= 406:
                                        abc_contests.append({
                                            'contest_id': f'abc{abc_num}',
                                            'contest_name': contest_name,
                                            'contest_url': contest_url,
                                            'abc_num': abc_num
                                        })
            
            print(f"✅ 参加ABCコンテスト: {len(abc_contests)}件")
            return abc_contests
            
        except Exception as e:
            print(f"❌ 参加ABCコンテスト取得エラー: {e}")
            return []
    
    def get_contest_submissions(self, contest_id):
        """特定コンテストの提出履歴を取得"""
        print(f"📥 コンテスト {contest_id} の提出履歴取得中...")
        
        try:
            # コンテストの提出ページにアクセス
            url = f"https://atcoder.jp/contests/{contest_id}/submissions?f.User={self.user_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"   ❌ 提出ページアクセス失敗: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ログインが必要かチェック
            if 'Sign In' in soup.get_text():
                print(f"   ⚠️  コンテスト {contest_id}: ログインが必要")
                return []
            
            # 提出履歴テーブルを探す
            table = soup.find('table', class_='table')
            if not table:
                print(f"   ⚠️  コンテスト {contest_id}: 提出テーブルが見つかりません")
                return []
            
            submissions = []
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 6:
                        # 提出データを抽出
                        submission_time = cols[0].get_text(strip=True)
                        problem_link = cols[1].find('a')
                        language = cols[3].get_text(strip=True)
                        score = cols[4].get_text(strip=True)
                        status = cols[6].get_text(strip=True)
                        
                        if problem_link:
                            problem_url = problem_link.get('href')
                            problem_id = self._extract_problem_id(problem_url)
                            problem_title = problem_link.get_text(strip=True)
                            
                            submissions.append({
                                'submission_time': submission_time,
                                'problem_id': problem_id,
                                'problem_title': problem_title,
                                'language': language,
                                'score': score,
                                'status': status,
                                'problem_url': problem_url
                            })
            
            print(f"   ✅ コンテスト {contest_id}: {len(submissions)}件の提出を取得")
            return submissions
            
        except Exception as e:
            print(f"   ❌ コンテスト {contest_id} 提出取得エラー: {e}")
            return []
    
    def get_all_submissions(self):
        """全参加ABCコンテストの提出を取得"""
        print("🔄 全ABCコンテストの提出履歴取得開始")
        print("=" * 50)
        
        abc_contests = self.get_participated_abcs()
        all_submissions = []
        
        for contest in abc_contests:
            contest_id = contest['contest_id']
            submissions = self.get_contest_submissions(contest_id)
            
            # コンテスト情報を各提出に追加
            for submission in submissions:
                submission['contest_id'] = contest_id
                submission['contest_name'] = contest['contest_name']
                submission['abc_num'] = contest['abc_num']
            
            all_submissions.extend(submissions)
            time.sleep(1)  # レート制限対策
        
        print(f"\n🎉 全提出データ取得完了: {len(all_submissions)}件")
        return all_submissions
    
    def get_ac_submissions(self):
        """AC済み提出のみフィルタリング"""
        all_submissions = self.get_all_submissions()
        ac_submissions = [s for s in all_submissions if s['status'] == 'AC']
        
        print(f"✅ AC提出フィルタリング完了: {len(ac_submissions)}件")
        return ac_submissions
    
    def check_existing_folders(self):
        """既存のABCフォルダをチェック"""
        print("📁 既存ABCフォルダ確認中...")
        
        existing_folders = []
        for i in range(126, 407):
            folder_name = f'ABC{i}'
            if os.path.exists(folder_name):
                existing_folders.append({
                    'folder': folder_name,
                    'abc_num': i,
                    'files': self._check_folder_files(folder_name)
                })
        
        print(f"✅ 既存ABCフォルダ: {len(existing_folders)}件")
        return existing_folders
    
    def _check_folder_files(self, folder_path):
        """フォルダ内のファイル状況をチェック"""
        files_info = {}
        
        for problem in ['A', 'B', 'C', 'D']:
            for ext in ['.java', '.cpp', '.py']:
                file_path = os.path.join(folder_path, f'{problem}{ext}')
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if not content:
                                files_info[f'{problem}{ext}'] = 'empty'
                            elif len(content) < 50 and any(placeholder in content.lower() 
                                for placeholder in ['todo', 'placeholder', '//TODO', '# TODO']):
                                files_info[f'{problem}{ext}'] = 'placeholder'
                            else:
                                files_info[f'{problem}{ext}'] = 'has_content'
                    except:
                        files_info[f'{problem}{ext}'] = 'error'
        
        return files_info
    
    def organize_by_contest_and_problem(self, submissions):
        """コンテスト・問題別に整理"""
        organized = {}
        
        for submission in submissions:
            contest_id = submission.get('contest_id', 'unknown')
            problem_id = submission.get('problem_id', 'unknown')
            
            if contest_id not in organized:
                organized[contest_id] = {}
            
            if problem_id not in organized[contest_id]:
                organized[contest_id][problem_id] = []
            
            organized[contest_id][problem_id].append(submission)
        
        return organized
    
    def _extract_problem_id(self, url):
        """URLから問題IDを抽出"""
        if not url:
            return None
        
        # /contests/abc123/tasks/abc123_a のような形式
        match = re.search(r'/contests/([^/]+)/tasks/([^/]+)', url)
        if match:
            return match.group(2)  # abc123_a
        return None
    
    def _get_problem_letter(self, problem_id):
        """問題IDから問題文字(A,B,C,D)を抽出"""
        if not problem_id:
            return None
        
        # abc123_a -> A
        match = re.search(r'_([a-z])$', problem_id.lower())
        if match:
            return match.group(1).upper()
        return None
    
    def get_folder_name_from_contest_id(self, contest_id):
        """contest_id (abc378) から フォルダ名 (ABC378) を取得"""
        if contest_id.startswith('abc'):
            num = contest_id[3:]
            return f'ABC{num}'
        return None

def test_contest_scraper():
    """コンテスト個別取得のテスト"""
    print("🧪 コンテスト個別取得テスト開始")
    print("=" * 50)
    
    scraper = AtCoderContestScraper()
    
    # 1. 既存フォルダ確認
    print("1️⃣ 既存ABCフォルダ確認テスト...")
    existing_folders = scraper.check_existing_folders()
    print(f"   既存フォルダ数: {len(existing_folders)}件")
    
    if existing_folders:
        print("   📋 既存フォルダ例:")
        for folder in existing_folders[:3]:
            print(f"   - {folder['folder']}: {len(folder['files'])}ファイル")
            # 空ファイルがあるかチェック
            empty_files = [f for f, status in folder['files'].items() if status == 'empty']
            if empty_files:
                print(f"     空ファイル: {empty_files}")
    
    # 2. 参加ABCコンテスト一覧
    print("\n2️⃣ 参加ABCコンテスト取得テスト...")
    abc_contests = scraper.get_participated_abcs()
    print(f"   取得成功: {len(abc_contests)}件")
    
    if abc_contests:
        print("   📋 参加ABCコンテスト:")
        for contest in abc_contests[:5]:  # 最初の5件
            folder_name = scraper.get_folder_name_from_contest_id(contest['contest_id'])
            folder_exists = os.path.exists(folder_name) if folder_name else False
            print(f"   - {contest['contest_id']}: {contest['contest_name']} (フォルダ: {'✅' if folder_exists else '❌'})")
    
    # 3. 特定コンテストの提出履歴テスト
    if abc_contests:
        print(f"\n3️⃣ 特定コンテスト提出テスト ({abc_contests[0]['contest_id']})...")
        test_contest_id = abc_contests[0]['contest_id']
        submissions = scraper.get_contest_submissions(test_contest_id)
        print(f"   提出数: {len(submissions)}件")
        
        if submissions:
            print("   📋 提出例:")
            for sub in submissions[:3]:
                problem_letter = scraper._get_problem_letter(sub['problem_id'])
                print(f"   - 問題{problem_letter}: {sub['status']} ({sub['language']})")
    
    print("\n" + "=" * 50)
    print("🎯 コンテスト個別取得テスト完了")
    
    # 4. 既存フォルダとの対応関係
    if abc_contests and existing_folders:
        print("\n📊 既存フォルダと参加コンテストの対応関係:")
        participated_nums = [c['abc_num'] for c in abc_contests]
        existing_nums = [f['abc_num'] for f in existing_folders]
        
        # 参加したが既存フォルダがないもの
        missing_folders = [num for num in participated_nums if num not in existing_nums]
        if missing_folders:
            print(f"   📂 作成が必要なフォルダ: ABC{', ABC'.join(map(str, missing_folders))}")
        
        # 既存フォルダがあり参加もしているもの
        matched = [num for num in participated_nums if num in existing_nums]
        if matched:
            print(f"   🎯 更新対象フォルダ: {len(matched)}件")

if __name__ == "__main__":
    test_contest_scraper()
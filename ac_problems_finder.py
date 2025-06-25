import requests
import json
from datetime import datetime
from config import ATCODER_USER_ID

class AtCoderACFinder:
    def __init__(self, user_id=None):
        self.user_id = user_id or ATCODER_USER_ID
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_ac_problems_from_kenkoooo(self):
        """AtCoder Problems (kenkoooo.com) からAC済み問題を取得"""
        print(f"🔍 {self.user_id} のAC済み問題を取得中...")
        
        # 複数のエンドポイントを試行
        endpoints = [
            f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac?user={self.user_id}",
            f"https://kenkoooo.com/atcoder/atcoder-api/results?user={self.user_id}",
            f"https://kenkoooo.com/atcoder/resources/ac.json?user={self.user_id}",
            f"https://kenkoooo.com/atcoder/resources/user/{self.user_id}.json"
        ]
        
        for endpoint in endpoints:
            try:
                print(f"   試行中: {endpoint}")
                response = self.session.get(endpoint, timeout=15)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            print(f"   ✅ 成功: {len(data)}件のデータを取得")
                            return data
                        elif isinstance(data, dict):
                            print(f"   ✅ 成功: オブジェクト形式のデータを取得")
                            return data
                    except json.JSONDecodeError:
                        print(f"   ❌ JSON解析エラー")
                        continue
                else:
                    print(f"   ❌ ステータス: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ エラー: {e}")
                continue
        
        return None
    
    def get_submissions_from_alternative_api(self):
        """代替APIから提出データを取得"""
        print(f"🔄 代替APIから提出データを取得中...")
        
        # 別のAtCoder Problems APIを試行
        alternative_urls = [
            f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={self.user_id}&from_second=0",
            f"https://kenkoooo.com/atcoder/atcoder-api/user/submissions?user={self.user_id}",
            f"https://atcoder.jp/users/{self.user_id}/history/json"
        ]
        
        for url in alternative_urls:
            try:
                print(f"   試行中: {url}")
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ 成功: {len(data) if isinstance(data, list) else 1}件取得")
                        return data
                    except:
                        print(f"   ❌ JSON解析失敗")
                else:
                    print(f"   ❌ ステータス: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ エラー: {e}")
        
        return None
    
    def extract_abc_ac_problems(self, submissions_data):
        """提出データからABC問題のAC済み問題を抽出"""
        if not submissions_data:
            return []
        
        abc_ac_problems = []
        
        for submission in submissions_data:
            # データ形式の確認
            if isinstance(submission, dict):
                problem_id = submission.get('problem_id', '')
                result = submission.get('result', '')
                
                # ABC問題かつAC済みの問題を抽出
                if problem_id.startswith('abc') and result == 'AC':
                    # abc376_a -> ABC376, A の形式に変換
                    parts = problem_id.split('_')
                    if len(parts) == 2:
                        contest_part = parts[0]  # abc376
                        problem_part = parts[1]  # a
                        
                        # abc376 -> 376
                        contest_num = contest_part[3:]
                        problem_letter = problem_part.upper()
                        
                        if contest_num.isdigit():
                            abc_num = int(contest_num)
                            if 126 <= abc_num <= 406:  # 既存フォルダ範囲
                                abc_ac_problems.append({
                                    'contest_id': f'abc{contest_num}',
                                    'contest_folder': f'ABC{contest_num}',
                                    'problem_id': problem_id,
                                    'problem_letter': problem_letter,
                                    'abc_num': abc_num,
                                    'submission_data': submission
                                })
        
        # 重複を除去（同じ問題で複数のAC提出がある場合）
        unique_problems = {}
        for problem in abc_ac_problems:
            key = f"{problem['contest_folder']}_{problem['problem_letter']}"
            if key not in unique_problems:
                unique_problems[key] = problem
        
        return list(unique_problems.values())
    
    def check_folder_file_status(self, folder_name, problem_letter):
        """既存フォルダのファイル状況をチェック"""
        import os
        
        file_extensions = ['.java', '.cpp', '.py', '.c', '.cs']
        file_status = {}
        
        for ext in file_extensions:
            file_path = os.path.join(folder_name, f'{problem_letter}{ext}')
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if not content:
                            file_status[ext] = 'empty'
                        elif len(content) < 50:
                            file_status[ext] = 'placeholder'
                        else:
                            file_status[ext] = 'has_content'
                except:
                    file_status[ext] = 'error'
        
        return file_status
    
    def analyze_ac_problems(self):
        """AC済み問題の詳細分析"""
        print("🎯 AC済み問題詳細分析開始")
        print("=" * 60)
        
        # 1. AC済み問題データ取得
        submissions_data = self.get_ac_problems_from_kenkoooo()
        if not submissions_data:
            submissions_data = self.get_submissions_from_alternative_api()
        
        if not submissions_data:
            print("❌ AC済み問題データが取得できませんでした")
            return []
        
        # 2. ABC問題のAC済み問題を抽出
        abc_ac_problems = self.extract_abc_ac_problems(submissions_data)
        print(f"✅ ABC AC済み問題: {len(abc_ac_problems)}件")
        
        # 3. 詳細分析
        analysis_results = []
        
        for problem in abc_ac_problems:
            folder_name = problem['contest_folder']
            problem_letter = problem['problem_letter']
            
            # フォルダとファイルの状況確認
            import os
            folder_exists = os.path.exists(folder_name)
            
            file_status = {}
            if folder_exists:
                file_status = self.check_folder_file_status(folder_name, problem_letter)
            
            analysis_result = {
                **problem,
                'folder_exists': folder_exists,
                'file_status': file_status,
                'needs_update': folder_exists and any(status in ['empty', 'placeholder'] for status in file_status.values())
            }
            
            analysis_results.append(analysis_result)
        
        # 4. 結果の表示
        self.display_analysis_results(analysis_results)
        
        return analysis_results
    
    def display_analysis_results(self, results):
        """分析結果の表示"""
        print(f"\n📊 AC済み問題分析結果")
        print("=" * 60)
        
        # コンテスト別にグループ化
        by_contest = {}
        for result in results:
            contest = result['contest_folder']
            if contest not in by_contest:
                by_contest[contest] = []
            by_contest[contest].append(result)
        
        # 更新が必要なファイル
        needs_update = []
        
        for contest, problems in sorted(by_contest.items()):
            print(f"\n🏆 {contest}:")
            
            for problem in sorted(problems, key=lambda x: x['problem_letter']):
                letter = problem['problem_letter']
                folder_exists = problem['folder_exists']
                file_status = problem['file_status']
                
                status_icon = "✅" if folder_exists else "❌"
                print(f"   {status_icon} 問題{letter}: {problem['problem_id']}")
                
                if folder_exists:
                    # ファイル状況の詳細表示
                    for ext, status in file_status.items():
                        if status == 'empty':
                            print(f"      📝 {letter}{ext}: 空ファイル（更新対象）")
                            needs_update.append(f"{contest}/{letter}{ext}")
                        elif status == 'placeholder':
                            print(f"      📝 {letter}{ext}: プレースホルダー（更新対象）")
                            needs_update.append(f"{contest}/{letter}{ext}")
                        elif status == 'has_content':
                            print(f"      ✅ {letter}{ext}: コンテンツあり")
                else:
                    print(f"      ❌ フォルダが存在しません")
        
        # サマリー
        print(f"\n📈 サマリー:")
        print(f"   AC済み問題総数: {len(results)}件")
        print(f"   既存フォルダあり: {sum(1 for r in results if r['folder_exists'])}件")
        print(f"   更新が必要: {len(needs_update)}ファイル")
        
        if needs_update:
            print(f"\n🎯 更新対象ファイル例:")
            for file_path in needs_update[:10]:  # 最初の10件
                print(f"   - {file_path}")
            if len(needs_update) > 10:
                print(f"   ... 他{len(needs_update) - 10}件")

def main():
    finder = AtCoderACFinder()
    results = finder.analyze_ac_problems()
    
    print(f"\n💡 次のステップ:")
    print(f"   1. 上記の更新対象ファイルに実際のソースコードを取得")
    print(f"   2. AtCoderの提出履歴から該当するソースコードを抽出")
    print(f"   3. 空ファイルを実際のコードで更新")

if __name__ == "__main__":
    main()
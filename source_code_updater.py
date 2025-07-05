"""
AtCoder ソースコード自動更新ツール

【重要な問題解決記録】
日付: 2025-06-25
問題: BeautifulSoupでAtCoder提出ページからソースコード取得時に1行おきに空行が挿入される
解決: 生のHTMLから正規表現で直接抽出する方式に変更
結果: 正常な改行間隔でソースコードを取得可能

機能:
- AtCoder Problems APIからAC済み提出データを取得
- 各提出のソースコードをAtCoderサイトから抽出
- 空のJavaファイルを実際のACソースコードで更新
"""

import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime
from config import ATCODER_USER_ID

class SourceCodeUpdater:
    def __init__(self, user_id=None):
        self.user_id = user_id or ATCODER_USER_ID
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def format_timestamp(self, epoch_second):
        """Unix timestampを人間が読める形式に変換"""
        try:
            dt = datetime.fromtimestamp(epoch_second)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return 'N/A'
    
    def get_latest_contest_number(self):
        """ユーザーの提出データから最新のABCコンテスト番号を推定"""
        try:
            print("🔍 最新のコンテスト番号を推定中...")
            
            # ユーザーの全提出データから最新のABCを取得
            url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={self.user_id}&from_second=0"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"⚠️ 提出データ取得失敗、デフォルト値を使用")
                return 412  # 最新のデフォルト値に更新
            
            submissions = response.json()
            print(f"✅ 全提出データ取得: {len(submissions)}件")
            
            # ABCコンテストの最大番号を取得
            abc_numbers = []
            for submission in submissions:
                problem_id = submission.get('problem_id', '')
                if problem_id.startswith('abc'):
                    parts = problem_id.split('_')
                    if len(parts) == 2:
                        contest_part = parts[0]  # abc213
                        contest_num = contest_part[3:]  # 213
                        
                        if contest_num.isdigit():
                            abc_numbers.append(int(contest_num))
            
            if abc_numbers:
                latest_contest = max(abc_numbers)
                print(f"✅ 提出データから推定した最新コンテスト: ABC{latest_contest}")
                
                # 【修正】より現実的な推定値を設定
                # 2025年7月時点でABC412が最新なので、提出データから+30程度が妥当
                estimated_latest = latest_contest + 30
                print(f"✅ 安全マージン適用後: ABC{estimated_latest}")
                
                # 【追加】最低でもABC412以上を保証
                estimated_latest = max(estimated_latest, 412)
                print(f"✅ 最新保証適用後: ABC{estimated_latest}")
                
                return estimated_latest
            else:
                print(f"⚠️ ABCコンテストが見つからない、デフォルト値を使用")
                return 412  # 最新のデフォルト値
                
        except Exception as e:
            print(f"⚠️ 最新コンテスト推定エラー: {e}、デフォルト値を使用")
            return 412  # 最新のデフォルト値

    def get_ac_submissions_with_urls(self, min_contest=None):
        """AC済み提出をソースコードURLと共に取得（簡素化版）"""
        # 提出データから最新コンテストを推定
        if min_contest is None:
            latest_contest = self.get_latest_contest_number()
            # 過去100コンテスト分を対象とする
            min_contest = max(200, latest_contest - 100)
        
        print(f"🔍 {self.user_id} のAC済み提出データ（ABC{min_contest}以降）を取得中...")
        
        try:
            url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={self.user_id}&from_second=0"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ API取得失敗: {response.status_code}")
                return []
            
            submissions = response.json()
            print(f"✅ 全提出データ取得: {len(submissions)}件")
            
            # AC済み提出のみフィルタリング（範囲指定付き）
            ac_submissions = []
            for submission in submissions:
                if submission.get('result') == 'AC':
                    problem_id = submission.get('problem_id', '')
                    
                    # ABC形式の問題のみ対象
                    if problem_id.startswith('abc'):
                        # コンテスト番号を抽出
                        parts = problem_id.split('_')
                        if len(parts) == 2:
                            contest_part = parts[0]  # abc213
                            contest_num = contest_part[3:]  # 213
                            
                            if contest_num.isdigit() and int(contest_num) >= min_contest:
                                submission_id = submission.get('id')
                                contest_id = contest_part
                                submission_url = f"https://atcoder.jp/contests/{contest_id}/submissions/{submission_id}"
                                
                                submission['submission_url'] = submission_url
                                ac_submissions.append(submission)
            
            print(f"✅ ABC{min_contest}以降のAC済み提出: {len(ac_submissions)}件")
            
            # コンテスト別統計を表示
            contest_stats = {}
            for submission in ac_submissions:
                problem_id = submission['problem_id']
                contest_num = int(problem_id.split('_')[0][3:])
                contest_stats[contest_num] = contest_stats.get(contest_num, 0) + 1
            
            if contest_stats:
                min_contest_num = min(contest_stats.keys())
                max_contest_num = max(contest_stats.keys())
                
                print(f"📊 実際の対象範囲: ABC{min_contest_num} ～ ABC{max_contest_num}")
                print(f"📊 対象コンテスト数: {len(contest_stats)}個")
            
            return ac_submissions
        except Exception as e:
            print(f"❌ 提出データ取得エラー: {e}")
            return []
        
    def get_all_submissions_with_urls(self, min_contest=None):
        """すべての提出をソースコードURLと共に取得（AC・非AC含む）"""
        if min_contest is None:
            latest_contest = self.get_latest_contest_number()
            min_contest = max(200, latest_contest - 100)
        
        print(f"🔍 {self.user_id} のすべての提出データ（ABC{min_contest}以降）を取得中...")
        
        try:
            url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={self.user_id}&from_second=0"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ API取得失敗: {response.status_code}")
                return []
            
            submissions = response.json()
            print(f"✅ 全提出データ取得: {len(submissions)}件")
            
            # ABC形式の提出をフィルタリング（AC・非AC含む）
            abc_submissions = []
            for submission in submissions:
                problem_id = submission.get('problem_id', '')
                result = submission.get('result', '')
                
                # ABC形式の問題のみ対象
                if problem_id.startswith('abc'):
                    parts = problem_id.split('_')
                    if len(parts) == 2:
                        contest_part = parts[0]  # abc213
                        contest_num = contest_part[3:]  # 213
                        
                        if contest_num.isdigit() and int(contest_num) >= min_contest:
                            submission_id = submission.get('id')
                            contest_id = contest_part
                            submission_url = f"https://atcoder.jp/contests/{contest_id}/submissions/{submission_id}"
                            
                            submission['submission_url'] = submission_url
                            abc_submissions.append(submission)
            
            print(f"✅ ABC{min_contest}以降の提出: {len(abc_submissions)}件")
            
            # 結果別統計を表示
            result_stats = {}
            for submission in abc_submissions:
                result = submission.get('result', 'Unknown')
                result_stats[result] = result_stats.get(result, 0) + 1
            
            print(f"📊 結果別統計:")
            for result, count in sorted(result_stats.items()):
                print(f"  {result}: {count}件")
            
            return abc_submissions
            
        except Exception as e:
            print(f"❌ 提出データ取得エラー: {e}")
            return []

    def create_missing_files_in_range(self, min_contest=None):
        """指定範囲のすべての提出問題の空ファイルを自動作成（AC・非AC含む）"""
        if min_contest is None:
            latest_contest = self.get_latest_contest_number()
            min_contest = max(200, latest_contest - 100)

        print(f"📁 ABC{min_contest}以降の空ファイル自動作成（AC・非AC含む）")
        print("=" * 60)
        
        # すべての提出データを取得
        all_submissions = self.get_all_submissions_with_urls(min_contest)
        if not all_submissions:
            print("❌ 提出データが取得できませんでした")
            return 0
        
        # 問題ID別に最新の提出を取得
        latest_submissions = {}
        for submission in all_submissions:
            problem_id = submission['problem_id']
            epoch_second = submission.get('epoch_second', 0)
            
            if problem_id not in latest_submissions or epoch_second > latest_submissions[problem_id].get('epoch_second', 0):
                latest_submissions[problem_id] = submission
    
        created_folders = set()
        created_files = []
        
        for problem_id, submission in latest_submissions.items():
            parts = problem_id.split('_')
            
            if len(parts) == 2:
                contest_part = parts[0]  # abc213
                problem_part = parts[1]  # a
                result = submission.get('result', '')
                
                contest_num = contest_part[3:]
                if contest_num.isdigit():
                    folder_name = f'ABC{contest_num}'
                    problem_letter = problem_part.upper()
                    
                    # ファイル名を結果に応じて決定
                    if result == 'AC':
                        file_name = f'{problem_letter}.java'
                    else:
                        file_name = f'{problem_letter}_no.java'
                    
                    file_path = os.path.join(folder_name, file_name)
                    
                    # フォルダ作成
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name, exist_ok=True)
                        created_folders.add(folder_name)
                        print(f"📂 フォルダ作成: {folder_name}")
                    
                    # ファイルが存在しない場合のみ作成
                    if not os.path.exists(file_path):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('')  # 空ファイル作成
                        created_files.append(file_path)
                        
                        # 結果に応じてメッセージを変更
                        if result == 'AC':
                            print(f"📝 AC問題ファイル作成: {file_path}")
                        else:
                            print(f"📝 非AC問題ファイル作成: {file_path} (結果: {result})")
        
        print(f"\n📈 作成結果:")
        print(f"  フォルダ: {len(created_folders)}個")
        print(f"  ファイル: {len(created_files)}個")
        
        return len(created_files)

    def update_all_empty_files_in_range(self, min_contest=None, max_updates=1000):
        """指定範囲の全ての空ファイルを更新（AC・非AC含む）"""
        if min_contest is None:
            latest_contest = self.get_latest_contest_number()
            min_contest = max(200, latest_contest - 100)

        print(f"🔄 ABC{min_contest}以降の空ファイル一括更新開始（AC・非AC含む）")
        print("=" * 70)
        
        # すべての提出データを取得
        all_submissions = self.get_all_submissions_with_urls(min_contest)
        if not all_submissions:
            print("❌ 提出データが取得できませんでした")
            return
        
        # 問題ID別に最新の提出を取得
        latest_submissions = {}
        for submission in all_submissions:
            problem_id = submission['problem_id']
            epoch_second = submission.get('epoch_second', 0)
            
            if problem_id not in latest_submissions or epoch_second > latest_submissions[problem_id].get('epoch_second', 0):
                latest_submissions[problem_id] = submission
    
        print(f"📊 ユニーク問題数: {len(latest_submissions)}件")
        
        # 結果別統計
        result_stats = {}
        for submission in latest_submissions.values():
            result = submission.get('result', 'Unknown')
            result_stats[result] = result_stats.get(result, 0) + 1
        
        print(f"📊 結果別統計:")
        for result, count in sorted(result_stats.items()):
            print(f"  {result}: {count}件")
        
        # 更新処理
        updated_count = 0
        for problem_id, submission in latest_submissions.items():
            if updated_count >= max_updates:
                print(f"⚠️  制限により{max_updates}件で停止")
                break
            
            # 問題IDからフォルダとファイルを特定
            parts = problem_id.split('_')
            if len(parts) != 2:
                continue
                
            contest_part = parts[0]  # abc213
            problem_part = parts[1]  # a
            result = submission.get('result', '')
            
            contest_num = contest_part[3:]
            if not contest_num.isdigit():
                continue
            
            folder_name = f'ABC{contest_num}'
            problem_letter = problem_part.upper()
            
            # ファイル名を結果に応じて決定
            if result == 'AC':
                file_name = f'{problem_letter}.java'
            else:
                file_name = f'{problem_letter}_no.java'
            
            file_path = os.path.join(folder_name, file_name)
            
            # フォルダとファイルの存在確認
            if not os.path.exists(folder_name) or not os.path.exists(file_path):
                continue
            
            print(f"\n🎯 処理中: {problem_id} ({result}) -> {file_path}")
            
            # ソースコード取得
            source_code = self.get_source_code_from_url(submission['submission_url'])
            if not source_code:
                print(f"   ⚠️  ソースコード取得失敗、スキップ")
                continue
            
            # ファイル更新
            if self.update_empty_file_with_result(file_path, source_code, submission):
                updated_count += 1
                print(f"   🎉 更新成功 ({updated_count})")
        
        print(f"\n📈 更新完了: {updated_count}ファイル")

    def get_source_code_from_url(self, submission_url):
        """
        提出URLからソースコードを取得（生HTML解析版）
        
        【問題】BeautifulSoupのget_text()を使用すると、AtCoderの提出ページから
               ソースコードを取得する際に1行おきに空行が挿入される問題が発生
        
        【原因】BeautifulSoupがHTMLの改行構造を誤解釈し、内部的に改行を2倍化
               していた可能性
        
        【解決策】生のHTMLテキストから正規表現で直接<pre>要素の中身を抽出することで
                 元のAtCoderコードの改行間隔をそのまま保持
        
        【修正前】BeautifulSoup + get_text() → 1行おきに空行
        【修正後】正規表現 + 生HTML抽出 → 正常な改行間隔
        """
        try:
            print(f"   📥 ソースコード取得: {submission_url}")
            
            response = self.session.get(submission_url, timeout=10)
            if response.status_code != 200:
                print(f"   ❌ ソースコード取得失敗: {response.status_code}")
                return None
            
            # 【修正】生のHTMLテキストから直接抽出（BeautifulSoup使用せず）
            html_content = response.text
            
            # 正規表現でpre要素の中身を抽出
            import re
            pattern = r'<pre[^>]*id="submission-code"[^>]*>(.*?)</pre>'
            match = re.search(pattern, html_content, re.DOTALL)
            
            if match:
                print(f"   ✅ 正規表現でソースコード発見")
                
                source_code = match.group(1)
                
                # HTMLエンティティをデコード
                import html
                source_code = html.unescape(source_code)
                
                # 先頭・末尾の空白を除去
                source_code = source_code.strip()
                
                print(f"   📊 抽出結果: {len(source_code)}文字")
                
                # 改行を統一
                source_code = source_code.replace('\r\n', '\n').replace('\r', '\n')
                
                lines = source_code.split('\n')
                print(f"   📊 行数: {len(lines)}行")
                
                return source_code
            else:
                print(f"   ⚠️  正規表現でソースコードが見つかりません")
                return None
            
        except Exception as e:
            print(f"   ❌ ソースコード取得エラー: {e}")
            return None
    
    def update_empty_file(self, file_path, source_code, problem_info):
        """空ファイルを実際のソースコードで更新（public class版）"""
        try:
            if not os.path.exists(file_path):
                print(f"   ❌ ファイルが存在しません: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read().strip()
            
            # 空ファイルまたはプレースホルダーの場合のみ更新
            if current_content and len(current_content) > 50:
                print(f"   ⚠️  既にコンテンツあり、スキップ: {file_path}")
                return False
            
            # ファイルパスから情報を取得
            filename = os.path.basename(file_path)
            problem_letter = filename.split('.')[0]  # A.java → A
            directory = os.path.basename(os.path.dirname(file_path))  # ABC213
            
            # package文をフォルダ名と同じ大文字に変更
            package_name = directory  # ABC213 (大文字のまま)
            package_statement = f"package {package_name};\n\n"
            
            # 【修正】public class Main → public class [問題名] に変更
            if 'public class Main' in source_code:
                source_code = source_code.replace('public class Main', f'public class {problem_letter}')
                print(f"   🔄 クラス名変更: public class Main → public class {problem_letter}")
            elif 'class Main' in source_code:
                source_code = source_code.replace('class Main', f'public class {problem_letter}')
                print(f"   🔄 クラス名変更: class Main → public class {problem_letter}")
            
            # 実行時間の処理
            epoch_second = problem_info.get('epoch_second', 0)
            formatted_date = self.format_timestamp(epoch_second)
            execution_time = problem_info.get('execution_time', 0)
            execution_time_str = f"{execution_time}ms" if execution_time else "N/A"
            
            # ソースコードを書き込み
            with open(file_path, 'w', encoding='utf-8') as f:
                header = f"// AC済み問題: {problem_info['problem_id']}\n"
                header += f"// 提出日時: {formatted_date}\n"
                header += f"// 実行時間: {execution_time_str}\n"
                header += f"// 注意: AtCoderは public class Main だが、IDE用に public class {problem_letter} に変更\n\n"
                
                # package文 + ヘッダー + ソースコード
                f.write(header + package_statement + source_code)
        
            print(f"   ✅ ファイル更新完了: {file_path}")
            print(f"   📦 package追加: {package_name}")
            print(f"   ⚡ 実行時間: {execution_time_str}")
            return True
        
        except Exception as e:
            print(f"   ❌ ファイル更新エラー: {e}")
            return False

    def update_empty_file_with_result(self, file_path, source_code, problem_info):
        """空ファイルを実際のソースコードで更新（結果対応版）"""
        try:
            if not os.path.exists(file_path):
                print(f"   ❌ ファイルが存在しません: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read().strip()
            
            # 空ファイルまたはプレースホルダーの場合のみ更新
            if current_content and len(current_content) > 50:
                print(f"   ⚠️  既にコンテンツあり、スキップ: {file_path}")
                return False
            
            # ファイルパスから情報を取得
            filename = os.path.basename(file_path)
            file_parts = filename.split('_')
            
            if len(file_parts) == 1:
                # A.java の場合
                problem_letter = file_parts[0].split('.')[0]
                is_ac = True
            else:
                # A_no.java の場合
                problem_letter = file_parts[0]
                is_ac = False
            
            directory = os.path.basename(os.path.dirname(file_path))  # ABC213
            
            # package文をフォルダ名と同じ大文字に変更
            package_name = directory  # ABC213 (大文字のまま)
            package_statement = f"package {package_name};\n\n"
            
            # クラス名変更
            if 'public class Main' in source_code:
                source_code = source_code.replace('public class Main', f'public class {problem_letter}')
                print(f"   🔄 クラス名変更: public class Main → public class {problem_letter}")
            elif 'class Main' in source_code:
                source_code = source_code.replace('class Main', f'public class {problem_letter}')
                print(f"   🔄 クラス名変更: class Main → public class {problem_letter}")
            
            # 実行時間・結果の処理
            epoch_second = problem_info.get('epoch_second', 0)
            formatted_date = self.format_timestamp(epoch_second)
            execution_time = problem_info.get('execution_time', 0)
            execution_time_str = f"{execution_time}ms" if execution_time else "N/A"
            result = problem_info.get('result', 'Unknown')
            
            # ソースコードを書き込み
            with open(file_path, 'w', encoding='utf-8') as f:
                if is_ac:
                    header = f"// AC済み問題: {problem_info['problem_id']}\n"
                    header += f"// 提出日時: {formatted_date}\n"
                    header += f"// 実行時間: {execution_time_str}\n"
                    header += f"// 注意: AtCoderは public class Main だが、IDE用に public class {problem_letter} に変更\n\n"
                else:
                    header = f"// 未AC問題: {problem_info['problem_id']}\n"
                    header += f"// 提出日時: {formatted_date}\n"
                    header += f"// 結果: {result}\n"
                    header += f"// 実行時間: {execution_time_str}\n"
                    header += f"// 注意: AtCoderは public class Main だが、IDE用に public class {problem_letter} に変更\n\n"
                
                # package文 + ヘッダー + ソースコード
                f.write(header + package_statement + source_code)
        
            print(f"   ✅ ファイル更新完了: {file_path}")
            print(f"   📦 package追加: {package_name}")
            print(f"   📊 結果: {result}")
            print(f"   ⚡ 実行時間: {execution_time_str}")
            return True
        
        except Exception as e:
            print(f"   ❌ ファイル更新エラー: {e}")
            return False

    def update_all_empty_files(self, max_updates=10):
        """全ての空ファイルを更新"""
        print("🔄 空ファイル一括更新開始")
        print("=" * 60)
        
        # AC済み提出データを取得
        ac_submissions = self.get_ac_submissions_with_urls()
        if not ac_submissions:
            print("❌ AC済み提出データが取得できませんでした")
            return
        
        # 問題ID別に最新の提出を取得
        latest_submissions = {}
        for submission in ac_submissions:
            problem_id = submission['problem_id']
            epoch_second = submission.get('epoch_second', 0)
            
            if problem_id not in latest_submissions or epoch_second > latest_submissions[problem_id].get('epoch_second', 0):
                latest_submissions[problem_id] = submission
        
        print(f"📊 ユニーク問題数: {len(latest_submissions)}件")
        
        # 更新処理
        updated_count = 0
        for problem_id, submission in latest_submissions.items():
            if updated_count >= max_updates:
                print(f"⚠️  制限により{max_updates}件で停止")
                break
            
            # 問題IDからフォルダとファイルを特定
            parts = problem_id.split('_')
            if len(parts) != 2:
                continue
                
            contest_part = parts[0]  # abc213
            problem_part = parts[1]  # a
            
            # abc213 -> ABC213
            contest_num = contest_part[3:]
            if not contest_num.isdigit():
                continue
            
            folder_name = f'ABC{contest_num}'
            problem_letter = problem_part.upper()
            file_path = os.path.join(folder_name, f'{problem_letter}.java')
            
            # フォルダとファイルの存在確認
            if not os.path.exists(folder_name) or not os.path.exists(file_path):
                continue
            
            print(f"\n🎯 処理中: {problem_id} -> {file_path}")
            
            # ソースコード取得
            source_code = self.get_source_code_from_url(submission['submission_url'])
            if not source_code:
                print(f"   ⚠️  ソースコード取得失敗、スキップ")
                continue
            
            # ファイル更新
            if self.update_empty_file(file_path, source_code, submission):
                updated_count += 1
                print(f"   🎉 更新成功 ({updated_count}/{max_updates})")
            
            # レート制限対策
            time.sleep(2)
        
        print(f"\n📈 更新完了: {updated_count}ファイル")
    
    def debug_memory_info(self):
        """メモリ情報のデバッグ"""
        print("🧠 メモリ情報デバッグ")
        print("=" * 40)
        
        # AC済み提出データを取得
        ac_submissions = self.get_ac_submissions_with_urls()
        
        print(f"📊 メモリ情報の分析:")
        memory_available = 0
        memory_total = 0
        
        for submission in ac_submissions[:20]:  # 最初の20件で分析
            problem_id = submission['problem_id']
            memory = submission.get('memory', 0)
            execution_time = submission.get('execution_time', 0)
            
            if memory and memory > 0:
                memory_available += 1
                print(f"✅ {problem_id}: {memory}KB, {execution_time}ms")
            else:
                print(f"❌ {problem_id}: メモリ情報なし, {execution_time}ms")
            
            memory_total += 1
        
        print(f"\n📈 統計:")
        print(f"  メモリ情報あり: {memory_available}/{memory_total} 件")
        print(f"  メモリ情報なし: {memory_total - memory_available}/{memory_total} 件")

    def test_single_update():
        """単一ファイル更新のテスト"""
        print("🧪 単一ファイル更新テスト")
        print("=" * 40)
        
        updater = SourceCodeUpdater()
        
        test_problem_id = 'abc213_a'
        test_folder = 'ABC213'
        test_file = 'A.java'
        test_file_path = os.path.join(test_folder, test_file)
        
        print(f"🎯 テスト対象: {test_problem_id}")
        print(f"📁 ファイルパス: {test_file_path}")
        
        if not os.path.exists(test_file_path):
            print(f"❌ テストファイルが存在しません: {test_file_path}")
            return
        
        # AC済み提出から該当問題を検索
        ac_submissions = updater.get_ac_submissions_with_urls()
        target_submission = None
        
        for submission in ac_submissions:
            if submission['problem_id'] == test_problem_id:
                target_submission = submission
                break
        
        if not target_submission:
            print(f"❌ {test_problem_id} のAC提出が見つかりません")
            return
        
        print(f"✅ AC提出発見: {target_submission['submission_url']}")
        
        # ソースコード取得・更新
        source_code = updater.get_source_code_from_url(target_submission['submission_url'])
        if source_code:
            success = updater.update_empty_file(test_file_path, source_code, target_submission)
            if success:
                print(f"🎉 テスト成功: {test_file_path} を更新しました")
            else:
                print(f"⚠️  テスト完了: ファイルは既にコンテンツがあります")
        else:
            print(f"❌ テスト失敗: ソースコード取得できませんでした")

    def test_latest_contest():
        """最新コンテスト取得のテスト"""
        print("🔍 最新コンテスト取得テスト")
        print("=" * 50)
        
        updater = SourceCodeUpdater()
        
        # 1. 最新コンテスト番号の取得
        latest_contest = updater.get_latest_contest_number()
        print(f"\n📊 推定結果:")
        print(f"  最新コンテスト: ABC{latest_contest}")
        
        # 2. 実際の提出データから詳細確認
        print(f"\n🔍 提出データから詳細分析:")
        
        try:
            url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={updater.user_id}&from_second=0"
            response = updater.session.get(url, timeout=30)
            
            if response.status_code == 200:
                submissions = response.json()
                
                # ABC提出のみ抽出
                abc_submissions = []
                for submission in submissions:
                    problem_id = submission.get('problem_id', '')
                    if problem_id.startswith('abc'):
                        parts = problem_id.split('_')
                        if len(parts) == 2:
                            contest_num = parts[0][3:]
                            if contest_num.isdigit():
                                abc_submissions.append({
                                    'contest_num': int(contest_num),
                                    'problem_id': problem_id,
                                    'submission_date': updater.format_timestamp(submission.get('epoch_second', 0)),
                                    'result': submission.get('result', ''),
                                    'epoch_second': submission.get('epoch_second', 0)
                                })
                
                # コンテスト番号でソート
                abc_submissions.sort(key=lambda x: x['contest_num'], reverse=True)
                
                print(f"📈 ABC提出統計:")
                print(f"  総ABC提出数: {len(abc_submissions)}件")
                
                if abc_submissions:
                    latest_submission = abc_submissions[0]
                    print(f"  最新提出コンテスト: ABC{latest_submission['contest_num']}")
                    print(f"  最新提出日時: {latest_submission['submission_date']}")
                    print(f"  最新提出問題: {latest_submission['problem_id']}")
                    
                    # 最新10コンテストの提出状況
                    print(f"\n🏆 最新10コンテストの提出状況:")
                    contest_stats = {}
                    for sub in abc_submissions:
                        contest_num = sub['contest_num']
                        if contest_num not in contest_stats:
                            contest_stats[contest_num] = {'AC': 0, 'total': 0}
                        
                        contest_stats[contest_num]['total'] += 1
                        if sub['result'] == 'AC':
                            contest_stats[contest_num]['AC'] += 1
                    
                    # 最新10コンテストを表示
                    latest_contests = sorted(contest_stats.keys(), reverse=True)[:10]
                    for contest_num in latest_contests:
                        stats = contest_stats[contest_num]
                        print(f"  ABC{contest_num}: AC {stats['AC']}/{stats['total']} 件")
                    
                    # 現在時刻との比較
                    from datetime import datetime
                    current_time = datetime.now()
                    print(f"\n⏰ 現在時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # 最新ABC番号の推定
                    max_contest = max(contest_stats.keys())
                    print(f"📊 あなたの提出から推定される最新: ABC{max_contest}")
                    
                    # 【修正】より現実的な推定範囲
                    print(f"🎯 2025年7月時点での実際の最新: ABC412")
                    print(f"🎯 推定範囲: ABC{max_contest + 20}～ABC{max_contest + 40}")
                    
                else:
                    print("❌ ABC提出データが見つかりませんでした")
                    
        except Exception as e:
            print(f"❌ エラー: {e}")

    def get_contest_range_input(self):
        """コンテスト範囲の入力を取得"""
        print("📋 コンテスト範囲を指定してください")
        print("=" * 40)
        
        try:
            # 開始コンテスト
            start_input = input("開始コンテスト番号（例: 200）: ").strip()
            if not start_input.isdigit():
                print("❌ 無効な開始コンテスト番号です")
                return None, None
            start_contest = int(start_input)
            
            # 終了コンテスト
            end_input = input("終了コンテスト番号（例: 210）: ").strip()
            if not end_input.isdigit():
                print("❌ 無効な終了コンテスト番号です")
                return None, None
            end_contest = int(end_input)
            
            # 範囲チェック
            if start_contest > end_contest:
                print("❌ 開始コンテストが終了コンテストより大きいです")
                return None, None
            
            if end_contest - start_contest > 50:
                print("❌ 範囲が大きすぎます（最大50コンテスト）")
                return None, None
            
            print(f"✅ 範囲設定: ABC{start_contest} ～ ABC{end_contest}")
            return start_contest, end_contest
            
        except ValueError:
            print("❌ 無効な入力です")
            return None, None

    def get_submissions_by_contest_range(self, start_contest, end_contest):
        """指定コンテスト範囲の提出データを取得"""
        print(f"🔍 ABC{start_contest}～ABC{end_contest}の提出データを取得中...")
        
        try:
            url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={self.user_id}&from_second=0"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ API取得失敗: {response.status_code}")
                return []
            
            submissions = response.json()
            print(f"✅ 全提出データ取得: {len(submissions)}件")
            
            # 指定範囲のABC提出をフィルタリング
            range_submissions = []
            for submission in submissions:
                problem_id = submission.get('problem_id', '')
                
                # ABC形式の問題のみ対象
                if problem_id.startswith('abc'):
                    parts = problem_id.split('_')
                    if len(parts) == 2:
                        contest_part = parts[0]  # abc213
                        contest_num = contest_part[3:]  # 213
                        
                        if contest_num.isdigit():
                            contest_number = int(contest_num)
                            # 指定範囲内かチェック
                            if start_contest <= contest_number <= end_contest:
                                submission_id = submission.get('id')
                                contest_id = contest_part
                                submission_url = f"https://atcoder.jp/contests/{contest_id}/submissions/{submission_id}"
                                
                                submission['submission_url'] = submission_url
                                range_submissions.append(submission)
            
            print(f"✅ ABC{start_contest}～ABC{end_contest}の提出: {len(range_submissions)}件")
            
            # 結果別統計を表示
            result_stats = {}
            for submission in range_submissions:
                result = submission.get('result', 'Unknown')
                result_stats[result] = result_stats.get(result, 0) + 1
            
            print(f"📊 結果別統計:")
            for result, count in sorted(result_stats.items()):
                print(f"  {result}: {count}件")
            
            # コンテスト別統計を表示
            contest_stats = {}
            for submission in range_submissions:
                problem_id = submission['problem_id']
                contest_num = int(problem_id.split('_')[0][3:])
                if contest_num not in contest_stats:
                    contest_stats[contest_num] = {'AC': 0, 'total': 0}
                
                contest_stats[contest_num]['total'] += 1
                if submission.get('result') == 'AC':
                    contest_stats[contest_num]['AC'] += 1
            
            print(f"📊 コンテスト別統計:")
            for contest_num in sorted(contest_stats.keys()):
                stats = contest_stats[contest_num]
                print(f"  ABC{contest_num}: AC {stats['AC']}/{stats['total']} 件")
        
            return range_submissions

        except Exception as e:
            print(f"❌ 提出データ取得エラー: {e}")
            return []

    def create_files_by_contest_range(self, start_contest, end_contest):
        """指定コンテスト範囲の空ファイルを作成"""
        print(f"📁 ABC{start_contest}～ABC{end_contest}の空ファイル作成")
        print("=" * 60)
        
        # 指定範囲の提出データを取得
        range_submissions = self.get_submissions_by_contest_range(start_contest, end_contest)
        if not range_submissions:
            print("❌ 指定範囲の提出データが取得できませんでした")
            return 0
        
        # 問題ID別に最新の提出を取得
        latest_submissions = {}
        for submission in range_submissions:
            problem_id = submission['problem_id']
            epoch_second = submission.get('epoch_second', 0)
            
            if problem_id not in latest_submissions or epoch_second > latest_submissions[problem_id].get('epoch_second', 0):
                latest_submissions[problem_id] = submission
    
        created_folders = set()
        created_files = []
        
        for problem_id, submission in latest_submissions.items():
            parts = problem_id.split('_')
            
            if len(parts) == 2:
                contest_part = parts[0]  # abc213
                problem_part = parts[1]  # a
                result = submission.get('result', '')
                
                contest_num = contest_part[3:]
                if contest_num.isdigit():
                    folder_name = f'ABC{contest_num}'
                    problem_letter = problem_part.upper()
                    
                    # ファイル名を結果に応じて決定
                    if result == 'AC':
                        file_name = f'{problem_letter}.java'
                    else:
                        file_name = f'{problem_letter}_no.java'
                    
                    file_path = os.path.join(folder_name, file_name)
                    
                    # フォルダ作成
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name, exist_ok=True)
                        created_folders.add(folder_name)
                        print(f"📂 フォルダ作成: {folder_name}")
                    
                    # ファイルが存在しない場合のみ作成
                    if not os.path.exists(file_path):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('')  # 空ファイル作成
                        created_files.append(file_path)
                        
                        # 結果に応じてメッセージを変更
                        if result == 'AC':
                            print(f"📝 AC問題ファイル作成: {file_path}")
                        else:
                            print(f"📝 非AC問題ファイル作成: {file_path} (結果: {result})")
    
        print(f"\n📈 作成結果:")
        print(f"  フォルダ: {len(created_folders)}個")
        print(f"  ファイル: {len(created_files)}個")
        print(f"  対象コンテスト: ABC{start_contest}～ABC{end_contest}")
        
        return len(created_files)

    def update_files_by_contest_range(self, start_contest, end_contest, max_updates=1000):
        """指定コンテスト範囲のファイルを更新"""
        print(f"🔄 ABC{start_contest}～ABC{end_contest}のファイル更新開始")
        print("=" * 70)
        
        # 指定範囲の提出データを取得
        range_submissions = self.get_submissions_by_contest_range(start_contest, end_contest)
        if not range_submissions:
            print("❌ 指定範囲の提出データが取得できませんでした")
            return
        
        # 問題ID別に最新の提出を取得
        latest_submissions = {}
        for submission in range_submissions:
            problem_id = submission['problem_id']
            epoch_second = submission.get('epoch_second', 0)
            
            if problem_id not in latest_submissions or epoch_second > latest_submissions[problem_id].get('epoch_second', 0):
                latest_submissions[problem_id] = submission
    
        print(f"📊 ユニーク問題数: {len(latest_submissions)}件")
        
        # 結果別統計
        result_stats = {}
        for submission in latest_submissions.values():
            result = submission.get('result', 'Unknown')
            result_stats[result] = result_stats.get(result, 0) + 1
        
        print(f"📊 結果別統計:")
        for result, count in sorted(result_stats.items()):
            print(f"  {result}: {count}件")
        
        # 更新処理
        updated_count = 0
        for problem_id, submission in latest_submissions.items():
            if updated_count >= max_updates:
                print(f"⚠️  制限により{max_updates}件で停止")
                break
            
            # 問題IDからフォルダとファイルを特定
            parts = problem_id.split('_')
            if len(parts) != 2:
                continue
                
            contest_part = parts[0]  # abc213
            problem_part = parts[1]  # a
            result = submission.get('result', '')
            
            contest_num = contest_part[3:]
            if not contest_num.isdigit():
                continue
            
            folder_name = f'ABC{contest_num}'
            problem_letter = problem_part.upper()
            
            # ファイル名を結果に応じて決定
            if result == 'AC':
                file_name = f'{problem_letter}.java'
            else:
                file_name = f'{problem_letter}_no.java'
            
            file_path = os.path.join(folder_name, file_name)
            
            # フォルダとファイルの存在確認
            if not os.path.exists(folder_name) or not os.path.exists(file_path):
                continue
            
            print(f"\n🎯 処理中: {problem_id} ({result}) -> {file_path}")
            
            # ソースコード取得
            source_code = self.get_source_code_from_url(submission['submission_url'])
            if not source_code:
                print(f"   ⚠️  ソースコード取得失敗、スキップ")
                continue
            
            # ファイル更新
            if self.update_empty_file_with_result(file_path, source_code, submission):
                updated_count += 1
                print(f"   🎉 更新成功 ({updated_count})")
        
        print(f"\n📈 更新完了: {updated_count}ファイル")
        print(f"📁 対象範囲: ABC{start_contest}～ABC{end_contest}")

    def analyze_contest_submissions(self, min_contest=None):
        """コンテスト別の提出状況を詳細分析"""
        if min_contest is None:
            latest_contest = self.get_latest_contest_number()
            min_contest = max(200, latest_contest - 100)
        
        print(f"📊 ABC{min_contest}以降のコンテスト別提出状況分析")
        print("=" * 70)
        
        # すべての提出データを取得
        all_submissions = self.get_all_submissions_with_urls(min_contest)
        if not all_submissions:
            print("❌ 提出データが取得できませんでした")
            return
        
        # コンテスト別に分析
        contest_analysis = {}
        
        for submission in all_submissions:
            problem_id = submission['problem_id']
            parts = problem_id.split('_')
            
            if len(parts) == 2:
                contest_part = parts[0]  # abc213
                problem_part = parts[1]  # a
                result = submission.get('result', 'Unknown')
                
                contest_num = contest_part[3:]
                if contest_num.isdigit():
                    contest_number = int(contest_num)
                    
                    if contest_number not in contest_analysis:
                        contest_analysis[contest_number] = {
                            'AC': 0,
                            'WA': 0,
                            'TLE': 0,
                            'RE': 0,
                            'CE': 0,
                            'MLE': 0,
                            'OLE': 0,
                            'IE': 0,
                            'WJ': 0,
                            'Other': 0,
                            'total': 0,
                            'problems': set(),
                            'ac_problems': set(),
                            'submissions_detail': []
                        }
                    
                    # 結果別カウント
                    if result == 'AC':
                        contest_analysis[contest_number]['AC'] += 1
                        contest_analysis[contest_number]['ac_problems'].add(problem_part.upper())
                    elif result == 'WA':
                        contest_analysis[contest_number]['WA'] += 1
                    elif result == 'TLE':
                        contest_analysis[contest_number]['TLE'] += 1
                    elif result == 'RE':
                        contest_analysis[contest_number]['RE'] += 1
                    elif result == 'CE':
                        contest_analysis[contest_number]['CE'] += 1
                    elif result == 'MLE':
                        contest_analysis[contest_number]['MLE'] += 1
                    elif result == 'OLE':
                        contest_analysis[contest_number]['OLE'] += 1
                    elif result == 'IE':
                        contest_analysis[contest_number]['IE'] += 1
                    elif result == 'WJ':
                        contest_analysis[contest_number]['WJ'] += 1
                    else:
                        contest_analysis[contest_number]['Other'] += 1
                    
                    contest_analysis[contest_number]['total'] += 1
                    contest_analysis[contest_number]['problems'].add(problem_part.upper())
                    
                    # 詳細情報を保存
                    contest_analysis[contest_number]['submissions_detail'].append({
                        'problem': problem_part.upper(),
                        'result': result,
                        'submission_date': self.format_timestamp(submission.get('epoch_second', 0)),
                        'execution_time': submission.get('execution_time', 0)
                    })
        
        # 結果表示
        print(f"📈 コンテスト別提出状況（ABC{min_contest}以降）")
        print("-" * 70)
        
        # ソート（コンテスト番号順）
        sorted_contests = sorted(contest_analysis.keys())
        
        total_contests = len(sorted_contests)
        total_ac_problems = 0
        total_other_problems = 0
        
        for contest_num in sorted_contests:
            stats = contest_analysis[contest_num]
            ac_count = stats['AC']
            other_count = stats['total'] - stats['AC']
            unique_problems = len(stats['problems'])
            ac_problems = len(stats['ac_problems'])
            
            total_ac_problems += ac_count
            total_other_problems += other_count
            
            # 基本情報
            print(f"ABC{contest_num:03d}: AC {ac_count:2d}問 | それ以外 {other_count:2d}問 | 計 {stats['total']:2d}提出")
            
            # 詳細結果
            details = []
            if stats['WA'] > 0:
                details.append(f"WA:{stats['WA']}")
            if stats['TLE'] > 0:
                details.append(f"TLE:{stats['TLE']}")
            if stats['RE'] > 0:
                details.append(f"RE:{stats['RE']}")
            if stats['CE'] > 0:
                details.append(f"CE:{stats['CE']}")
            if stats['MLE'] > 0:
                details.append(f"MLE:{stats['MLE']}")
            if stats['Other'] > 0:
                details.append(f"Other:{stats['Other']}")
            
            if details:
                print(f"        詳細: {' | '.join(details)}")
            
            # AC済み問題一覧
            if ac_problems > 0:
                ac_list = sorted(list(stats['ac_problems']))
                print(f"        AC問題: {' '.join(ac_list)}")
            
            print()
        
        # 総合統計
        print("=" * 70)
        print(f"📊 総合統計")
        print(f"  対象コンテスト数: {total_contests}個")
        print(f"  AC問題数: {total_ac_problems}問")
        print(f"  それ以外問題数: {total_other_problems}問")
        print(f"  総提出数: {total_ac_problems + total_other_problems}件")
        
        # 平均統計
        if total_contests > 0:
            avg_ac = total_ac_problems / total_contests
            avg_other = total_other_problems / total_contests
            print(f"  平均AC問題数/コンテスト: {avg_ac:.1f}問")
            print(f"  平均それ以外問題数/コンテスト: {avg_other:.1f}問")
        
        # 最新10コンテストの詳細
        print(f"\n🏆 最新10コンテストの詳細")
        print("-" * 70)
        
        latest_10 = sorted_contests[-10:] if len(sorted_contests) >= 10 else sorted_contests
        for contest_num in reversed(latest_10):
            stats = contest_analysis[contest_num]
            ac_count = stats['AC']
            other_count = stats['total'] - stats['AC']
            
            print(f"ABC{contest_num}: AC {ac_count}問 | それ以外 {other_count}問")
            
            # 最新の提出を表示
            recent_submissions = sorted(stats['submissions_detail'], 
                                  key=lambda x: x['submission_date'], reverse=True)[:3]
            
            for sub in recent_submissions:
                exec_time = f"{sub['execution_time']}ms" if sub['execution_time'] else "N/A"
                print(f"  {sub['problem']} ({sub['result']}) - {sub['submission_date']} - {exec_time}")
        
        return contest_analysis

    def show_contest_range_analysis(self):
        """コンテスト範囲を指定して分析"""
        print("📊 コンテスト範囲指定分析")
        print("=" * 50)
        
        # 範囲入力
        start_contest, end_contest = self.get_contest_range_input()
        if not start_contest or not end_contest:
            print("❌ 範囲指定が無効です")
            return
        
        # 指定範囲の提出データを取得
        range_submissions = self.get_submissions_by_contest_range(start_contest, end_contest)
        if not range_submissions:
            print("❌ 指定範囲の提出データが取得できませんでした")
            return
        
        # 分析実行
        self.analyze_contest_submissions(start_contest)

    def debug_submission_data(self):
        """提出データの詳細デバッグ"""
        print("🔍 提出データ詳細デバッグ")
        print("=" * 50)
        
        try:
            url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={self.user_id}&from_second=0"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ API取得失敗: {response.status_code}")
                return
            
            submissions = response.json()
            print(f"✅ 全提出データ取得: {len(submissions)}件")
            
            # ABC提出のみ抽出して詳細確認
            abc_submissions = []
            contest_numbers = set()
            
            for submission in submissions:
                problem_id = submission.get('problem_id', '')
                
                if problem_id.startswith('abc'):
                    parts = problem_id.split('_')
                    if len(parts) == 2:
                        contest_part = parts[0]  # abc213
                        contest_num = contest_part[3:]  # 213
                        
                        if contest_num.isdigit():
                            contest_number = int(contest_num)
                            contest_numbers.add(contest_number)
                            abc_submissions.append({
                                'problem_id': problem_id,
                                'contest_num': contest_number,
                                'result': submission.get('result', ''),
                                'submission_date': self.format_timestamp(submission.get('epoch_second', 0))
                            })
            
            print(f"📊 ABC提出数: {len(abc_submissions)}件")
            
            # コンテスト番号の範囲を確認
            if contest_numbers:
                min_contest = min(contest_numbers)
                max_contest = max(contest_numbers)
                print(f"📊 実際のコンテスト範囲: ABC{min_contest} ～ ABC{max_contest}")
                
                # 範囲別統計
                ranges = [
                    (200, 250, "ABC200-250"),
                    (251, 300, "ABC251-300"),
                    (301, 349, "ABC301-349"),
                    (350, 400, "ABC350-400"),
                    (401, 450, "ABC401-450")
                ]
                
                print(f"\n📊 範囲別統計:")
                for start, end, label in ranges:
                    count = len([c for c in contest_numbers if start <= c <= end])
                    if count > 0:
                        print(f"  {label}: {count}コンテスト")
                
                # 最新20コンテストの提出状況
                print(f"\n🏆 最新20コンテストの提出状況:")
                sorted_contests = sorted(contest_numbers, reverse=True)[:20]
                
                for contest_num in sorted_contests:
                    contest_submissions = [s for s in abc_submissions if s['contest_num'] == contest_num]
                    ac_count = len([s for s in contest_submissions if s['result'] == 'AC'])
                    total_count = len(contest_submissions)
                    
                    print(f"  ABC{contest_num}: AC {ac_count}問 | 計 {total_count}提出")
                    
                    # 最新の提出を表示
                    latest_sub = max(contest_submissions, key=lambda x: x['submission_date'])
                    print(f"    最新提出: {latest_sub['problem_id']} ({latest_sub['result']}) - {latest_sub['submission_date']}")
            
            else:
                print("❌ ABC提出データが見つかりません")
                
        except Exception as e:
            print(f"❌ エラー: {e}")

    def process_contest_range_interactive(self):
        """コンテスト範囲選択の対話式処理"""
        print("📋 コンテスト範囲選択モード")
        print("=" * 50)
        
        # 範囲入力
        start_contest, end_contest = self.get_contest_range_input()
        if not start_contest or not end_contest:
            print("❌ 範囲指定が無効です")
            return
        
        # 処理選択
        print(f"\n🎯 ABC{start_contest}～ABC{end_contest}の処理を選択してください:")
        action = input("1. 空ファイル作成のみ\n2. 空ファイル作成+コード更新\n3. 既存ファイルの更新のみ\n4. 分析のみ ⭐NEW⭐\n選択 (1-4): ")
        
        if action == '1':
            # 空ファイル作成のみ
            created_count = self.create_files_by_contest_range(start_contest, end_contest)
            print(f"\n✅ 完了: {created_count}個のファイルを作成しました")
        
        elif action == '2':
            # 空ファイル作成+コード更新
            created_count = self.create_files_by_contest_range(start_contest, end_contest)
            if created_count > 0:
                print(f"\n🎯 続けてコード更新を実行しますか？ (y/n): ", end="")
                if input().lower() == 'y':
                    self.update_files_by_contest_range(start_contest, end_contest, max_updates=1000)
            else:
                print("❌ 作成されたファイルがないため、更新をスキップします")
                
        elif action == '3':
            # 既存ファイルの更新のみ
            self.update_files_by_contest_range(start_contest, end_contest, max_updates=1000)
            
        elif action == '4':
            # 分析のみ
            self.analyze_contest_range_detailed(start_contest, end_contest)
            
        else:
            print("❌ 無効な選択です")

    def analyze_contest_range_detailed(self, start_contest, end_contest):
        """指定コンテスト範囲の詳細分析"""
        print(f"📊 ABC{start_contest}～ABC{end_contest}の詳細分析")
        print("=" * 70)
        
        # 指定範囲の提出データを取得
        range_submissions = self.get_submissions_by_contest_range(start_contest, end_contest)
        if not range_submissions:
            print("❌ 指定範囲の提出データが取得できませんでした")
            return
        
        # コンテスト別に分析
        contest_analysis = {}
        
        for submission in range_submissions:
            problem_id = submission['problem_id']
            parts = problem_id.split('_')
            
            if len(parts) == 2:
                contest_part = parts[0]  # abc300
                problem_part = parts[1]  # a
                result = submission.get('result', 'Unknown')
                
                contest_num = contest_part[3:]
                if contest_num.isdigit():
                    contest_number = int(contest_num)
                    
                    if contest_number not in contest_analysis:
                        contest_analysis[contest_number] = {
                            'AC': 0,
                            'WA': 0,
                            'TLE': 0,
                            'RE': 0,
                            'CE': 0,
                            'MLE': 0,
                            'OLE': 0,
                            'IE': 0,
                            'WJ': 0,
                            'Other': 0,
                            'total': 0,
                            'problems': set(),
                            'ac_problems': set(),
                            'submissions_detail': []
                        }
                    
                    # 結果別カウント
                    if result == 'AC':
                        contest_analysis[contest_number]['AC'] += 1
                        contest_analysis[contest_number]['ac_problems'].add(problem_part.upper())
                    elif result == 'WA':
                        contest_analysis[contest_number]['WA'] += 1
                    elif result == 'TLE':
                        contest_analysis[contest_number]['TLE'] += 1
                    elif result == 'RE':
                        contest_analysis[contest_number]['RE'] += 1
                    elif result == 'CE':
                        contest_analysis[contest_number]['CE'] += 1
                    elif result == 'MLE':
                        contest_analysis[contest_number]['MLE'] += 1
                    elif result == 'OLE':
                        contest_analysis[contest_number]['OLE'] += 1
                    elif result == 'IE':
                        contest_analysis[contest_number]['IE'] += 1
                    elif result == 'WJ':
                        contest_analysis[contest_number]['WJ'] += 1
                    else:
                        contest_analysis[contest_number]['Other'] += 1
                    
                    contest_analysis[contest_number]['total'] += 1
                    contest_analysis[contest_number]['problems'].add(problem_part.upper())
                    
                    # 詳細情報を保存
                    contest_analysis[contest_number]['submissions_detail'].append({
                        'problem': problem_part.upper(),
                        'result': result,
                        'submission_date': self.format_timestamp(submission.get('epoch_second', 0)),
                        'execution_time': submission.get('execution_time', 0)
                    })
        
        # 結果表示
        print(f"📈 コンテスト別提出状況（ABC{start_contest}～ABC{end_contest}）")
        print("-" * 70)
        
        # ソート（コンテスト番号順）
        sorted_contests = sorted(contest_analysis.keys())
        
        total_contests = len(sorted_contests)
        total_ac_problems = 0
        total_other_problems = 0
        
        for contest_num in sorted_contests:
            stats = contest_analysis[contest_num]
            ac_count = stats['AC']
            other_count = stats['total'] - stats['AC']
            unique_problems = len(stats['problems'])
            ac_problems = len(stats['ac_problems'])
            
            total_ac_problems += ac_count
            total_other_problems += other_count
            
            # 基本情報
            print(f"ABC{contest_num:03d}: AC {ac_count:2d}問 | それ以外 {other_count:2d}問 | 計 {stats['total']:2d}提出")
            
            # 詳細結果
            details = []
            if stats['WA'] > 0:
                details.append(f"WA:{stats['WA']}")
            if stats['TLE'] > 0:
                details.append(f"TLE:{stats['TLE']}")
            if stats['RE'] > 0:
                details.append(f"RE:{stats['RE']}")
            if stats['CE'] > 0:
                details.append(f"CE:{stats['CE']}")
            if stats['MLE'] > 0:
                details.append(f"MLE:{stats['MLE']}")
            if stats['Other'] > 0:
                details.append(f"Other:{stats['Other']}")
            
            if details:
                print(f"        詳細: {' | '.join(details)}")
            
            # AC済み問題一覧
            if ac_problems > 0:
                ac_list = sorted(list(stats['ac_problems']))
                print(f"        AC問題: {' '.join(ac_list)}")
            
            print()
        
        # 総合統計
        print("=" * 70)
        print(f"📊 総合統計")
        print(f"  対象コンテスト数: {total_contests}個")
        print(f"  AC問題数: {total_ac_problems}問")
        print(f"  それ以外問題数: {total_other_problems}問")
        print(f"  総提出数: {total_ac_problems + total_other_problems}件")
        
        # 平均統計
        if total_contests > 0:
            avg_ac = total_ac_problems / total_contests
            avg_other = total_other_problems / total_contests
            print(f"  平均AC問題数/コンテスト: {avg_ac:.1f}問")
            print(f"  平均それ以外問題数/コンテスト: {avg_other:.1f}問")
        
        # 最新10コンテストの詳細
        print(f"\n🏆 最新10コンテストの詳細")
        print("-" * 70)
        
        latest_10 = sorted_contests[-10:] if len(sorted_contests) >= 10 else sorted_contests
        for contest_num in reversed(latest_10):
            stats = contest_analysis[contest_num]
            ac_count = stats['AC']
            other_count = stats['total'] - stats['AC']
            
            print(f"ABC{contest_num}: AC {ac_count}問 | それ以外 {other_count}問")
            
            # 最新の提出を表示
            recent_submissions = sorted(stats['submissions_detail'], 
                                  key=lambda x: x['submission_date'], reverse=True)[:3]
            
            for sub in recent_submissions:
                exec_time = f"{sub['execution_time']}ms" if sub['execution_time'] else "N/A"
                print(f"  {sub['problem']} ({sub['result']}) - {sub['submission_date']} - {exec_time}")
        
        return contest_analysis

def main():
    print("🚀 AtCoder ソースコード自動更新ツール（デバッグ対応）")
    print("=" * 70)
    
    choice = input("""実行モードを選択してください:
1. 単一ファイルテスト
2. 空ファイル自動作成（全範囲・AC非AC含む）
3. 10件制限更新（全範囲・AC非AC含む）
4. 全件更新（全範囲・AC非AC含む）
5. 最新コンテスト確認
6. コンテスト範囲選択処理
7. コンテスト別提出状況分析
8. 範囲指定コンテスト分析
9. 提出データ詳細デバッグ ⭐NEW⭐
選択 (1-9): """)
    
    if choice == '1':
        test_single_update()
    elif choice == '2':
        updater = SourceCodeUpdater()
        created_count = updater.create_missing_files_in_range()
        if created_count > 0:
            print(f"\n🎯 続けて更新しますか？ (y/n): ", end="")
            if input().lower() == 'y':
                updater.update_all_empty_files_in_range(max_updates=1000)
    elif choice == '3':
        updater = SourceCodeUpdater()
        updater.update_all_empty_files_in_range(max_updates=10)
    elif choice == '4':
        updater = SourceCodeUpdater()
        updater.update_all_empty_files_in_range(max_updates=1000)
    elif choice == '5':
        test_latest_contest()
    elif choice == '6':
        updater = SourceCodeUpdater()
        updater.process_contest_range_interactive()
    elif choice == '7':
        updater = SourceCodeUpdater()
        updater.analyze_contest_submissions()
    elif choice == '8':
        updater = SourceCodeUpdater()
        updater.show_contest_range_analysis()
    elif choice == '9':
        updater = SourceCodeUpdater()
        updater.debug_submission_data()
    else:
        print("無効な選択です")

if __name__ == "__main__":
    main()
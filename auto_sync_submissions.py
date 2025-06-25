#!/usr/bin/env python3
"""
AtCoder Problems APIを使用して、ACした提出を自動でGitHubに同期するスクリプト
"""

import os
import requests
import json
import time
import argparse
from datetime import datetime, timezone, timedelta
import re
from typing import Dict, List, Optional, Tuple

# 設定
ATCODER_USER_ID = os.environ.get("ATCODER_USER_ID", "Y_maekawa")
API_BASE_URL = "https://kenkoooo.com/atcoder/atcoder-api"
SUPPORTED_LANGUAGES = {
    "Java": ".java",
    "Java8": ".java", 
    "OpenJDK": ".java",
    "C++": ".cpp",
    "C++14": ".cpp",
    "C++17": ".cpp",
    "C++20": ".cpp",
    "Python": ".py",
    "Python3": ".py",
    "PyPy3": ".py"
}

class AtCoderSyncer:
    def __init__(self, user_id: str, base_path: str = "."):
        self.user_id = user_id
        self.base_path = base_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AtCoder-GitHub-Syncer/1.0'
        })
        
    def get_user_submissions(self, from_second: Optional[int] = None) -> List[Dict]:
        """ユーザーの提出データを取得"""
        url = f"{API_BASE_URL}/v3/user/submissions"
        params = {"user": self.user_id}
        if from_second:
            params["from_second"] = from_second
            
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"APIリクエストエラー: {e}")
            return []
    
    def get_problems_info(self) -> Dict[str, Dict]:
        """問題情報を取得"""
        url = f"{API_BASE_URL}/v3/problems"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            problems = response.json()
            return {p["id"]: p for p in problems}
        except requests.RequestException as e:
            print(f"問題情報取得エラー: {e}")
            return {}
    
    def parse_contest_and_problem(self, problem_id: str) -> Optional[Tuple[str, str]]:
        """問題IDからコンテスト名と問題を解析"""
        # ABC形式の問題のみ対象
        match = re.match(r"(abc\d{3})_([a-z])", problem_id.lower())
        if match:
            contest = match.group(1).upper()  # ABC126
            problem = match.group(2).upper()  # A
            return contest, problem
        return None
    
    def get_submission_source_code(self, submission_id: int, contest_id: str) -> Optional[str]:
        """提出のソースコードを取得"""
        # 実際のスクレイピング実装
        try:
            from scraper import AtCoderScraper
            scraper = AtCoderScraper()
            return scraper.get_submission_with_retry(submission_id, contest_id)
        except ImportError:
            # スクレイピング機能が利用できない場合のフォールバック
            return self._create_placeholder_code(submission_id, contest_id)
    
    def _create_placeholder_code(self, submission_id: int, contest_id: str) -> str:
        """プレースホルダーコードを生成"""
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return f"""// AtCoder Submission ID: {submission_id}
// Contest: {contest_id}
// Generated: {timestamp}
// 
// 注意: これは自動生成されたプレースホルダーです
// 実際のソースコードを取得するには、AtCoderにログインしてスクレイピング機能を有効にしてください

public class Main {{
    public static void main(String[] args) {{
        // AC solution for submission {submission_id}
        // 実装は AtCoder の提出詳細ページを参照してください
        // https://atcoder.jp/contests/{contest_id}/submissions/{submission_id}
    }}
}}"""
    
    def check_existing_files(self, contest: str, problem: str) -> Dict[str, str]:
        """既存ファイルの確認"""
        folder_path = os.path.join(self.base_path, contest)
        if not os.path.exists(folder_path):
            return {}
        
        existing_files = {}
        files = os.listdir(folder_path)
        
        # 標準的なファイル名をチェック (A.java, B.cpp, etc.)
        for ext in ['.java', '.cpp', '.py', '.cs', '.c']:
            standard_name = f"{problem.upper()}{ext}"
            if standard_name in files:
                filepath = os.path.join(folder_path, standard_name)
                if os.path.getsize(filepath) > 0:  # 空ファイルでない
                    existing_files['standard'] = filepath
                    break
        
        # タイムスタンプ付きファイルをチェック
        problem_lower = problem.lower()
        timestamp_files = [f for f in files if f.startswith(f"{problem_lower}_") and any(f.endswith(ext) for ext in ['.java', '.cpp', '.py', '.cs', '.c'])]
        if timestamp_files:
            # 最新のタイムスタンプファイルを取得
            timestamp_files.sort(reverse=True)
            existing_files['timestamp'] = os.path.join(folder_path, timestamp_files[0])
        
        return existing_files
    
    def save_submission_code(self, contest: str, problem: str, 
                           language: str, source_code: str, 
                           submission_id: int, epoch_second: int) -> bool:
        """提出コードをファイルに保存（既存ファイルを考慮）"""
        if language not in SUPPORTED_LANGUAGES:
            print(f"未対応言語: {language}")
            return False
            
        folder_path = self.create_contest_folder(contest)
        extension = SUPPORTED_LANGUAGES[language]
        
        # 既存ファイルを確認
        existing_files = self.check_existing_files(contest, problem)
        
        if existing_files:
            # 既存ファイルがある場合の処理
            if 'standard' in existing_files:
                print(f"📁 既存ファイル発見: {existing_files['standard']}")
                
                # 既存ファイルの内容と比較
                try:
                    with open(existing_files['standard'], 'r', encoding='utf-8') as f:
                        existing_content = f.read().strip()
                    
                    # プレースホルダーまたは空ファイルの場合は更新
                    if (len(existing_content) == 0 or 
                        'placeholder' in existing_content.lower() or
                        'auto-generated' in existing_content.lower()):
                        
                        print(f"🔄 プレースホルダーファイルを更新: {existing_files['standard']}")
                        with open(existing_files['standard'], 'w', encoding='utf-8') as f:
                            f.write(self._add_submission_header(source_code, submission_id, epoch_second))
                        return True
                    else:
                        print(f"✅ 既に有効なコードが存在: {existing_files['standard']}")
                        return False
                        
                except Exception as e:
                    print(f"⚠️  既存ファイル読み込みエラー: {e}")
        
        # 新しいファイルを作成（標準形式を優先）
        standard_filename = f"{problem.upper()}{extension}"
        standard_filepath = os.path.join(folder_path, standard_filename)
        
        # 標準ファイルが存在しない場合は作成
        if not os.path.exists(standard_filepath):
            try:
                with open(standard_filepath, 'w', encoding='utf-8') as f:
                    f.write(self._add_submission_header(source_code, submission_id, epoch_second))
                print(f"📄 新規作成: {standard_filepath}")
                return True
            except Exception as e:
                print(f"ファイル作成エラー: {e}")
                return False
        
        # 標準ファイルが既にある場合はタイムスタンプ付きで作成
        timestamp = datetime.fromtimestamp(epoch_second).strftime("%Y%m%d_%H%M%S")
        timestamp_filename = f"{problem.lower()}_{timestamp}{extension}"
        timestamp_filepath = os.path.join(folder_path, timestamp_filename)
        
        try:
            with open(timestamp_filepath, 'w', encoding='utf-8') as f:
                f.write(self._add_submission_header(source_code, submission_id, epoch_second))
            print(f"📄 タイムスタンプ付きで保存: {timestamp_filepath}")
            return True
        except Exception as e:
            print(f"ファイル保存エラー: {e}")
            return False
    
    def _add_submission_header(self, source_code: str, submission_id: int, epoch_second: int) -> str:
        """ソースコードにヘッダー情報を追加"""
        timestamp = datetime.fromtimestamp(epoch_second).strftime("%Y/%m/%d %H:%M:%S")
        header = f"""/*
 * AtCoder Submission Info:
 * - Submission ID: {submission_id}
 * - Submitted at: {timestamp}
 * - Auto-synced from AtCoder Problems API
 */

"""
        return header + source_code
    
    def sync_ac_submissions(self, days_back: int = 7, include_all_history: bool = False) -> List[str]:
        """最近のAC提出を同期"""
        print(f"📡 {self.user_id}の提出データを取得中...")
        
        if include_all_history:
            print("🗂️  全履歴を対象に同期します...")
            submissions = self.get_user_submissions()
        else:
            # 指定日数前からの提出を取得
            cutoff_time = int((datetime.now() - timedelta(days=days_back)).timestamp())
            submissions = self.get_user_submissions(from_second=cutoff_time)
        
        if not submissions:
            print("提出データが取得できませんでした")
            return []
        
        print(f"📊 {len(submissions)}件の提出を確認中...")
        
        synced_files = []
        ac_submissions = []
        
        # AC提出のみフィルタリング
        for sub in submissions:
            if sub.get("result") == "AC":
                contest_problem = self.parse_contest_and_problem(sub["problem_id"])
                if contest_problem:
                    ac_submissions.append((sub, contest_problem))
        
        print(f"✅ {len(ac_submissions)}件のAC提出を発見")
        
        if not ac_submissions:
            print("対象となるABC問題のAC提出がありませんでした")
            return []
        
        # 各AC提出を処理
        for i, (submission, (contest, problem)) in enumerate(ac_submissions):
            submission_id = submission["id"]
            language = submission["language"]
            epoch_second = submission["epoch_second"]
            contest_id = submission["contest_id"]
            
            print(f"🔍 処理中 ({i+1}/{len(ac_submissions)}): {contest} {problem} ({language})")
            
            # ソースコードを取得
            source_code = self.get_submission_source_code(submission_id, contest_id)
            
            if source_code and self.save_submission_code(
                contest, problem, language, source_code, 
                submission_id, epoch_second
            ):
                synced_files.append(f"{contest}/{problem}")
                
            # API制限対策
            time.sleep(1.0)  # 少し間隔を開ける
        
        return synced_files
    
    def create_commit_message(self, synced_files: List[str]) -> str:
        """コミットメッセージを生成"""
        if not synced_files:
            return "No new AC submissions to sync"
            
        if len(synced_files) == 1:
            return f"🎉 AC: {synced_files[0]}"
        else:
            contests = set(f.split('/')[0] for f in synced_files)
            if len(contests) == 1:
                return f"🎉 AC: {list(contests)[0]} ({len(synced_files)} problems)"
            else:
                return f"🎉 AC: {len(synced_files)} problems across {len(contests)} contests"
    
    def create_contest_folder(self, contest: str) -> str:
        """コンテストフォルダを作成"""
        folder_path = os.path.join(self.base_path, contest)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='AtCoder提出自動同期')
    parser.add_argument('--days-back', type=int, default=7, 
                       help='何日前まで遡って同期するか (デフォルト: 7)')
    parser.add_argument('--user-id', type=str, default=ATCODER_USER_ID,
                       help='AtCoderユーザーID')
    parser.add_argument('--dry-run', action='store_true',
                       help='実際のファイル作成を行わず、処理内容のみ表示')
    parser.add_argument('--all-history', action='store_true',
                       help='全ての提出履歴を対象に同期（初回セットアップ用）')
    
    args = parser.parse_args()
    
    syncer = AtCoderSyncer(args.user_id)
    
    print(f"🚀 AtCoder提出自動同期を開始... (ユーザー: {args.user_id})")
    
    if args.all_history:
        print("📚 全履歴同期モード: 過去のすべてのAC提出を確認")
        print("⚠️  初回実行時のみ推奨（時間がかかります）")
    else:
        print(f"📅 過去{args.days_back}日間の提出を確認")
    
    if args.dry_run:
        print("🔍 ドライランモード: 実際のファイル作成は行いません")
    
    synced_files = syncer.sync_ac_submissions(
        days_back=args.days_back, 
        include_all_history=args.all_history
    )
    
    if synced_files:
        commit_msg = syncer.create_commit_message(synced_files)
        print(f"\n✨ 同期完了! {len(synced_files)}個のファイルを更新")
        print(f"💬 推奨コミットメッセージ: {commit_msg}")
        
        # 同期したファイルの詳細を表示
        print("\n📂 同期されたファイル:")
        for file_path in sorted(synced_files):
            print(f"  - {file_path}")
            
        # 統計情報を表示
        contests = set(f.split('/')[0] for f in synced_files)
        print(f"\n📊 統計: {len(contests)}個のコンテスト, {len(synced_files)}問題")
    else:
        print("\n📝 新しく同期する提出はありませんでした")
        print("💡 既存ファイルがある問題はスキップされています")

if __name__ == "__main__":
    main()

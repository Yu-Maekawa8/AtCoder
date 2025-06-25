#!/usr/bin/env python3
"""
AtCoder過去提出の一括同期スクリプト
既存のABC126-406フォルダと提出履歴を照合して、不足分を補完します
"""

import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auto_sync_submissions import AtCoderSyncer
from config import ATCODER_USER_ID

class HistorySyncer(AtCoderSyncer):
    def __init__(self, user_id: str, base_path: str = "."):
        super().__init__(user_id, base_path)
        self.sync_report = {
            'total_folders': 0,
            'folders_with_files': 0,
            'empty_folders': 0,
            'updated_files': 0,
            'skipped_files': 0,
            'errors': []
        }
    
    def analyze_existing_structure(self) -> dict:
        """既存のフォルダ構造を分析"""
        analysis = {
            'folders': {},
            'summary': {
                'total_contests': 0,
                'contests_with_files': 0,
                'empty_contests': 0,
                'total_problems': 0,
                'problems_with_code': 0
            }
        }
        
        print("📂 既存フォルダ構造を分析中...")
        
        # ABC126-406の範囲をチェック
        for contest_num in range(126, 407):
            contest_name = f"ABC{contest_num:03d}"
            folder_path = os.path.join(self.base_path, contest_name)
            
            if os.path.exists(folder_path):
                analysis['folders'][contest_name] = {
                    'problems': {},
                    'has_files': False,
                    'file_count': 0
                }
                
                analysis['summary']['total_contests'] += 1
                
                # A-D問題をチェック
                for problem in ['A', 'B', 'C', 'D']:
                    problem_files = []
                    
                    # 各拡張子をチェック
                    for ext in ['.java', '.cpp', '.py', '.cs', '.c']:
                        file_path = os.path.join(folder_path, f"{problem}{ext}")
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            problem_files.append({
                                'path': file_path,
                                'size': file_size,
                                'has_content': file_size > 0
                            })
                    
                    analysis['folders'][contest_name]['problems'][problem] = problem_files
                    
                    if problem_files and any(f['has_content'] for f in problem_files):
                        analysis['summary']['problems_with_code'] += 1
                        analysis['folders'][contest_name]['has_files'] = True
                        analysis['folders'][contest_name]['file_count'] += 1
                    
                    analysis['summary']['total_problems'] += 1
                
                if analysis['folders'][contest_name]['has_files']:
                    analysis['summary']['contests_with_files'] += 1
                else:
                    analysis['summary']['empty_contests'] += 1
        
        return analysis
    
    def sync_with_atcoder_history(self, analysis: dict, limit_contests: int = None) -> dict:
        """AtCoder提出履歴と照合して同期"""
        print(f"\n🔄 AtCoder提出履歴との同期開始...")
        
        # 全提出履歴を取得
        print("📡 提出履歴を取得中...")
        submissions = self.get_user_submissions()
        
        if not submissions:
            print("❌ 提出データが取得できませんでした")
            return self.sync_report
        
        print(f"📊 {len(submissions)}件の提出を分析中...")
        
        # AC提出をフィルタリング
        ac_submissions = []
        for sub in submissions:
            if sub.get("result") == "AC":
                contest_problem = self.parse_contest_and_problem(sub["problem_id"])
                if contest_problem:
                    contest, problem = contest_problem
                    # ABC126-406の範囲内かチェック
                    if contest in analysis['folders']:
                        ac_submissions.append((sub, contest_problem))
        
        print(f"✅ 対象範囲内のAC提出: {len(ac_submissions)}件")
        
        # 各提出を処理
        processed_contests = set()
        for i, (submission, (contest, problem)) in enumerate(ac_submissions):
            if limit_contests and len(processed_contests) >= limit_contests:
                print(f"⏸️  処理制限に達しました ({limit_contests}コンテスト)")
                break
            
            processed_contests.add(contest)
            
            submission_id = submission["id"]
            language = submission["language"]
            epoch_second = submission["epoch_second"]
            contest_id = submission["contest_id"]
            
            print(f"🔍 処理中 ({i+1}/{len(ac_submissions)}): {contest} {problem}")
            
            # 既存ファイルの状況を確認
            existing_files = self.check_existing_files(contest, problem)
            
            if existing_files and 'standard' in existing_files:
                # 既存ファイルの内容を確認
                try:
                    with open(existing_files['standard'], 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    
                    if content and len(content) > 50 and 'placeholder' not in content.lower():
                        print(f"  ✅ 既に有効なコード存在: {problem}")
                        self.sync_report['skipped_files'] += 1
                        continue
                except:
                    pass
            
            # ソースコードを取得して保存
            source_code = self.get_submission_source_code(submission_id, contest_id)
            
            if source_code:
                if self.save_submission_code(contest, problem, language, source_code, 
                                           submission_id, epoch_second):
                    self.sync_report['updated_files'] += 1
                    print(f"  📄 更新完了: {contest} {problem}")
                else:
                    self.sync_report['errors'].append(f"{contest} {problem}: 保存失敗")
            else:
                self.sync_report['errors'].append(f"{contest} {problem}: ソースコード取得失敗")
            
            # API制限対策
            import time
            time.sleep(1.5)
        
        return self.sync_report
    
    def generate_report(self, analysis: dict) -> str:
        """同期レポートを生成"""
        report = []
        report.append("# AtCoder履歴同期レポート")
        report.append(f"生成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
        report.append("")
        
        # 既存構造の分析結果
        report.append("## 📊 既存フォルダ構造分析")
        s = analysis['summary']
        report.append(f"- 総コンテスト数: {s['total_contests']}")
        report.append(f"- ファイル有りコンテスト: {s['contests_with_files']}")
        report.append(f"- 空のコンテスト: {s['empty_contests']}")
        report.append(f"- 総問題数: {s['total_problems']}")
        report.append(f"- コード有り問題数: {s['problems_with_code']}")
        report.append("")
        
        # 同期結果
        report.append("## 🔄 同期結果")
        report.append(f"- 更新されたファイル: {self.sync_report['updated_files']}")
        report.append(f"- スキップされたファイル: {self.sync_report['skipped_files']}")
        report.append(f"- エラー: {len(self.sync_report['errors'])}")
        report.append("")
        
        if self.sync_report['errors']:
            report.append("## ❌ エラー詳細")
            for error in self.sync_report['errors']:
                report.append(f"- {error}")
        
        return "\n".join(report)

def main():
    print("🚀 AtCoder履歴同期ツール開始")
    print("=" * 50)
    
    syncer = HistorySyncer(ATCODER_USER_ID)
    
    # 既存構造を分析
    analysis = syncer.analyze_existing_structure()
    
    print("\n📋 分析結果:")
    s = analysis['summary']
    print(f"  - 総コンテスト: {s['total_contests']}")
    print(f"  - ファイル有り: {s['contests_with_files']}")
    print(f"  - 空フォルダ: {s['empty_contests']}")
    print(f"  - コード有り問題: {s['problems_with_code']}/{s['total_problems']}")
    
    # 同期実行確認
    print(f"\n🤔 AtCoder提出履歴と同期しますか？")
    print("   (既存ファイルがある問題はスキップされます)")
    
    while True:
        choice = input("\n選択してください [y/n/test]: ").lower().strip()
        if choice in ['y', 'yes']:
            break
        elif choice in ['n', 'no']:
            print("同期をキャンセルしました")
            return
        elif choice in ['test', 't']:
            print("テストモード: 最初の5コンテストのみ処理")
            syncer.sync_with_atcoder_history(analysis, limit_contests=5)
            break
        else:
            print("y/n/test のいずれかを入力してください")
    
    if choice in ['y', 'yes']:
        # 本格的な同期実行
        syncer.sync_with_atcoder_history(analysis)
    
    # レポート生成
    report = syncer.generate_report(analysis)
    
    # レポートをファイルに保存
    report_file = f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 レポートを保存しました: {report_file}")
    print("\n🎉 履歴同期完了!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AtCoder自動同期機能のテストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_sync_submissions import AtCoderSyncer
from config import ATCODER_USER_ID

def test_api_connection():
    """API接続テスト"""
    print("🔍 AtCoder Problems API接続テスト...")
    syncer = AtCoderSyncer(ATCODER_USER_ID)
    
    # 問題情報取得テスト
    problems = syncer.get_problems_info()
    if problems:
        print(f"✅ 問題データ取得成功: {len(problems)}問題")
        # ABC126のA問題があるかチェック
        if "abc126_a" in problems:
            print("✅ ABC126-A問題データ確認")
        else:
            print("⚠️  ABC126-A問題データが見つかりません")
    else:
        print("❌ 問題データ取得失敗")
        return False
    
    # 提出データ取得テスト
    submissions = syncer.get_user_submissions()
    if submissions:
        print(f"✅ 提出データ取得成功: {len(submissions)}件")
        
        # AC提出の確認
        ac_count = sum(1 for sub in submissions if sub.get("result") == "AC")
        print(f"✅ AC提出数: {ac_count}件")
        
        # ABC形式の問題をチェック
        abc_problems = []
        for sub in submissions[:10]:  # 最新10件をチェック
            parsed = syncer.parse_contest_and_problem(sub["problem_id"])
            if parsed:
                abc_problems.append(parsed)
        
        if abc_problems:
            print(f"✅ ABC問題検出: {len(abc_problems)}件")
            for contest, problem in abc_problems[:3]:  # 最初の3件を表示
                print(f"   - {contest} {problem}")
        else:
            print("⚠️  ABC問題が見つかりません")
            
    else:
        print("❌ 提出データ取得失敗")
        return False
    
    return True

def test_folder_creation():
    """フォルダ作成テスト"""
    print("\n📁 フォルダ作成テスト...")
    syncer = AtCoderSyncer(ATCODER_USER_ID)
    
    test_contest = "ABC999"  # テスト用のコンテスト名
    folder_path = syncer.create_contest_folder(test_contest)
    
    if os.path.exists(folder_path):
        print(f"✅ フォルダ作成成功: {folder_path}")
        # テスト後にフォルダを削除
        try:
            os.rmdir(folder_path)
            print("✅ テストフォルダ削除完了")
        except:
            print("⚠️  テストフォルダ削除失敗（既にファイルが存在する可能性）")
        return True
    else:
        print(f"❌ フォルダ作成失敗: {folder_path}")
        return False

def test_parsing():
    """問題ID解析テスト"""
    print("\n🔍 問題ID解析テスト...")
    syncer = AtCoderSyncer(ATCODER_USER_ID)
    
    test_cases = [
        ("abc126_a", ("ABC126", "A")),
        ("abc300_d", ("ABC300", "D")),
        ("arc123_a", None),  # ABC以外は対象外
        ("invalid_id", None)
    ]
    
    all_passed = True
    for problem_id, expected in test_cases:
        result = syncer.parse_contest_and_problem(problem_id)
        if result == expected:
            print(f"✅ {problem_id} -> {result}")
        else:
            print(f"❌ {problem_id} -> {result} (期待値: {expected})")
            all_passed = False
    
    return all_passed

def main():
    """メインテスト"""
    print("🚀 AtCoder自動同期機能テスト開始\n")
    
    tests = [
        ("API接続", test_api_connection),
        ("フォルダ作成", test_folder_creation),
        ("問題ID解析", test_parsing)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name}テスト: 成功\n")
                passed += 1
            else:
                print(f"❌ {test_name}テスト: 失敗\n")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}テスト: エラー - {e}\n")
            failed += 1
    
    print("=" * 50)
    print(f"📊 テスト結果: {passed}件成功, {failed}件失敗")
    
    if failed == 0:
        print("🎉 すべてのテストが成功しました！")
        print("自動同期機能は正常に動作する準備ができています。")
    else:
        print("⚠️  一部のテストが失敗しました。")
        print("設定や環境を確認してください。")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# AtCoder 自動同期設定

# AtCoderのユーザーID（必須）
ATCODER_USER_ID = "Y_maekawa"

# 自動同期する日数（デフォルト：7日）
DEFAULT_DAYS_BACK = 7

# 対応言語とファイル拡張子
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
    "PyPy3": ".py",
    "C#": ".cs",
    "C": ".c",
    "JavaScript": ".js",
    "TypeScript": ".ts",
    "Go": ".go",
    "Rust": ".rs",
    "Ruby": ".rb",
    "Perl": ".pl",
    "PHP": ".php"
}

# API設定
API_BASE_URL = "https://kenkoooo.com/atcoder/atcoder-api"
RATE_LIMIT_DELAY = 1.0  # API呼び出し間隔（秒）

# ファイル命名規則
# {problem}_{timestamp}{extension} の形式
# 例: a_20250625_140323.java
FILENAME_FORMAT = "{problem}_{timestamp}{extension}"

# コミットメッセージのテンプレート
COMMIT_MESSAGES = {
    "single": "🎉 AC: {contest_problem}",  # 1問の場合
    "multiple_same_contest": "🎉 AC: {contest} ({count} problems)",  # 同じコンテストの複数問題
    "multiple_different": "🎉 AC: {count} problems across {contest_count} contests"  # 異なるコンテストの複数問題
}

# デバッグ設定
DEBUG = False
VERBOSE = True

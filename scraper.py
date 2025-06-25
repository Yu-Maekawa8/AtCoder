#!/usr/bin/env python3
"""
AtCoderからソースコードを取得するスクレイピング機能
"""

import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from typing import Optional

class AtCoderScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://atcoder.jp"
        
    def get_submission_source_code(self, submission_id: int, contest_id: str) -> Optional[str]:
        """提出IDからソースコードを取得"""
        url = f"{self.base_url}/contests/{contest_id}/submissions/{submission_id}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ソースコード部分を探す
            code_element = soup.find('pre', {'id': 'submission-code'}) or \
                          soup.find('div', {'class': 'prettyprint'}) or \
                          soup.find('pre', {'class': 'prettyprint'}) or \
                          soup.find('pre', string=re.compile(r'.*'))
            
            if code_element:
                return code_element.get_text().strip()
            else:
                print(f"⚠️  提出ID {submission_id}: ソースコードが見つかりませんでした")
                return None
                
        except requests.RequestException as e:
            print(f"❌ 提出ID {submission_id}: 取得エラー - {e}")
            return None
        except Exception as e:
            print(f"❌ 提出ID {submission_id}: 解析エラー - {e}")
            return None
    
    def get_submission_with_retry(self, submission_id: int, contest_id: str, max_retries: int = 3) -> Optional[str]:
        """リトライ機能付きでソースコードを取得"""
        for attempt in range(max_retries):
            try:
                code = self.get_submission_source_code(submission_id, contest_id)
                if code:
                    return code
                    
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"⏳ {wait_time}秒待機してリトライ...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"試行 {attempt + 1}/{max_retries} 失敗: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        return None

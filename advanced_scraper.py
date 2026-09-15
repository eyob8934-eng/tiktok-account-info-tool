"""
Advanced TikTok Account Information Extractor with caching and batch processing
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import hashlib
from config import *

class AdvancedTikTokScraper:
    def __init__(self, enable_cache=ENABLE_CACHE):
        self.headers = DEFAULT_HEADERS
        self.enable_cache = enable_cache
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)
        self.request_count = 0
        self.last_request_time = 0

    def get_cache_path(self, username: str) -> Path:
        """Generate cache file path for username"""
        hash_username = hashlib.md5(username.encode()).hexdigest()
        return self.cache_dir / f"{hash_username}.json"

    def load_from_cache(self, username: str) -> Optional[Dict]:
        """Load account info from cache if available and fresh"""
        if not self.enable_cache:
            return None
        
        cache_file = self.get_cache_path(username)
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cached_data['cached_at'])
                if datetime.now() - cache_time < timedelta(seconds=CACHE_DURATION):
                    print(f"[CACHE] Using cached data for @{username}")
                    return cached_data['data']
            except Exception as e:
                print(f"[CACHE] Error reading cache: {e}")
        
        return None

    def save_to_cache(self, username: str, data: Dict):
        """Save account info to cache"""
        if not self.enable_cache:
            return
        
        try:
            cache_file = self.get_cache_path(username)
            cache_data = {
                'username': username,
                'cached_at': datetime.now().isoformat(),
                'data': data
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"[CACHE] Error saving to cache: {e}")

    def rate_limit(self):
        """Implement rate limiting"""
        time_since_last_request = time.time() - self.last_request_time
        min_delay = 1 / REQUESTS_PER_SECOND
        
        if time_since_last_request < min_delay:
            sleep_time = min_delay - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1

    def get_account_info(self, username: str, force_refresh=False) -> Optional[Dict]:
        """Fetch account info with caching support"""
        username = username.lstrip('@')
        
        # Check cache first
        if not force_refresh:
            cached_data = self.load_from_cache(username)
            if cached_data:
                return cached_data
        
        # Rate limiting
        self.rate_limit()
        
        try:
            url = f"{TIKTOK_API_BASE_URL}/user/detail/?uniqueId={username}"
            response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                account_info = self._parse_user_data(data, username)
                
                # Save to cache
                if account_info:
                    self.save_to_cache(username, account_info)
                
                return account_info
            else:
                print(f"[ERROR] Status {response.status_code} for @{username}")
                return None
        
        except Exception as e:
            print(f"[ERROR] Failed to fetch @{username}: {e}")
            return None

    def batch_get_accounts(self, usernames: List[str], output_file: Optional[str] = None) -> List[Dict]:
        """Fetch information for multiple accounts"""
        results = []
        
        print(f"\n[BATCH] Processing {len(usernames)} accounts...")
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] Fetching @{username}...", end=' ')
            account_info = self.get_account_info(username)
            
            if account_info:
                results.append(account_info)
                print("✓")
            else:
                print("✗")
        
        # Save results if output file specified
        if output_file:
            self.save_results(results, output_file)
        
        return results

    def save_results(self, results: List[Dict], output_file: str):
        """Save results to file"""
        try:
            Path(EXPORT_DIR).mkdir(exist_ok=True)
            filepath = Path(EXPORT_DIR) / output_file
            
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n[SAVE] Results saved to {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to save results: {e}")

    def _parse_user_data(self, data: Dict, username: str) -> Optional[Dict]:
        """Parse user data from API response"""
        try:
            user_details = data.get('userDetail', {})
            user = user_details.get('user', {})
            
            create_time = user.get('createTime', 0)
            creation_date = datetime.fromtimestamp(create_time) if create_time else "Unknown"
            
            return {
                'username': username,
                'user_id': user.get('id', 'Unknown'),
                'display_name': user.get('nickname', 'Unknown'),
                'creation_date': str(creation_date),
                'creation_timestamp': create_time,
                'verified': user.get('verified', False),
                'private_account': user.get('privateAccount', False),
                'follower_count': user.get('followerCount', 0),
                'following_count': user.get('followingCount', 0),
                'video_count': user.get('videoCount', 0),
                'device_info': self._extract_device_info(user),
                'avatar_url': user.get('avatarLarger', ''),
                'bio': user.get('signature', '')
            }
        except Exception as e:
            print(f"[ERROR] Failed to parse user data: {e}")
            return None

    def _extract_device_info(self, user: Dict) -> Dict:
        """Extract device information"""
        device_info = {
            'device_model': 'Unknown',
            'os_type': 'Unknown',
            'app_version': 'Unknown',
            'browser_info': 'Unknown'
        }
        
        user_agent = user.get('userAgent', '')
        if user_agent:
            device_info['browser_info'] = user_agent
            
            if 'iPhone' in user_agent:
                device_info['device_model'] = 'iPhone'
                device_info['os_type'] = 'iOS'
            elif 'Android' in user_agent:
                device_info['device_model'] = 'Android'
                device_info['os_type'] = 'Android'
            elif 'Windows' in user_agent:
                device_info['os_type'] = 'Windows'
            elif 'Mac' in user_agent:
                device_info['os_type'] = 'macOS'
        
        return device_info

    def get_stats(self) -> Dict:
        """Get tool statistics"""
        return {
            'total_requests': self.request_count,
            'cache_enabled': self.enable_cache,
            'cache_dir': str(self.cache_dir)
        }


if __name__ == "__main__":
    scraper = AdvancedTikTokScraper()
    
    # Example: Batch processing
    usernames = ["tiktok", "cristiano", "khaby.lame"]
    results = scraper.batch_get_accounts(usernames, output_file="tiktok_accounts.json")
    
    print(f"\n[STATS] {json.dumps(scraper.get_stats(), indent=2)}")

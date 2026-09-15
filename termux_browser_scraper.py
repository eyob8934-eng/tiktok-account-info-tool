"""
TikTok Advanced Browser Automation & Forensics Scraper (Termux & Chromium Optimized)
Expert Level: Multi-threaded, Proxy Support, Data Extraction, Device Spoofing
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time
import re
import threading
from typing import Dict, List, Optional
from datetime import datetime
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('tiktok_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedTikTokTermuxScraper:
    """
    Expert-level TikTok scraper with advanced features
    """
    
    def __init__(self, use_proxy: bool = False, proxy_list: List[str] = None):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        ]
        
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
        self.session_data = {}
        self.extraction_stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': datetime.now()
        }

    def get_chrome_options(self, randomize_ua: bool = True, use_proxy: bool = False) -> Options:
        """
        Get optimized Chrome options with advanced spoofing
        """
        options = Options()
        
        # Termux optimization
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless=new")
        
        # Performance optimization
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-extensions')
        options.add_argument("--disable-sync")
        options.add_argument("--disable-default-apps")
        options.add_argument("--no-default-browser-check")
        
        # Security & Fingerprinting evasion
        options.add_argument("--disable-web-resources")
        options.add_argument("--disable-component-extensions-with-background-pages")
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_settings.popups": 0
        }
        options.add_experimental_option("prefs", prefs)
        
        # User Agent spoofing
        if randomize_ua:
            import random
            user_agent = random.choice(self.user_agents)
        else:
            user_agent = self.user_agents[0]
        options.add_argument(f"user-agent={user_agent}")
        
        # Proxy configuration
        if use_proxy and self.proxy_list:
            proxy = self.proxy_list[self.current_proxy_index % len(self.proxy_list)]
            options.add_argument(f"--proxy-server={proxy}")
            self.current_proxy_index += 1
            logger.info(f"Using proxy: {proxy}")
        
        # Chromium binary path for Termux
        try:
            options.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
        except:
            logger.warning("Chromium binary path not found, using system default")
        
        return options

    def fetch_profile(self, username: str, wait_time: int = 7) -> Optional[Dict]:
        """
        Fetch complete TikTok profile with forensics analysis
        """
        username = username.lstrip('@')
        url = f"https://www.tiktok.com/@{username}"
        
        logger.info(f"Fetching profile for @{username}")
        self.extraction_stats['total_requests'] += 1
        
        driver = None
        try:
            # Initialize WebDriver
            options = self.get_chrome_options(randomize_ua=True, use_proxy=self.use_proxy)
            driver = webdriver.Chrome(options=options)
            
            logger.info(f"Navigating to: {url}")
            driver.get(url)
            
            # Wait for page load
            time.sleep(wait_time)
            
            # Extract profile data
            profile_data = self._extract_profile_data(driver, username)
            
            if profile_data:
                self.extraction_stats['successful'] += 1
                return profile_data
            else:
                self.extraction_stats['failed'] += 1
                return None
        
        except Exception as e:
            logger.error(f"Error fetching profile: {str(e)}")
            self.extraction_stats['failed'] += 1
            return None
        
        finally:
            if driver:
                driver.quit()

    def _extract_profile_data(self, driver, username: str) -> Optional[Dict]:
        """
        Extract complete profile data using multiple methods
        """
        try:
            # Method 1: Extract from __NEXT_DATA__ tag (Primary)
            profile_data = self._extract_from_next_data(driver, username)
            if profile_data:
                return profile_data
            
            # Method 2: Extract from page HTML (Fallback)
            profile_data = self._extract_from_html(driver, username)
            if profile_data:
                return profile_data
            
            logger.warning(f"Could not extract profile data for @{username}")
            return None
        
        except Exception as e:
            logger.error(f"Error extracting profile data: {str(e)}")
            return None

    def _extract_from_next_data(self, driver, username: str) -> Optional[Dict]:
        """
        Extract data from __NEXT_DATA__ JSON container
        """
        try:
            script_element = driver.find_element(By.ID, "__NEXT_DATA__")
            json_raw = script_element.get_attribute('innerHTML')
            data = json.loads(json_raw)
            
            return self._parse_next_data(data, username)
        except Exception as e:
            logger.debug(f"__NEXT_DATA__ extraction failed: {e}")
            return None

    def _extract_from_html(self, driver, username: str) -> Optional[Dict]:
        """
        Extract data from page HTML as fallback
        """
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract meta data
            meta_tags = soup.find_all('meta')
            profile_data = {
                'username': username,
                'extraction_method': 'HTML Meta Tags',
                'metadata': {}
            }
            
            for meta in meta_tags:
                if meta.get('property'):
                    property_name = meta.get('property')
                    content = meta.get('content', '')
                    if 'og:' in property_name or 'twitter:' in property_name:
                        profile_data['metadata'][property_name] = content
            
            return profile_data if profile_data['metadata'] else None
        
        except Exception as e:
            logger.debug(f"HTML extraction failed: {e}")
            return None

    def _parse_next_data(self, data: dict, username: str) -> Optional[Dict]:
        """
        Parse __NEXT_DATA__ JSON structure
        """
        try:
            # Navigate through nested structure
            page_props = data.get('props', {}).get('pageProps', {})
            user_info = page_props.get('userInfo', {})
            
            if not user_info:
                logger.warning(f"No userInfo found for @{username}")
                return None
            
            user = user_info.get('user', {})
            stats = user_info.get('stats', {})
            
            # Extract comprehensive data
            profile = {
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'extraction_method': '__NEXT_DATA__',
                
                # Basic Info
                'user_id': user.get('id'),
                'display_name': user.get('nickname'),
                'unique_id': user.get('uniqueId'),
                'signature': user.get('signature', ''),
                'avatar': user.get('avatarLarger', ''),
                'avatar_medium': user.get('avatarMedium', ''),
                'avatar_small': user.get('avatarThumb', ''),
                
                # Account Status
                'verified': user.get('verified', False),
                'private_account': user.get('privateAccount', False),
                'business_account': user.get('isBusinessAccount', False),
                'restricted': user.get('restricted', False),
                
                # Statistics
                'follower_count': stats.get('followerCount', 0),
                'following_count': stats.get('followingCount', 0),
                'video_count': stats.get('videoCount', 0),
                'heart_count': stats.get('heartCount', 0),
                'comment_count': stats.get('commentCount', 0),
                'share_count': stats.get('shareCount', 0),
                'download_count': stats.get('downloadCount', 0),
                
                # Engagement Analysis
                'engagement_metrics': self._calculate_engagement(stats),
                
                # Device & Browser Info
                'device_info': self._extract_device_info(user),
                
                # Account Forensics
                'forensics': self._analyze_forensics(user, stats),
            }
            
            return profile
        
        except Exception as e:
            logger.error(f"Error parsing __NEXT_DATA__: {str(e)}")
            return None

    def _calculate_engagement(self, stats: dict) -> dict:
        """
        Calculate engagement metrics
        """
        videos = stats.get('videoCount', 0)
        hearts = stats.get('heartCount', 0)
        followers = stats.get('followerCount', 0)
        comments = stats.get('commentCount', 0)
        shares = stats.get('shareCount', 0)
        downloads = stats.get('downloadCount', 0)
        
        return {
            'avg_likes_per_video': int(hearts / videos) if videos > 0 else 0,
            'avg_likes_per_follower': round(hearts / followers, 4) if followers > 0 else 0,
            'avg_comments_per_video': int(comments / videos) if videos > 0 else 0,
            'avg_shares_per_video': int(shares / videos) if videos > 0 else 0,
            'engagement_rate': round((hearts + comments + shares + downloads) / (videos * followers) * 100, 2) if (videos and followers) > 0 else 0,
            'virality_score': round(hearts / followers, 2) if followers > 0 else 0,
            'interaction_score': hearts + comments + shares + downloads
        }

    def _extract_device_info(self, user: dict) -> dict:
        """
        Extract device and platform information
        """
        user_agent = user.get('userAgent', '')
        region = user.get('region', 'Unknown')
        language = user.get('language', 'Unknown')
        
        device_type = 'Unknown'
        os = 'Unknown'
        
        if 'iPhone' in user_agent:
            device_type = 'iPhone'
            os = 'iOS'
        elif 'iPad' in user_agent:
            device_type = 'iPad'
            os = 'iOS'
        elif 'Android' in user_agent:
            device_type = 'Android'
            os = 'Android'
        elif 'Windows' in user_agent:
            device_type = 'Windows PC'
            os = 'Windows'
        elif 'Mac' in user_agent:
            device_type = 'Mac'
            os = 'macOS'
        
        return {
            'type': device_type,
            'os': os,
            'region': region,
            'language': language,
            'user_agent': user_agent
        }

    def _analyze_forensics(self, user: dict, stats: dict) -> dict:
        """
        Analyze account for forensic indicators
        """
        followers = stats.get('followerCount', 0)
        following = stats.get('followingCount', 0)
        videos = stats.get('videoCount', 0)
        hearts = stats.get('heartCount', 0)
        
        # Anomaly detection
        anomalies = []
        
        # Check for bot-like patterns
        if followers > 0 and videos > 0:
            if (followers / (videos + 1)) > 100000:
                anomalies.append('Unusually high followers per video')
        
        if following > 0 and followers > 0:
            follow_ratio = followers / following
            if follow_ratio > 1000:
                anomalies.append('Extremely high follower-to-following ratio')
        
        if hearts > 0 and videos > 0:
            avg_likes = hearts / videos
            if avg_likes > 1000000:
                anomalies.append('Suspiciously high average likes')
        
        return {
            'account_age_assessment': self._assess_account_age(user),
            'growth_pattern': self._analyze_growth_pattern(followers, videos),
            'authenticity_indicators': self._assess_authenticity(user, stats),
            'anomalies_detected': anomalies,
            'risk_score': self._calculate_risk_score(anomalies, stats)
        }

    def _assess_account_age(self, user: dict) -> str:
        """
        Assess account age from available data
        """
        # This would require additional timestamp data from TikTok
        return user.get('createTime', 'Unknown')

    def _analyze_growth_pattern(self, followers: int, videos: int) -> str:
        """
        Analyze growth pattern
        """
        if videos == 0:
            return 'No content'
        
        followers_per_video = followers / videos
        
        if followers_per_video > 50000:
            return 'Exponential growth'
        elif followers_per_video > 10000:
            return 'Rapid growth'
        elif followers_per_video > 1000:
            return 'Steady growth'
        else:
            return 'Slow growth'

    def _assess_authenticity(self, user: dict, stats: dict) -> dict:
        """
        Assess account authenticity
        """
        return {
            'verified': user.get('verified', False),
            'has_profile_pic': bool(user.get('avatarLarger')),
            'has_bio': bool(user.get('signature')),
            'public_account': not user.get('privateAccount', False),
            'business_account': user.get('isBusinessAccount', False)
        }

    def _calculate_risk_score(self, anomalies: list, stats: dict) -> float:
        """
        Calculate risk score (0-100)
        """
        risk = 0
        risk += len(anomalies) * 15
        
        if stats.get('heartCount', 0) == 0 and stats.get('videoCount', 0) > 0:
            risk += 20
        
        return min(100, risk)

    def batch_fetch_profiles(self, usernames: List[str], max_workers: int = 3) -> List[Dict]:
        """
        Fetch multiple profiles concurrently
        """
        logger.info(f"Starting batch fetch for {len(usernames)} profiles")
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.fetch_profile, username): username for username in usernames}
            
            for future in as_completed(futures):
                username = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        logger.info(f"Successfully fetched @{username}")
                except Exception as e:
                    logger.error(f"Error fetching @{username}: {str(e)}")
        
        return results

    def export_profile(self, profile: Dict, filename: str):
        """
        Export profile to JSON file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            logger.info(f"Profile exported to {filename}")
        except Exception as e:
            logger.error(f"Export error: {str(e)}")

    def export_batch(self, profiles: List[Dict], filename: str):
        """
        Export batch profiles to JSON
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)
            logger.info(f"Batch profiles exported to {filename}")
        except Exception as e:
            logger.error(f"Export error: {str(e)}")

    def generate_report(self, profile: Dict) -> str:
        """
        Generate detailed forensics report
        """
        report = "\n" + "=" * 80 + "\n"
        report += "TIKTOK ACCOUNT FORENSICS REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"Username: {profile.get('username')}\n"
        report += f"Display Name: {profile.get('display_name')}\n"
        report += f"User ID: {profile.get('user_id')}\n"
        report += f"Verified: {profile.get('verified')}\n"
        report += f"Business Account: {profile.get('business_account')}\n"
        report += f"Private Account: {profile.get('private_account')}\n\n"
        
        report += "STATISTICS:\n"
        report += f"  Followers: {profile.get('follower_count'):,}\n"
        report += f"  Following: {profile.get('following_count'):,}\n"
        report += f"  Videos: {profile.get('video_count')}\n"
        report += f"  Total Hearts: {profile.get('heart_count'):,}\n\n"
        
        engagement = profile.get('engagement_metrics', {})
        report += "ENGAGEMENT ANALYSIS:\n"
        report += f"  Avg Likes per Video: {engagement.get('avg_likes_per_video'):,}\n"
        report += f"  Engagement Rate: {engagement.get('engagement_rate')}%\n"
        report += f"  Virality Score: {engagement.get('virality_score')}\n"
        report += f"  Interaction Score: {engagement.get('interaction_score'):,}\n\n"
        
        device = profile.get('device_info', {})
        report += "DEVICE INFORMATION:\n"
        report += f"  Type: {device.get('type')}\n"
        report += f"  OS: {device.get('os')}\n"
        report += f"  Region: {device.get('region')}\n"
        report += f"  Language: {device.get('language')}\n\n"
        
        forensics = profile.get('forensics', {})
        report += "FORENSIC ANALYSIS:\n"
        report += f"  Growth Pattern: {forensics.get('growth_pattern')}\n"
        report += f"  Risk Score: {forensics.get('risk_score')}/100\n"
        report += f"  Anomalies Detected: {len(forensics.get('anomalies_detected', []))}\n"
        if forensics.get('anomalies_detected'):
            for anomaly in forensics.get('anomalies_detected'):
                report += f"    - {anomaly}\n"
        
        report += "\n" + "=" * 80 + "\n"
        return report

    def get_stats(self) -> Dict:
        """
        Get extraction statistics
        """
        elapsed = (datetime.now() - self.extraction_stats['start_time']).total_seconds()
        
        return {
            'total_requests': self.extraction_stats['total_requests'],
            'successful': self.extraction_stats['successful'],
            'failed': self.extraction_stats['failed'],
            'success_rate': round(self.extraction_stats['successful'] / max(self.extraction_stats['total_requests'], 1) * 100, 2),
            'elapsed_seconds': elapsed
        }


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("     TIKTOK ADVANCED BROWSER AUTOMATION & FORENSICS SCRAPER")
    print("     Expert Level with Proxy & Device Spoofing")
    print("=" * 80 + "\n")
    
    # Initialize scraper
    scraper = AdvancedTikTokTermuxScraper(use_proxy=False)
    
    # Menu
    while True:
        print("\nOptions:")
        print("1. Fetch single profile")
        print("2. Batch fetch profiles")
        print("3. View statistics")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            username = input("Enter TikTok username: ").strip()
            if username:
                profile = scraper.fetch_profile(username)
                if profile:
                    print(scraper.generate_report(profile))
                    save = input("\nSave to file? (y/n): ").lower()
                    if save == 'y':
                        filename = f"{username}_profile.json"
                        scraper.export_profile(profile, filename)
        
        elif choice == '2':
            usernames_input = input("Enter usernames (comma-separated): ").strip()
            usernames = [u.strip() for u in usernames_input.split(',')]
            if usernames:
                profiles = scraper.batch_fetch_profiles(usernames, max_workers=3)
                print(f"\nFetched {len(profiles)}/{len(usernames)} profiles")
                save = input("Save to file? (y/n): ").lower()
                if save == 'y':
                    scraper.export_batch(profiles, "batch_profiles.json")
        
        elif choice == '3':
            stats = scraper.get_stats()
            print("\nStatistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        
        elif choice == '4':
            print("\nExiting...")
            break

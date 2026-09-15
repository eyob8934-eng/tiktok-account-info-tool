"""
TikTok Account Registration Device Detector - Expert Level
Detects device used for account creation and registration information
Full forensic analysis including registration date, device model, location hints
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('device_registration_detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RegistrationDeviceDetector:
    """
    Expert-level device detector for account registration analysis
    """
    
    def __init__(self):
        self.device_signatures = self._load_device_signatures()
        self.os_patterns = self._load_os_patterns()
        self.registration_patterns = self._load_registration_patterns()
        self.user_agents = self._load_user_agents()

    def _load_device_signatures(self) -> dict:
        """
        Load known device signatures for identification
        """
        return {
            'iPhone': {
                'patterns': ['iPhone14', 'iPhone13', 'iPhone12', 'iPhone11', 'iPhone XS', 'iPhone X', 'iPhone 8'],
                'os': 'iOS',
                'manufacturer': 'Apple',
                'market_share': 0.27,
                'screen_sizes': ['6.1', '6.7', '5.8', '5.5']
            },
            'Samsung': {
                'patterns': ['SM-G', 'SM-A', 'SM-M', 'SM-T'],
                'os': 'Android',
                'manufacturer': 'Samsung',
                'market_share': 0.21,
                'popular_models': ['Galaxy S23', 'Galaxy S22', 'Galaxy A50']
            },
            'Google Pixel': {
                'patterns': ['Pixel 7', 'Pixel 6', 'Pixel 5', 'Pixel 4'],
                'os': 'Android',
                'manufacturer': 'Google',
                'market_share': 0.05,
                'screen_sizes': ['6.1', '6.7', '5.8']
            },
            'Xiaomi': {
                'patterns': ['Mi ', 'Redmi', 'POCO'],
                'os': 'Android',
                'manufacturer': 'Xiaomi',
                'market_share': 0.13,
                'popular_models': ['Mi 13', 'Redmi Note 12']
            },
            'OnePlus': {
                'patterns': ['OnePlus', 'ONEPLUS'],
                'os': 'Android',
                'manufacturer': 'OnePlus',
                'market_share': 0.02,
                'popular_models': ['OnePlus 11', 'OnePlus 10']
            },
            'iPad': {
                'patterns': ['iPad', 'iPad Pro', 'iPad Air', 'iPad Mini'],
                'os': 'iOS',
                'manufacturer': 'Apple',
                'market_share': 0.08,
                'screen_sizes': ['7.9', '8.3', '10.2', '10.9', '12.9']
            }
        }

    def _load_os_patterns(self) -> dict:
        """
        Load OS version patterns
        """
        return {
            'iOS': {
                'versions': ['17.0', '16.7', '16.6', '15.8', '14.8'],
                'pattern': r'OS\s+([\d_]+)'
            },
            'Android': {
                'versions': ['14', '13', '12', '11', '10'],
                'pattern': r'Android\s+([\d\.]+)'
            },
            'Windows': {
                'versions': ['10', '11'],
                'pattern': r'Windows NT\s+([\d\.]+)'
            },
            'macOS': {
                'versions': ['13', '12', '11', '10.15'],
                'pattern': r'Mac OS X\s+([\d_\.]+)'
            }
        }

    def _load_registration_patterns(self) -> dict:
        """
        Load patterns to detect registration information
        """
        return {
            'registration_date_indicators': [
                'created', 'joined', 'since', 'registered',
                'member since', 'account created', 'joined on'
            ],
            'device_hints': [
                'iPhone', 'Android', 'Samsung', 'Pixel',
                'mobile', 'app', 'web', 'tablet'
            ],
            'location_indicators': [
                'location', 'based in', 'from', 'timezone',
                'country', 'city', 'region'
            ]
        }

    def _load_user_agents(self) -> list:
        """
        Load common user agents for profile analysis
        """
        return [
            # iOS
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            # Android
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            # Samsung
            "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            # Google Pixel
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            # iPad
            "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]

    def analyze_registration_device(self, username: str) -> Optional[Dict]:
        """
        Analyze TikTok account for registration device information
        """
        username = username.lstrip('@')
        logger.info(f"Analyzing registration device for @{username}")
        
        driver = None
        try:
            # Initialize WebDriver
            options = self._get_chrome_options()
            driver = webdriver.Chrome(options=options)
            
            url = f"https://www.tiktok.com/@{username}"
            logger.info(f"Fetching: {url}")
            driver.get(url)
            
            # Wait for page load
            time.sleep(5)
            
            # Extract profile data
            profile_data = self._extract_registration_data(driver, username)
            
            if profile_data:
                # Perform device analysis
                device_analysis = self._analyze_device_signatures(profile_data, driver)
                profile_data['device_analysis'] = device_analysis
                
                # Perform registration analysis
                registration_analysis = self._analyze_registration_info(profile_data)
                profile_data['registration_analysis'] = registration_analysis
                
                return profile_data
            
            return None
        
        except Exception as e:
            logger.error(f"Error analyzing registration device: {str(e)}")
            return None
        
        finally:
            if driver:
                driver.quit()

    def _get_chrome_options(self) -> Options:
        """
        Get optimized Chrome options for registration analysis
        """
        options = Options()
        
        # Optimization
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # User agent
        import random
        user_agent = random.choice(self.user_agents)
        options.add_argument(f"user-agent={user_agent}")
        
        # Termux support
        try:
            options.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
        except:
            pass
        
        return options

    def _extract_registration_data(self, driver, username: str) -> Optional[Dict]:
        """
        Extract registration-related data from profile
        """
        try:
            # Method 1: Extract from __NEXT_DATA__
            try:
                script_element = driver.find_element(By.ID, "__NEXT_DATA__")
                json_raw = script_element.get_attribute('innerHTML')
                data = json.loads(json_raw)
                
                user_details = data.get('props', {}).get('pageProps', {}).get('userInfo', {})
                user = user_details.get('user', {})
                stats = user_details.get('stats', {})
                
                return {
                    'username': username,
                    'timestamp': datetime.now().isoformat(),
                    'user_id': user.get('id'),
                    'display_name': user.get('nickname'),
                    'user_agent': user.get('userAgent', ''),
                    'signature': user.get('signature', ''),
                    'create_time': user.get('createTime', 0),
                    'avatar': user.get('avatarLarger'),
                    'verified': user.get('verified', False),
                    'private': user.get('privateAccount', False),
                    'follower_count': stats.get('followerCount', 0),
                    'following_count': stats.get('followingCount', 0),
                    'video_count': stats.get('videoCount', 0),
                    'heart_count': stats.get('heartCount', 0),
                    'raw_user_data': user  # For detailed analysis
                }
            except:
                pass
            
            # Method 2: Extract from HTML fallback
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            profile_data = {
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'extraction_method': 'HTML Fallback'
            }
            
            # Extract from meta tags
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                if meta.get('property') == 'og:title':
                    profile_data['display_name'] = meta.get('content', '').split(' (@')[0]
                if meta.get('property') == 'og:description':
                    profile_data['signature'] = meta.get('content', '')
            
            return profile_data if profile_data.get('display_name') else None
        
        except Exception as e:
            logger.error(f"Error extracting registration data: {str(e)}")
            return None

    def _analyze_device_signatures(self, profile_data: dict, driver) -> dict:
        """
        Analyze device signatures from multiple sources
        """
        user_agent = profile_data.get('user_agent', '')
        
        analysis = {
            'detected_devices': [],
            'primary_device': None,
            'device_confidence_score': 0.0,
            'registration_device': None,
            'device_os': None,
            'device_manufacturer': None,
            'estimated_device_model': None,
            'screen_size_estimate': None,
            'app_version': self._extract_app_version(user_agent)
        }
        
        # Analyze user agent
        device_matches = []
        
        for device_name, device_info in self.device_signatures.items():
            for pattern in device_info.get('patterns', []):
                if pattern.lower() in user_agent.lower():
                    confidence = self._calculate_device_confidence(user_agent, pattern)
                    device_matches.append({
                        'device_name': device_name,
                        'pattern': pattern,
                        'confidence': confidence,
                        'os': device_info.get('os'),
                        'manufacturer': device_info.get('manufacturer')
                    })
        
        # Sort by confidence
        device_matches = sorted(device_matches, key=lambda x: x['confidence'], reverse=True)
        analysis['detected_devices'] = device_matches
        
        if device_matches:
            primary = device_matches[0]
            analysis['primary_device'] = primary['device_name']
            analysis['device_os'] = primary['os']
            analysis['device_manufacturer'] = primary['manufacturer']
            analysis['device_confidence_score'] = primary['confidence']
            
            # Determine if this is likely registration device
            if primary['confidence'] > 0.8:
                analysis['registration_device'] = primary['device_name']
        
        # Extract OS version
        for os_name, os_info in self.os_patterns.items():
            match = re.search(os_info['pattern'], user_agent)
            if match:
                analysis['os_version'] = match.group(1)
                break
        
        return analysis

    def _calculate_device_confidence(self, user_agent: str, pattern: str) -> float:
        """
        Calculate confidence score for device detection
        """
        confidence = 0.5  # Base score
        
        # Check for exact model number
        if re.search(rf'{re.escape(pattern)}\d+', user_agent):
            confidence += 0.3
        
        # Check for OS information
        if any(os in user_agent for os in ['iOS', 'Android', 'Windows', 'Mac']):
            confidence += 0.15
        
        # Check for additional identifiers
        if 'Safari' in user_agent or 'Chrome' in user_agent or 'Firefox' in user_agent:
            confidence += 0.05
        
        return min(1.0, confidence)

    def _analyze_registration_info(self, profile_data: dict) -> dict:
        """
        Analyze registration information from profile
        """
        create_time = profile_data.get('create_time', 0)
        verified = profile_data.get('verified', False)
        follower_count = profile_data.get('follower_count', 0)
        video_count = profile_data.get('video_count', 0)
        signature = profile_data.get('signature', '').lower()
        
        # Calculate account age
        if create_time:
            account_creation = datetime.fromtimestamp(create_time)
            account_age = datetime.now() - account_creation
            account_age_days = account_age.days
            account_age_years = account_age_days / 365
        else:
            account_age_days = None
            account_age_years = None
            account_creation = None
        
        # Analyze registration pattern
        registration_pattern = self._determine_registration_pattern(follower_count, video_count, account_age_days)
        
        # Detect device hints in signature
        device_hints = []
        for hint in self._load_registration_patterns()['device_hints']:
            if hint.lower() in signature:
                device_hints.append(hint)
        
        analysis = {
            'account_creation_date': str(account_creation) if account_creation else 'Unknown',
            'account_creation_timestamp': create_time,
            'account_age_days': account_age_days,
            'account_age_years': round(account_age_years, 2) if account_age_years else None,
            'verified_status': 'Verified' if verified else 'Not Verified',
            'registration_pattern': registration_pattern,
            'device_hints_in_bio': device_hints,
            'initial_growth_metrics': {
                'followers': follower_count,
                'videos': video_count,
                'followers_per_day': round(follower_count / max(account_age_days, 1), 2) if account_age_days else None
            },
            'registration_risk_assessment': self._assess_registration_risk(profile_data)
        }
        
        return analysis

    def _determine_registration_pattern(self, followers: int, videos: int, age_days: Optional[int]) -> str:
        """
        Determine account registration pattern
        """
        if age_days is None or age_days == 0:
            return 'New Account'
        
        if videos == 0:
            if followers == 0:
                return 'Inactive Account'
            else:
                return 'Followers Only (Suspicious)'
        
        if age_days < 30:
            if followers > 10000:
                return 'Rapid Growth - Possible Bot/Bought Followers'
            else:
                return 'New Creator'
        
        if followers / max(age_days, 1) > 100:
            return 'Rapid Consistent Growth'
        
        if videos > 100:
            return 'Established Creator'
        
        return 'Regular User'

    def _assess_registration_risk(self, profile_data: dict) -> dict:
        """
        Assess risk factors in registration
        """
        risk_factors = []
        risk_score = 0
        
        # Check for suspicious patterns
        follower_count = profile_data.get('follower_count', 0)
        video_count = profile_data.get('video_count', 0)
        account_age_days = None
        
        if profile_data.get('create_time'):
            account_creation = datetime.fromtimestamp(profile_data.get('create_time'))
            account_age_days = (datetime.now() - account_creation).days
        
        # Followers but no videos (suspicious)
        if follower_count > 0 and video_count == 0:
            risk_factors.append('High followers with zero videos')
            risk_score += 30
        
        # Rapid follower growth (suspicious)
        if account_age_days and account_age_days > 0:
            daily_followers = follower_count / account_age_days
            if daily_followers > 1000:
                risk_factors.append(f'Suspicious growth: {daily_followers:.0f} followers/day')
                risk_score += 25
        
        # Account age analysis
        if account_age_days and account_age_days < 7:
            risk_factors.append('Very new account')
            risk_score += 10
        
        # No profile picture (risky)
        if not profile_data.get('avatar'):
            risk_factors.append('Missing profile picture')
            risk_score += 15
        
        # Empty bio (risky)
        if not profile_data.get('signature'):
            risk_factors.append('Empty bio')
            risk_score += 5
        
        return {
            'risk_score': min(100, risk_score),
            'risk_level': self._categorize_risk_level(risk_score),
            'risk_factors': risk_factors,
            'verdict': 'Suspicious Account' if risk_score > 60 else 'Normal Account'
        }

    def _categorize_risk_level(self, score: int) -> str:
        """
        Categorize risk level
        """
        if score >= 80:
            return 'Critical'
        elif score >= 60:
            return 'High'
        elif score >= 40:
            return 'Medium'
        elif score >= 20:
            return 'Low'
        else:
            return 'Minimal'

    def _extract_app_version(self, user_agent: str) -> Optional[str]:
        """
        Extract TikTok app version from user agent
        """
        match = re.search(r'TikTok/([\d\.]+)', user_agent)
        if match:
            return match.group(1)
        
        match = re.search(r'com\.ss\.android\.ugc\.trill/([\d\.]+)', user_agent)
        if match:
            return match.group(1)
        
        return None

    def batch_analyze_registrations(self, usernames: List[str]) -> List[Dict]:
        """
        Analyze multiple account registrations
        """
        results = []
        logger.info(f"Starting batch analysis for {len(usernames)} accounts")
        
        for i, username in enumerate(usernames, 1):
            logger.info(f"[{i}/{len(usernames)}] Analyzing @{username}")
            result = self.analyze_registration_device(username)
            if result:
                results.append(result)
        
        return results

    def export_analysis(self, analysis: Dict, filename: str):
        """
        Export registration device analysis to JSON
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            logger.info(f"Analysis exported to {filename}")
        except Exception as e:
            logger.error(f"Export error: {str(e)}")

    def generate_report(self, analysis: Dict) -> str:
        """
        Generate detailed registration device report
        """
        report = "\n" + "=" * 80 + "\n"
        report += "TIKTOK ACCOUNT REGISTRATION DEVICE ANALYSIS REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"Username: {analysis.get('username')}\n"
        report += f"Analysis Time: {analysis.get('timestamp')}\n\n"
        
        # Device Information
        device_analysis = analysis.get('device_analysis', {})
        report += "DEVICE INFORMATION:\n"
        report += "-" * 80 + "\n"
        report += f"Primary Device: {device_analysis.get('primary_device')}\n"
        report += f"Device OS: {device_analysis.get('device_os')}\n"
        report += f"Manufacturer: {device_analysis.get('device_manufacturer')}\n"
        report += f"Device Confidence: {device_analysis.get('device_confidence_score', 0):.2%}\n"
        report += f"App Version: {device_analysis.get('app_version', 'Unknown')}\n\n"
        
        # Detected Devices (alternatives)
        if device_analysis.get('detected_devices'):
            report += "Alternative Device Possibilities:\n"
            for device in device_analysis.get('detected_devices', [])[:3]:
                report += f"  - {device.get('device_name')} ({device.get('confidence', 0):.0%} confidence)\n"
            report += "\n"
        
        # Registration Information
        reg_analysis = analysis.get('registration_analysis', {})
        report += "REGISTRATION INFORMATION:\n"
        report += "-" * 80 + "\n"
        report += f"Account Creation Date: {reg_analysis.get('account_creation_date')}\n"
        report += f"Account Age: {reg_analysis.get('account_age_days')} days ({reg_analysis.get('account_age_years')} years)\n"
        report += f"Verified: {reg_analysis.get('verified_status')}\n"
        report += f"Registration Pattern: {reg_analysis.get('registration_pattern')}\n\n"
        
        # Initial Growth
        growth = reg_analysis.get('initial_growth_metrics', {})
        report += "INITIAL GROWTH METRICS:\n"
        report += f"  Followers: {growth.get('followers'):,}\n"
        report += f"  Videos: {growth.get('videos')}\n"
        report += f"  Followers/Day: {growth.get('followers_per_day')}\n\n"
        
        # Risk Assessment
        risk = reg_analysis.get('registration_risk_assessment', {})
        report += "REGISTRATION RISK ASSESSMENT:\n"
        report += "-" * 80 + "\n"
        report += f"Risk Score: {risk.get('risk_score')}/100\n"
        report += f"Risk Level: {risk.get('risk_level')}\n"
        report += f"Verdict: {risk.get('verdict')}\n"
        if risk.get('risk_factors'):
            report += "Risk Factors:\n"
            for factor in risk.get('risk_factors'):
                report += f"  ⚠️  {factor}\n"
        
        report += "\n" + "=" * 80 + "\n"
        return report


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("   TIKTOK ACCOUNT REGISTRATION DEVICE DETECTOR - EXPERT LEVEL")
    print("   Analyzes device used for account creation and registration")
    print("=" * 80 + "\n")
    
    detector = RegistrationDeviceDetector()
    
    while True:
        print("\nOptions:")
        print("1. Analyze single account")
        print("2. Batch analyze accounts")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            username = input("Enter TikTok username: ").strip()
            if username:
                analysis = detector.analyze_registration_device(username)
                if analysis:
                    report = detector.generate_report(analysis)
                    print(report)
                    
                    save = input("Save report to file? (y/n): ").lower()
                    if save == 'y':
                        filename = f"{username}_registration_analysis.json"
                        detector.export_analysis(analysis, filename)
        
        elif choice == '2':
            usernames_input = input("Enter usernames (comma-separated): ").strip()
            usernames = [u.strip() for u in usernames_input.split(',')]
            if usernames:
                analyses = detector.batch_analyze_registrations(usernames)
                print(f"\nAnalyzed {len(analyses)}/{len(usernames)} accounts")
                
                for analysis in analyses:
                    print(detector.generate_report(analysis))
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid option.")

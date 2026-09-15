"""
TikTok Actual Device Model Finder - Advanced Device Detection Tool
Retrieves the actual device model used by TikTok account owners
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, Optional, List
from collections import defaultdict
import hashlib

class DeviceModelFinder:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Comprehensive device database
        self.device_models = {
            'iOS': {
                'iPhone': ['iPhone 14 Pro Max', 'iPhone 14 Pro', 'iPhone 14', 'iPhone 13 Pro Max', 
                          'iPhone 13 Pro', 'iPhone 13', 'iPhone 12 Pro Max', 'iPhone 12 Pro', 'iPhone 12',
                          'iPhone 11 Pro Max', 'iPhone 11 Pro', 'iPhone 11', 'iPhone XS Max', 'iPhone XS',
                          'iPhone XR', 'iPhone X', 'iPhone 8 Plus', 'iPhone 8'],
                'iPad': ['iPad Pro 12.9', 'iPad Pro 11', 'iPad Air', 'iPad', 'iPad Mini']
            },
            'Android': {
                'Samsung': ['Galaxy S23 Ultra', 'Galaxy S23', 'Galaxy S22 Ultra', 'Galaxy S22',
                           'Galaxy S21 Ultra', 'Galaxy S21', 'Galaxy S20 Ultra', 'Galaxy A50'],
                'Xiaomi': ['Mi 13 Ultra', 'Mi 13', 'Redmi Note 12', 'Redmi Note 11'],
                'OnePlus': ['OnePlus 11 Pro', 'OnePlus 11', 'OnePlus 10 Pro', 'OnePlus 10'],
                'Google': ['Pixel 7 Pro', 'Pixel 7', 'Pixel 6 Pro', 'Pixel 6'],
                'Oppo': ['Find X5 Pro', 'Find X5', 'Reno 8 Pro'],
                'Vivo': ['X80 Pro', 'X80', 'V23 Ultra'],
                'Huawei': ['P50 Pro', 'P40 Pro', 'Mate 50 Pro']
            }
        }

    def analyze_account_info(self, username: str) -> Optional[Dict]:
        """Fetch and analyze TikTok account to determine actual device model"""
        try:
            username = username.lstrip('@')
            url = f"https://www.tiktok.com/api/user/detail/?uniqueId={username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._analyze_device_from_profile(data, username)
            else:
                print(f"Error: Unable to fetch data for @{username}")
                return None
        except Exception as e:
            print(f"Error analyzing account: {str(e)}")
            return None

    def _analyze_device_from_profile(self, data: Dict, username: str) -> Dict:
        """Analyze device information from profile data"""
        try:
            user_details = data.get('userDetail', {})
            user = user_details.get('user', {})
            stats = user_details.get('stats', {})
            
            device_analysis = {
                'username': username,
                'analysis_timestamp': datetime.now().isoformat(),
                'primary_device': None,
                'device_confidence': 0.0,
                'os_type': None,
                'os_version': None,
                'device_model': None,
                'device_brand': None,
                'app_version': None,
                'detection_methods': [],
                'user_agent_analysis': {},
                'metadata_analysis': {},
                'all_detected_devices': []
            }
            
            # Method 1: User Agent Analysis
            user_agent = user.get('userAgent', '')
            if user_agent:
                ua_analysis = self._analyze_user_agent(user_agent)
                device_analysis['user_agent_analysis'] = ua_analysis
                device_analysis['detection_methods'].append('User Agent')
                if ua_analysis.get('device_model'):
                    device_analysis['all_detected_devices'].append(ua_analysis)
            
            # Method 2: Profile Metadata Analysis
            metadata_analysis = self._analyze_metadata(user)
            if metadata_analysis:
                device_analysis['metadata_analysis'] = metadata_analysis
                device_analysis['detection_methods'].append('Profile Metadata')
            
            # Method 3: App Version Detection
            app_version = self._extract_app_version(user)
            if app_version:
                device_analysis['app_version'] = app_version
            
            # Determine primary device
            if device_analysis['all_detected_devices']:
                primary = device_analysis['all_detected_devices'][0]
                device_analysis['primary_device'] = primary.get('device_model')
                device_analysis['device_brand'] = primary.get('brand')
                device_analysis['os_type'] = primary.get('os_type')
                device_analysis['os_version'] = primary.get('os_version')
                device_analysis['device_confidence'] = primary.get('confidence', 0.0)
            
            return device_analysis
        except Exception as e:
            print(f"Error analyzing device: {str(e)}")
            return None

    def _analyze_user_agent(self, user_agent: str) -> Dict:
        """Analyze user agent string to detect device"""
        analysis = {
            'raw_user_agent': user_agent,
            'device_model': None,
            'brand': None,
            'os_type': None,
            'os_version': None,
            'confidence': 0.0
        }
        
        if not user_agent:
            return analysis
        
        # iPhone detection
        if 'iPhone' in user_agent:
            analysis['os_type'] = 'iOS'
            analysis['brand'] = 'Apple'
            match = re.search(r'OS\s+([\d_]+)', user_agent)
            if match:
                analysis['os_version'] = match.group(1).replace('_', '.')
            
            if 'iPhone14' in user_agent:
                analysis['device_model'] = 'iPhone 14 Series'
                analysis['confidence'] = 0.95
            elif 'iPhone13' in user_agent:
                analysis['device_model'] = 'iPhone 13 Series'
                analysis['confidence'] = 0.95
            elif 'iPhone12' in user_agent:
                analysis['device_model'] = 'iPhone 12 Series'
                analysis['confidence'] = 0.95
            else:
                analysis['device_model'] = 'iPhone'
                analysis['confidence'] = 0.85
        
        # iPad detection
        elif 'iPad' in user_agent:
            analysis['os_type'] = 'iOS'
            analysis['brand'] = 'Apple'
            analysis['device_model'] = 'iPad'
            analysis['confidence'] = 0.9
        
        # Android detection
        elif 'Android' in user_agent:
            analysis['os_type'] = 'Android'
            match = re.search(r'Android\s+([\d\.]+)', user_agent)
            if match:
                analysis['os_version'] = match.group(1)
            
            if 'SM-' in user_agent:
                analysis['brand'] = 'Samsung'
                analysis['device_model'] = 'Samsung Galaxy'
                analysis['confidence'] = 0.95
            elif 'Pixel' in user_agent:
                analysis['brand'] = 'Google'
                analysis['device_model'] = 'Google Pixel'
                analysis['confidence'] = 0.95
            elif re.search(r'Mi\s*\d+|Redmi', user_agent, re.I):
                analysis['brand'] = 'Xiaomi'
                analysis['device_model'] = 'Xiaomi/Redmi'
                analysis['confidence'] = 0.9
            elif 'OnePlus' in user_agent:
                analysis['brand'] = 'OnePlus'
                analysis['device_model'] = 'OnePlus'
                analysis['confidence'] = 0.9
            elif 'OPPO' in user_agent or 'Find X' in user_agent:
                analysis['brand'] = 'Oppo'
                analysis['device_model'] = 'Oppo Find'
                analysis['confidence'] = 0.85
            else:
                analysis['device_model'] = 'Android Device'
                analysis['confidence'] = 0.7
        
        # Windows detection
        elif 'Windows' in user_agent:
            analysis['os_type'] = 'Windows'
            analysis['brand'] = 'Microsoft'
            analysis['device_model'] = 'Windows PC/Tablet'
            analysis['confidence'] = 0.85
        
        # macOS detection
        elif 'Macintosh' in user_agent or 'Mac OS' in user_agent:
            analysis['os_type'] = 'macOS'
            analysis['brand'] = 'Apple'
            analysis['device_model'] = 'Mac'
            analysis['confidence'] = 0.9
        
        return analysis

    def _analyze_metadata(self, user: Dict) -> Dict:
        """Analyze user profile metadata for device clues"""
        metadata = {
            'signature_contains_device_info': False,
            'device_mentions': [],
            'profile_indicators': []
        }
        
        signature = user.get('signature', '').lower()
        device_keywords = ['iphone', 'android', 'samsung', 'pixel', 'ipad', 'huawei', 'xiaomi', 'oneplus']
        
        for keyword in device_keywords:
            if keyword in signature:
                metadata['signature_contains_device_info'] = True
                metadata['device_mentions'].append(keyword)
        
        return metadata

    def _extract_app_version(self, user: Dict) -> Optional[str]:
        """Extract TikTok app version if available"""
        user_agent = user.get('userAgent', '')
        match = re.search(r'TikTok/([\d\.]+)', user_agent)
        return match.group(1) if match else None

    def batch_analyze_devices(self, usernames: List[str]) -> List[Dict]:
        """Analyze device models for multiple accounts"""
        results = []
        print(f"\n[DEVICE FINDER] Analyzing {len(usernames)} accounts...")
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] @{username}...", end=' ')
            analysis = self.analyze_account_info(username)
            if analysis:
                results.append(analysis)
                print(f"✓ {analysis.get('primary_device')}")
            else:
                print("✗")
        return results

    def generate_device_report(self, results: List[Dict]) -> Dict:
        """Generate comprehensive device analysis report"""
        report = {
            'total_accounts': len(results),
            'device_distribution': defaultdict(int),
            'os_distribution': defaultdict(int),
            'brand_distribution': defaultdict(int),
            'confidence_stats': {'high': 0, 'medium': 0, 'low': 0},
            'top_devices': []
        }
        
        for result in results:
            device = result.get('primary_device', 'Unknown')
            os_type = result.get('os_type', 'Unknown')
            brand = result.get('device_brand', 'Unknown')
            confidence = result.get('device_confidence', 0.0)
            
            report['device_distribution'][device] += 1
            report['os_distribution'][os_type] += 1
            report['brand_distribution'][brand] += 1
            
            if confidence > 0.8:
                report['confidence_stats']['high'] += 1
            elif confidence > 0.5:
                report['confidence_stats']['medium'] += 1
            else:
                report['confidence_stats']['low'] += 1
        
        report['top_devices'] = sorted(report['device_distribution'].items(), key=lambda x: x[1], reverse=True)[:10]
        return report

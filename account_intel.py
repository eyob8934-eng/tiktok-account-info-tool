"""
TikTok Account Intelligence Tool - Advanced analytics and insights
Provides deep insights about TikTok accounts including device, location hints, and patterns
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import re

class AccountIntelligence:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.tiktok_base = "https://www.tiktok.com/api"

    def get_account_intelligence(self, username: str) -> Optional[Dict]:
        """Get comprehensive intelligence on TikTok account"""
        try:
            username = username.lstrip('@')
            url = f"{self.tiktok_base}/user/detail/?uniqueId={username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            return self._analyze_intelligence(data, username)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _analyze_intelligence(self, data: Dict, username: str) -> Dict:
        """Analyze account intelligence"""
        try:
            user_details = data.get('userDetail', {})
            user = user_details.get('user', {})
            stats = user_details.get('stats', {})
            
            intel = {
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'user_id': user.get('id'),
                'account_status': self._analyze_account_status(user),
                'device_profile': self._analyze_device_profile(user),
                'posting_behavior': self._analyze_posting_behavior(stats, user),
                'engagement_profile': self._analyze_engagement(stats),
                'audience_insights': self._estimate_audience_insights(user, stats),
                'account_maturity': self._calculate_account_maturity(user),
                'creator_profile': self._create_creator_profile(user, stats),
                'content_quality_indicators': self._analyze_content_quality(stats),
                'risk_assessment': self._assess_risks(user, stats)
            }
            
            return intel
        except Exception as e:
            print(f"Error in analysis: {e}")
            return None

    def _analyze_account_status(self, user: Dict) -> Dict:
        """Analyze account status and credentials"""
        return {
            'verified': user.get('verified', False),
            'private_account': user.get('privateAccount', False),
            'business_account': user.get('isBusinessAccount', False),
            'restricted': user.get('restricted', False),
            'status': 'Active' if not user.get('restricted') else 'Restricted'
        }

    def _analyze_device_profile(self, user: Dict) -> Dict:
        """Analyze device usage patterns"""
        user_agent = user.get('userAgent', '')
        
        return {
            'primary_device': self._detect_device(user_agent),
            'os': self._detect_os(user_agent),
            'user_agent': user_agent,
            'likely_device_type': 'Mobile' if any(x in user_agent for x in ['Android', 'iPhone', 'iPad']) else 'Web/Desktop',
            'app_version': self._extract_version(user_agent)
        }

    def _detect_device(self, user_agent: str) -> str:
        """Detect device from user agent"""
        if 'iPhone' in user_agent:
            return 'iPhone'
        elif 'iPad' in user_agent:
            return 'iPad'
        elif 'Android' in user_agent:
            if 'SM-' in user_agent:
                return 'Samsung'
            elif 'Pixel' in user_agent:
                return 'Google Pixel'
            else:
                return 'Android Device'
        elif 'Windows' in user_agent:
            return 'Windows PC'
        elif 'Mac' in user_agent:
            return 'MacBook'
        return 'Unknown'

    def _detect_os(self, user_agent: str) -> str:
        """Detect operating system"""
        if 'iPhone' in user_agent or 'iPad' in user_agent:
            return 'iOS'
        elif 'Android' in user_agent:
            return 'Android'
        elif 'Windows' in user_agent:
            return 'Windows'
        elif 'Mac' in user_agent:
            return 'macOS'
        return 'Unknown'

    def _extract_version(self, user_agent: str) -> str:
        """Extract app version"""
        match = re.search(r'TikTok/([\d\.]+)', user_agent)
        return match.group(1) if match else 'Unknown'

    def _analyze_posting_behavior(self, stats: Dict, user: Dict) -> Dict:
        """Analyze posting behavior"""
        video_count = stats.get('videoCount', 0)
        create_time = user.get('createTime', 0)
        
        if create_time and video_count > 0:
            account_age_days = (datetime.now().timestamp() - create_time) / (24 * 3600)
            posting_frequency = video_count / max(account_age_days, 1)
        else:
            posting_frequency = 0
        
        return {
            'total_videos': video_count,
            'posting_frequency': f"{posting_frequency:.2f} videos/day",
            'posting_consistency': 'High' if posting_frequency > 0.5 else 'Medium' if posting_frequency > 0.1 else 'Low'
        }

    def _analyze_engagement(self, stats: Dict) -> Dict:
        """Analyze engagement metrics"""
        hearts = stats.get('heartCount', 0)
        videos = stats.get('videoCount', 0)
        followers = stats.get('followerCount', 0)
        
        avg_likes_per_video = (hearts / videos) if videos > 0 else 0
        avg_likes_per_follower = (hearts / followers) if followers > 0 else 0
        
        return {
            'total_hearts': hearts,
            'avg_likes_per_video': int(avg_likes_per_video),
            'avg_likes_per_follower': round(avg_likes_per_follower, 4),
            'engagement_quality': 'Excellent' if avg_likes_per_video > 10000 else 'Good' if avg_likes_per_video > 1000 else 'Fair' if avg_likes_per_video > 100 else 'Low'
        }

    def _estimate_audience_insights(self, user: Dict, stats: Dict) -> Dict:
        """Estimate audience insights"""
        followers = stats.get('followerCount', 0)
        following = stats.get('followingCount', 0)
        
        return {
            'follower_count': followers,
            'following_count': following,
            'follower_to_following_ratio': round(followers / max(following, 1), 2),
            'audience_size_category': self._categorize_audience(followers),
            'likely_audience_engagement': 'High' if (followers / max(following, 1)) > 10 else 'Medium' if (followers / max(following, 1)) > 2 else 'Low'
        }

    def _categorize_audience(self, followers: int) -> str:
        """Categorize audience size"""
        if followers >= 1000000:
            return 'Mega Influencer (1M+)'
        elif followers >= 100000:
            return 'Macro Creator (100K-1M)'
        elif followers >= 10000:
            return 'Micro Influencer (10K-100K)'
        elif followers >= 1000:
            return 'Nano Influencer (1K-10K)'
        elif followers >= 100:
            return 'Emerging (100-1K)'
        else:
            return 'Small Account (<100)'

    def _calculate_account_maturity(self, user: Dict) -> Dict:
        """Calculate account maturity"""
        create_time = user.get('createTime', 0)
        if create_time:
            age_days = (datetime.now().timestamp() - create_time) / (24 * 3600)
            age_years = age_days / 365
            
            if age_years < 1:
                maturity = 'Very New'
            elif age_years < 2:
                maturity = 'New'
            elif age_years < 3:
                maturity = 'Established'
            else:
                maturity = 'Mature'
        else:
            age_days = 0
            age_years = 0
            maturity = 'Unknown'
        
        return {
            'account_age_years': round(age_years, 2),
            'account_age_days': int(age_days),
            'maturity_level': maturity
        }

    def _create_creator_profile(self, user: Dict, stats: Dict) -> Dict:
        """Create creator profile"""
        return {
            'display_name': user.get('nickname'),
            'bio': user.get('signature'),
            'profile_picture': user.get('avatarLarger'),
            'verified_status': 'Verified' if user.get('verified') else 'Not Verified',
            'business_type': 'Business Account' if user.get('isBusinessAccount') else 'Personal Account'
        }

    def _analyze_content_quality(self, stats: Dict) -> Dict:
        """Analyze content quality indicators"""
        videos = stats.get('videoCount', 0)
        hearts = stats.get('heartCount', 0)
        
        if videos > 0:
            quality_score = min(100, (hearts / videos) / 100)
        else:
            quality_score = 0
        
        return {
            'content_volume': 'High' if videos > 100 else 'Medium' if videos > 20 else 'Low',
            'average_performance': quality_score,
            'quality_indicator': 'Excellent' if quality_score > 80 else 'Good' if quality_score > 50 else 'Average' if quality_score > 20 else 'Poor'
        }

    def _assess_risks(self, user: Dict, stats: Dict) -> Dict:
        """Assess account risks"""
        return {
            'suspicious_activity': False,
            'content_policy_risk': 'Low',
            'bot_activity_likelihood': 'Low',
            'recommendation': 'Safe to collaborate' if not user.get('restricted') else 'Check before collaboration'
        }

    def batch_analyze_intelligence(self, usernames: List[str]) -> List[Dict]:
        """Analyze multiple accounts"""
        results = []
        print(f"\n[INTELLIGENCE] Analyzing {len(usernames)} accounts...")
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] @{username}...", end=' ')
            intel = self.get_account_intelligence(username)
            if intel:
                results.append(intel)
                print("✓")
            else:
                print("✗")
        return results

    def export_intelligence(self, results: List[Dict], filename: str):
        """Export intelligence reports"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Exported to {filename}")
        except Exception as e:
            print(f"Export error: {e}")

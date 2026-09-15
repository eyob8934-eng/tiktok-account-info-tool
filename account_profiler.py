"""
TikTok Account Profiler - Comprehensive account analysis
Provides detailed information about TikTok account creation, activity, and device
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

class TikTokAccountProfiler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_complete_profile(self, username: str) -> Optional[Dict]:
        """Get complete account profile with all details"""
        try:
            username = username.lstrip('@')
            url = f"https://www.tiktok.com/api/user/detail/?uniqueId={username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            return self._extract_profile_data(data, username)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _extract_profile_data(self, data: Dict, username: str) -> Dict:
        """Extract comprehensive profile data"""
        try:
            user_details = data.get('userDetail', {})
            user = user_details.get('user', {})
            stats = user_details.get('stats', {})
            
            # Account dates
            create_time = user.get('createTime', 0)
            creation_date = datetime.fromtimestamp(create_time) if create_time else None
            
            # Calculate account age
            account_age = None
            if creation_date:
                account_age = (datetime.now() - creation_date).days
            
            # Calculate engagement metrics
            videos = stats.get('videoCount', 0)
            followers = stats.get('followerCount', 0)
            following = stats.get('followingCount', 0)
            hearts = stats.get('heartCount', 0)
            
            engagement_rate = 0
            if videos > 0:
                engagement_rate = (hearts / videos) if videos > 0 else 0
            
            follower_engagement = 0
            if followers > 0:
                follower_engagement = (hearts / followers) if followers > 0 else 0
            
            profile = {
                # Basic Info
                'username': username,
                'user_id': user.get('id'),
                'display_name': user.get('nickname'),
                'avatar_url': user.get('avatarLarger'),
                'bio': user.get('signature'),
                
                # Account Status
                'verified': user.get('verified', False),
                'private': user.get('privateAccount', False),
                'business_account': user.get('isBusinessAccount', False),
                'badge_count': len(user.get('badges', [])),
                
                # Dates & Age
                'account_creation_date': str(creation_date) if creation_date else 'Unknown',
                'account_creation_timestamp': create_time,
                'account_age_days': account_age,
                'account_age_years': round(account_age / 365, 2) if account_age else None,
                
                # Statistics
                'follower_count': followers,
                'following_count': following,
                'video_count': videos,
                'heart_count': hearts,
                'engagement_rate': round(engagement_rate, 2),
                'follower_engagement_rate': round(follower_engagement, 4),
                
                # Activity Analysis
                'videos_per_day': round(videos / account_age, 2) if account_age and account_age > 0 else 0,
                'followers_per_day': round(followers / account_age, 2) if account_age and account_age > 0 else 0,
                'hearts_per_video': round(hearts / videos, 0) if videos > 0 else 0,
                'follower_to_following_ratio': round(followers / following, 2) if following > 0 else 0,
                
                # Device Info
                'device_info': self._extract_device_info(user),
                
                # Account Type Classification
                'account_type': self._classify_account_type(followers, videos, engagement_rate),
                'growth_potential': self._assess_growth_potential(followers, engagement_rate, account_age),
                'authenticity_score': self._calculate_authenticity_score(followers, following, verified=user.get('verified')),
            }
            
            return profile
        except Exception as e:
            print(f"Error extracting profile: {e}")
            return None

    def _extract_device_info(self, user: Dict) -> Dict:
        """Extract device information"""
        user_agent = user.get('userAgent', '')
        
        device_info = {
            'raw_user_agent': user_agent,
            'device_type': 'Unknown',
            'device_os': 'Unknown'
        }
        
        if 'iPhone' in user_agent:
            device_info['device_type'] = 'iPhone'
            device_info['device_os'] = 'iOS'
        elif 'iPad' in user_agent:
            device_info['device_type'] = 'iPad'
            device_info['device_os'] = 'iOS'
        elif 'Android' in user_agent:
            device_info['device_type'] = 'Android'
            device_info['device_os'] = 'Android'
        elif 'Windows' in user_agent:
            device_info['device_type'] = 'Windows PC'
            device_info['device_os'] = 'Windows'
        elif 'Mac' in user_agent:
            device_info['device_type'] = 'Mac'
            device_info['device_os'] = 'macOS'
        
        return device_info

    def _classify_account_type(self, followers: int, videos: int, engagement_rate: float) -> str:
        """Classify account type based on metrics"""
        if followers > 1000000:
            return 'Mega Influencer'
        elif followers > 100000:
            return 'Macro Influencer'
        elif followers > 10000:
            return 'Micro Influencer'
        elif followers > 1000:
            return 'Nano Influencer'
        elif followers > 100:
            return 'Emerging Creator'
        else:
            return 'New Account'

    def _assess_growth_potential(self, followers: int, engagement_rate: float, account_age: Optional[int]) -> str:
        """Assess growth potential of account"""
        if engagement_rate > 0.1:
            return 'High Growth Potential'
        elif engagement_rate > 0.05:
            return 'Moderate Growth Potential'
        elif engagement_rate > 0.01:
            return 'Low Growth Potential'
        else:
            return 'Minimal Growth Potential'

    def _calculate_authenticity_score(self, followers: int, following: int, verified: bool) -> float:
        """Calculate authenticity score (0-100)"""
        score = 50
        
        if verified:
            score += 20
        
        if followers > 0 and following > 0:
            ratio = followers / following
            if 0.5 < ratio < 100:
                score += 20
            else:
                score -= 10
        
        if followers > 10000:
            score += 10
        
        return min(100, max(0, score))

    def batch_profile_accounts(self, usernames: List[str]) -> List[Dict]:
        """Get profiles for multiple accounts"""
        profiles = []
        print(f"\n[PROFILER] Analyzing {len(usernames)} accounts...")
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] @{username}...", end=' ')
            profile = self.get_complete_profile(username)
            if profile:
                profiles.append(profile)
                print(f"✓")
            else:
                print("✗")
        return profiles

    def export_profiles(self, profiles: List[Dict], filename: str):
        """Export profiles to JSON"""
        try:
            with open(filename, 'w') as f:
                json.dump(profiles, f, indent=2)
            print(f"Exported to {filename}")
        except Exception as e:
            print(f"Export error: {e}")

    def generate_comparison_report(self, profiles: List[Dict]) -> str:
        """Generate comparison report for multiple accounts"""
        if not profiles:
            return "No profiles to compare"
        
        report = "\n" + "=" * 80 + "\n"
        report += "TIKTOK ACCOUNT COMPARISON REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"Total Accounts: {len(profiles)}\n\n"
        
        # Create comparison table
        report += f"{'Username':<20} {'Followers':<15} {'Videos':<10} {'Engagement':<15} {'Account Type':<20}\n"
        report += "-" * 80 + "\n"
        
        for p in profiles:
            report += f"{p['username']:<20} {p['follower_count']:<15,} {p['video_count']:<10} {p['engagement_rate']:<15.2%} {p['account_type']:<20}\n"
        
        report += "\n" + "=" * 80 + "\n"
        return report

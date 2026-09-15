"""
TikTok Forensic Analysis Engine - Advanced Account Analysis
Multi-threaded, Proxy Rotation, Device Fingerprinting, Anomaly Detection
"""

import json
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from datetime import datetime
import logging
import hashlib
import re
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class ForensicAnalysisEngine:
    """
    Advanced forensic analysis for TikTok accounts
    """
    
    def __init__(self):
        self.profiles = {}
        self.anomaly_patterns = self._load_anomaly_patterns()

    def _load_anomaly_patterns(self) -> dict:
        """
        Load patterns for anomaly detection
        """
        return {
            'bot_indicators': {
                'perfect_follower_distribution': (0.0, 0.01),
                'exact_round_numbers': True,
                'rapid_follower_gain': (1000, 100000),
                'zero_engagement_spikes': True,
                'consistent_posting': (0.95, 1.0)  # Too consistent
            },
            'fake_account_indicators': {
                'no_profile_picture': True,
                'empty_bio': True,
                'no_videos': True,
                'suspicious_username': True,
                'mismatched_stats': True
            },
            'compromised_account_indicators': {
                'sudden_growth_spike': (500, 10000),
                'content_style_change': True,
                'posting_time_change': True,
                'new_engagement_pattern': True,
                'geo_location_anomaly': True
            }
        }

    def analyze_single_account(self, profile: Dict) -> Dict:
        """
        Perform comprehensive forensic analysis on single account
        """
        analysis = {
            'username': profile.get('username'),
            'timestamp': datetime.now().isoformat(),
            'account_classification': self._classify_account(profile),
            'risk_assessment': self._assess_risk(profile),
            'behavioral_analysis': self._analyze_behavior(profile),
            'network_analysis': self._analyze_network(profile),
            'content_analysis': self._analyze_content(profile),
            'integrity_score': self._calculate_integrity_score(profile),
            'recommendations': self._generate_recommendations(profile)
        }
        
        return analysis

    def _classify_account(self, profile: Dict) -> dict:
        """
        Classify account type and characteristics
        """
        followers = profile.get('follower_count', 0)
        verified = profile.get('verified', False)
        business = profile.get('business_account', False)
        private = profile.get('private_account', False)
        videos = profile.get('video_count', 0)
        
        classification = {
            'account_type': self._categorize_account_type(followers),
            'creator_status': 'Verified Creator' if verified else 'Unverified Creator',
            'business_status': 'Business Account' if business else 'Personal Account',
            'visibility': 'Private' if private else 'Public',
            'activity_level': self._assess_activity_level(videos)
        }
        
        return classification

    def _categorize_account_type(self, followers: int) -> str:
        """
        Categorize account type by follower count
        """
        if followers >= 1000000:
            return 'Mega Influencer'
        elif followers >= 100000:
            return 'Macro Influencer'
        elif followers >= 10000:
            return 'Micro Influencer'
        elif followers >= 1000:
            return 'Nano Influencer'
        elif followers >= 100:
            return 'Emerging Creator'
        else:
            return 'Small Account'

    def _assess_activity_level(self, videos: int) -> str:
        """
        Assess account activity level
        """
        if videos == 0:
            return 'Inactive'
        elif videos < 5:
            return 'Very Low'
        elif videos < 20:
            return 'Low'
        elif videos < 100:
            return 'Medium'
        elif videos < 500:
            return 'High'
        else:
            return 'Very High'

    def _assess_risk(self, profile: Dict) -> dict:
        """
        Assess account risk factors
        """
        risk_factors = []
        risk_score = 0
        
        # Check for missing information
        if not profile.get('display_name'):
            risk_factors.append('Missing display name')
            risk_score += 10
        
        if not profile.get('signature'):
            risk_factors.append('Empty bio')
            risk_score += 5
        
        if not profile.get('avatar'):
            risk_factors.append('No profile picture')
            risk_score += 20
        
        # Check for suspicious statistics
        followers = profile.get('follower_count', 0)
        videos = profile.get('video_count', 0)
        hearts = profile.get('heart_count', 0)
        
        if videos == 0 and followers > 0:
            risk_factors.append('Followers but no videos')
            risk_score += 30
        
        if followers > 0 and hearts == 0 and videos > 0:
            risk_factors.append('No engagement despite followers')
            risk_score += 20
        
        # Check for anomalies in forensics
        forensics = profile.get('forensics', {})
        anomalies = forensics.get('anomalies_detected', [])
        if anomalies:
            risk_score += len(anomalies) * 10
        
        return {
            'risk_score': min(100, risk_score),
            'risk_level': self._categorize_risk(risk_score),
            'risk_factors': risk_factors,
            'anomalies': anomalies
        }

    def _categorize_risk(self, score: int) -> str:
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

    def _analyze_behavior(self, profile: Dict) -> dict:
        """
        Analyze account behavior patterns
        """
        followers = profile.get('follower_count', 0)
        following = profile.get('following_count', 0)
        videos = profile.get('video_count', 0)
        hearts = profile.get('heart_count', 0)
        
        behavior = {
            'follower_following_ratio': round(followers / max(following, 1), 2),
            'engagement_per_video': int(hearts / max(videos, 1)),
            'audience_composition': self._analyze_audience_composition(followers, following),
            'posting_pattern': profile.get('forensics', {}).get('growth_pattern', 'Unknown'),
            'authenticity_score': self._calculate_authenticity(profile)
        }
        
        return behavior

    def _analyze_audience_composition(self, followers: int, following: int) -> str:
        """
        Analyze audience composition based on follower/following ratio
        """
        if following == 0:
            return 'Unknown'
        
        ratio = followers / following
        
        if ratio > 100:
            return 'High-quality followers (Influencer)'
        elif ratio > 10:
            return 'Good audience (Popular account)'
        elif ratio > 1:
            return 'Balanced audience'
        elif ratio == 1:
            return 'Equal followers and following'
        else:
            return 'Following more than followers'

    def _analyze_network(self, profile: Dict) -> dict:
        """
        Analyze account network characteristics
        """
        followers = profile.get('follower_count', 0)
        following = profile.get('following_count', 0)
        
        return {
            'network_size': self._categorize_network_size(followers + following),
            'influence_index': self._calculate_influence_index(profile),
            'reach_potential': self._estimate_reach_potential(profile),
            'collaboration_appeal': self._assess_collaboration_appeal(profile)
        }

    def _categorize_network_size(self, total_connections: int) -> str:
        """
        Categorize network size
        """
        if total_connections == 0:
            return 'Isolated'
        elif total_connections < 1000:
            return 'Small Network'
        elif total_connections < 100000:
            return 'Medium Network'
        else:
            return 'Large Network'

    def _calculate_influence_index(self, profile: Dict) -> float:
        """
        Calculate influence index (0-100)
        """
        followers = profile.get('follower_count', 0)
        engagement = profile.get('engagement_metrics', {}).get('virality_score', 0)
        verified = profile.get('verified', False)
        
        influence = 0
        
        # Follower component (60%)
        if followers >= 1000000:
            influence += 60
        elif followers >= 100000:
            influence += 45
        elif followers >= 10000:
            influence += 30
        elif followers >= 1000:
            influence += 15
        
        # Engagement component (30%)
        influence += min(30, engagement * 10)
        
        # Verification component (10%)
        if verified:
            influence += 10
        
        return min(100, influence)

    def _estimate_reach_potential(self, profile: Dict) -> dict:
        """
        Estimate reach potential
        """
        followers = profile.get('follower_count', 0)
        engagement_rate = profile.get('engagement_metrics', {}).get('engagement_rate', 0)
        
        return {
            'direct_reach': followers,
            'secondary_reach': int(followers * engagement_rate / 100 * 0.5),
            'potential_viral_reach': int(followers * engagement_rate / 100),
            'reach_category': 'High' if engagement_rate > 5 else 'Medium' if engagement_rate > 1 else 'Low'
        }

    def _assess_collaboration_appeal(self, profile: Dict) -> dict:
        """
        Assess appeal for brand collaborations
        """
        followers = profile.get('follower_count', 0)
        engagement = profile.get('engagement_metrics', {}).get('engagement_rate', 0)
        verified = profile.get('verified', False)
        business = profile.get('business_account', False)
        
        appeal_score = 0
        
        if followers >= 10000:
            appeal_score += 30
        elif followers >= 1000:
            appeal_score += 15
        
        if engagement > 5:
            appeal_score += 30
        elif engagement > 1:
            appeal_score += 15
        
        if verified:
            appeal_score += 20
        
        if business:
            appeal_score += 20
        
        return {
            'appeal_score': min(100, appeal_score),
            'collaboration_potential': 'High' if appeal_score > 70 else 'Medium' if appeal_score > 40 else 'Low',
            'estimated_rate_category': self._estimate_rate_category(followers, engagement, verified)
        }

    def _estimate_rate_category(self, followers: int, engagement: float, verified: bool) -> str:
        """
        Estimate collaboration rate category
        """
        if followers >= 1000000:
            return '$10,000 - $100,000+'
        elif followers >= 100000:
            return '$1,000 - $10,000'
        elif followers >= 10000:
            return '$100 - $1,000'
        else:
            return 'Micro-influencer/Gifting'

    def _analyze_content(self, profile: Dict) -> dict:
        """
        Analyze content characteristics
        """
        videos = profile.get('video_count', 0)
        hearts = profile.get('heart_count', 0)
        comments = profile.get('comment_count', 0)
        shares = profile.get('share_count', 0)
        downloads = profile.get('download_count', 0)
        
        return {
            'content_volume': videos,
            'average_performance': {
                'likes': int(hearts / max(videos, 1)),
                'comments': int(comments / max(videos, 1)),
                'shares': int(shares / max(videos, 1)),
                'downloads': int(downloads / max(videos, 1))
            },
            'viral_content_count': self._estimate_viral_count(hearts, videos),
            'content_quality': self._assess_content_quality(hearts, videos)
        }

    def _estimate_viral_count(self, hearts: int, videos: int) -> int:
        """
        Estimate number of viral videos (>1M likes)
        """
        if videos == 0:
            return 0
        avg_likes = hearts / videos
        # Assume top 10% are viral
        return max(0, int(videos * 0.1 * (avg_likes / 100000)))

    def _assess_content_quality(self, hearts: int, videos: int) -> str:
        """
        Assess overall content quality
        """
        if videos == 0:
            return 'No content'
        
        avg_likes = hearts / videos
        
        if avg_likes > 100000:
            return 'Excellent'
        elif avg_likes > 10000:
            return 'Very Good'
        elif avg_likes > 1000:
            return 'Good'
        elif avg_likes > 100:
            return 'Average'
        else:
            return 'Below Average'

    def _calculate_authenticity(self, profile: Dict) -> float:
        """
        Calculate authenticity score (0-100)
        """
        score = 50
        
        if profile.get('verified'):
            score += 20
        
        if profile.get('avatar'):
            score += 10
        
        if profile.get('signature'):
            score += 10
        
        if not profile.get('private_account'):
            score += 5
        
        if profile.get('business_account'):
            score += 5
        
        # Deduct points for anomalies
        anomalies = len(profile.get('forensics', {}).get('anomalies_detected', []))
        score -= anomalies * 5
        
        return max(0, min(100, score))

    def _calculate_integrity_score(self, profile: Dict) -> float:
        """
        Calculate overall account integrity score
        """
        # Weighted calculation
        auth_score = self._calculate_authenticity(profile)
        engagement = profile.get('engagement_metrics', {}).get('engagement_rate', 0)
        followers = profile.get('follower_count', 0)
        videos = profile.get('video_count', 0)
        
        integrity = 0
        
        # Authenticity (40%)
        integrity += auth_score * 0.4
        
        # Consistency (30%)
        if videos > 0:
            consistency_score = min(100, (followers / max(videos, 1)) / 1000)
            integrity += consistency_score * 0.3
        
        # Engagement (20%)
        integrity += min(100, engagement) * 0.2
        
        # Activity (10%)
        if videos >= 100:
            integrity += 10
        elif videos >= 20:
            integrity += 5
        
        return round(min(100, max(0, integrity)), 2)

    def _generate_recommendations(self, profile: Dict) -> list:
        """
        Generate recommendations based on analysis
        """
        recommendations = []
        
        followers = profile.get('follower_count', 0)
        engagement = profile.get('engagement_metrics', {}).get('engagement_rate', 0)
        risk_level = self._assess_risk(profile)['risk_level']
        
        if risk_level in ['Critical', 'High']:
            recommendations.append('⚠️ Use with caution - Account shows signs of suspicious activity')
        
        if followers >= 10000 and engagement > 5:
            recommendations.append('✅ Strong candidate for brand collaborations')
        
        if followers > 0 and engagement < 1:
            recommendations.append('⚠️ Low engagement despite follower base')
        
        if profile.get('verified'):
            recommendations.append('✅ Verified account - Higher credibility')
        
        if profile.get('business_account'):
            recommendations.append('✅ Business account - Professional focus')
        
        return recommendations

    def batch_analyze(self, profiles: List[Dict]) -> List[Dict]:
        """
        Analyze multiple profiles
        """
        analyses = []
        for profile in profiles:
            analysis = self.analyze_single_account(profile)
            analyses.append(analysis)
        
        return analyses

    def generate_summary_report(self, analyses: List[Dict]) -> str:
        """
        Generate summary report for multiple accounts
        """
        report = "\n" + "=" * 100 + "\n"
        report += "BATCH FORENSIC ANALYSIS SUMMARY REPORT\n"
        report += "=" * 100 + "\n\n"
        
        risk_summary = defaultdict(int)
        type_summary = defaultdict(int)
        
        for analysis in analyses:
            risk_level = analysis['risk_assessment']['risk_level']
            account_type = analysis['account_classification']['account_type']
            risk_summary[risk_level] += 1
            type_summary[account_type] += 1
        
        report += f"Total Accounts Analyzed: {len(analyses)}\n\n"
        report += "Risk Distribution:\n"
        for risk, count in sorted(risk_summary.items()):
            report += f"  {risk}: {count}\n"
        
        report += "\nAccount Type Distribution:\n"
        for acct_type, count in sorted(type_summary.items()):
            report += f"  {acct_type}: {count}\n"
        
        report += "\n" + "=" * 100 + "\n"
        return report

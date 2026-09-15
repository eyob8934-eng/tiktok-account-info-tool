"""
Comparative Analysis Tool - Compare multiple TikTok accounts side-by-side
Advanced metrics, growth patterns, and account health assessment
"""

import json
from typing import Dict, List
from datetime import datetime
from collections import defaultdict

class ComparativeAnalysisTool:
    """
    Tool for comparing multiple TikTok accounts
    """
    
    def __init__(self):
        self.accounts = {}
        self.metrics_cache = {}

    def add_profile(self, profile: Dict):
        """
        Add profile for comparison
        """
        username = profile.get('username')
        self.accounts[username] = profile
        self.metrics_cache.clear()  # Clear cache when new profile added

    def add_profiles_batch(self, profiles: List[Dict]):
        """
        Add multiple profiles
        """
        for profile in profiles:
            self.add_profile(profile)

    def compare_accounts(self, usernames: List[str]) -> Dict:
        """
        Compare specific accounts
        """
        comparison = {
            'comparison_time': datetime.now().isoformat(),
            'accounts_compared': usernames,
            'total_accounts': len(usernames),
            'account_details': {},
            'comparative_metrics': {},
            'rankings': {}
        }
        
        # Get details for each account
        for username in usernames:
            if username in self.accounts:
                comparison['account_details'][username] = self._extract_key_metrics(self.accounts[username])
        
        # Calculate comparative metrics
        comparison['comparative_metrics'] = self._calculate_comparative_metrics(usernames)
        
        # Generate rankings
        comparison['rankings'] = self._generate_rankings(usernames)
        
        return comparison

    def _extract_key_metrics(self, profile: Dict) -> Dict:
        """
        Extract key metrics from profile
        """
        return {
            'username': profile.get('username'),
            'display_name': profile.get('display_name'),
            'verified': profile.get('verified'),
            'followers': profile.get('follower_count'),
            'following': profile.get('following_count'),
            'videos': profile.get('video_count'),
            'hearts': profile.get('heart_count'),
            'engagement_rate': profile.get('engagement_metrics', {}).get('engagement_rate'),
            'virality_score': profile.get('engagement_metrics', {}).get('virality_score'),
            'device': profile.get('device_info', {}).get('type'),
            'integrity_score': profile.get('forensics', {}).get('risk_score')
        }

    def _calculate_comparative_metrics(self, usernames: List[str]) -> Dict:
        """
        Calculate metrics comparing accounts
        """
        metrics = {
            'follower_comparison': {},
            'engagement_comparison': {},
            'activity_comparison': {},
            'quality_comparison': {},
            'growth_comparison': {}
        }
        
        # Extract data
        data_points = {}
        for username in usernames:
            if username in self.accounts:
                profile = self.accounts[username]
                data_points[username] = {
                    'followers': profile.get('follower_count', 0),
                    'engagement_rate': profile.get('engagement_metrics', {}).get('engagement_rate', 0),
                    'videos': profile.get('video_count', 0),
                    'hearts': profile.get('heart_count', 0),
                    'virality': profile.get('engagement_metrics', {}).get('virality_score', 0)
                }
        
        # Calculate comparisons
        if data_points:
            # Follower comparison
            max_followers = max(dp['followers'] for dp in data_points.values())
            for username, data in data_points.items():
                metrics['follower_comparison'][username] = {
                    'count': data['followers'],
                    'rank': self._rank_by_value(data_points, 'followers', username),
                    'percentage_of_max': round(data['followers'] / max(max_followers, 1) * 100, 2)
                }
            
            # Engagement comparison
            max_engagement = max(dp['engagement_rate'] for dp in data_points.values())
            for username, data in data_points.items():
                metrics['engagement_comparison'][username] = {
                    'rate': data['engagement_rate'],
                    'rank': self._rank_by_value(data_points, 'engagement_rate', username),
                    'percentage_of_max': round(data['engagement_rate'] / max(max_engagement, 0.01) * 100, 2)
                }
            
            # Activity comparison
            max_videos = max(dp['videos'] for dp in data_points.values())
            for username, data in data_points.items():
                avg_hearts = data['hearts'] / max(data['videos'], 1)
                metrics['activity_comparison'][username] = {
                    'videos': data['videos'],
                    'rank': self._rank_by_value(data_points, 'videos', username),
                    'avg_hearts_per_video': int(avg_hearts)
                }
        
        return metrics

    def _rank_by_value(self, data_points: Dict, metric: str, username: str) -> int:
        """
        Rank account by specific metric
        """
        values = sorted(
            [(u, dp[metric]) for u, dp in data_points.items()],
            key=lambda x: x[1],
            reverse=True
        )
        for rank, (u, _) in enumerate(values, 1):
            if u == username:
                return rank
        return 0

    def _generate_rankings(self, usernames: List[str]) -> Dict:
        """
        Generate rankings across multiple metrics
        """
        rankings = {
            'followers_ranking': [],
            'engagement_ranking': [],
            'activity_ranking': [],
            'overall_ranking': []
        }
        
        # Followers ranking
        follower_sorted = sorted(
            [(u, self.accounts[u].get('follower_count', 0)) for u in usernames if u in self.accounts],
            key=lambda x: x[1],
            reverse=True
        )
        rankings['followers_ranking'] = [{'rank': i+1, 'username': u, 'count': c} for i, (u, c) in enumerate(follower_sorted)]
        
        # Engagement ranking
        engagement_sorted = sorted(
            [(u, self.accounts[u].get('engagement_metrics', {}).get('engagement_rate', 0)) for u in usernames if u in self.accounts],
            key=lambda x: x[1],
            reverse=True
        )
        rankings['engagement_ranking'] = [{'rank': i+1, 'username': u, 'rate': e} for i, (u, e) in enumerate(engagement_sorted)]
        
        # Activity ranking
        activity_sorted = sorted(
            [(u, self.accounts[u].get('video_count', 0)) for u in usernames if u in self.accounts],
            key=lambda x: x[1],
            reverse=True
        )
        rankings['activity_ranking'] = [{'rank': i+1, 'username': u, 'videos': v} for i, (u, v) in enumerate(activity_sorted)]
        
        return rankings

    def generate_comparison_report(self, usernames: List[str]) -> str:
        """
        Generate detailed comparison report
        """
        comparison = self.compare_accounts(usernames)
        
        report = "\n" + "=" * 120 + "\n"
        report += "TIKTOK ACCOUNTS COMPARATIVE ANALYSIS REPORT\n"
        report += "=" * 120 + "\n\n"
        
        report += f"Comparison Time: {comparison['comparison_time']}\n"
        report += f"Accounts Compared: {', '.join(usernames)}\n\n"
        
        # Followers ranking
        report += "FOLLOWERS RANKING:\n"
        report += "-" * 80 + "\n"
        for item in comparison['rankings']['followers_ranking']:
            report += f"  {item['rank']}. @{item['username']}: {item['count']:,} followers\n"
        report += "\n"
        
        # Engagement ranking
        report += "ENGAGEMENT RATE RANKING:\n"
        report += "-" * 80 + "\n"
        for item in comparison['rankings']['engagement_ranking']:
            report += f"  {item['rank']}. @{item['username']}: {item['rate']}%\n"
        report += "\n"
        
        # Activity ranking
        report += "ACTIVITY (VIDEOS) RANKING:\n"
        report += "-" * 80 + "\n"
        for item in comparison['rankings']['activity_ranking']:
            report += f"  {item['rank']}. @{item['username']}: {item['videos']} videos\n"
        report += "\n"
        
        # Detailed metrics
        report += "DETAILED METRICS COMPARISON:\n"
        report += "-" * 120 + "\n"
        report += f"{'Username':<20} {'Followers':<15} {'Engagement':<15} {'Videos':<10} {'Hearts':<15}\n"
        report += "-" * 120 + "\n"
        
        for username in usernames:
            if username in comparison['account_details']:
                detail = comparison['account_details'][username]
                report += f"{username:<20} {detail['followers']:<15,} {detail['engagement_rate']:<15}% {detail['videos']:<10} {detail['hearts']:<15,}\n"
        
        report += "\n" + "=" * 120 + "\n"
        return report

    def export_comparison(self, usernames: List[str], filename: str):
        """
        Export comparison to JSON
        """
        comparison = self.compare_accounts(usernames)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(comparison, f, indent=2, ensure_ascii=False)
            print(f"Comparison exported to {filename}")
        except Exception as e:
            print(f"Export error: {e}")

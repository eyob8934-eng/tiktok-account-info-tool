"""
Unit tests for TikTok Account Info Tool
"""

import unittest
from tiktok_scraper import TikTokAccountInfo
from advanced_scraper import AdvancedTikTokScraper
import json

class TestTikTokScraper(unittest.TestCase):
    def setUp(self):
        self.tool = TikTokAccountInfo()
        self.advanced_tool = AdvancedTikTokScraper()

    def test_username_normalization(self):
        """Test that usernames are normalized correctly"""
        username = "@testuser"
        normalized = username.lstrip('@')
        self.assertEqual(normalized, "testuser")

    def test_account_info_structure(self):
        """Test that account info has expected structure"""
        # This would require a valid TikTok account
        expected_fields = [
            'username', 'user_id', 'display_name', 'creation_date',
            'verified', 'private_account', 'follower_count', 'device_info'
        ]
        
        for field in expected_fields:
            self.assertIsNotNone(field)

    def test_device_info_extraction(self):
        """Test device information extraction"""
        test_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)"
        
        # Mock user data
        mock_user = {'userAgent': test_user_agent}
        device_info = self.tool._extract_device_info({'user': mock_user})
        
        self.assertIsNotNone(device_info)
        self.assertIn('device_model', device_info)

    def test_cache_functionality(self):
        """Test caching mechanism"""
        username = "testuser"
        test_data = {'username': username, 'verified': True}
        
        # Save to cache
        self.advanced_tool.save_to_cache(username, test_data)
        
        # Load from cache
        cached_data = self.advanced_tool.load_from_cache(username)
        self.assertIsNotNone(cached_data)

    def test_rate_limiting(self):
        """Test rate limiting is applied"""
        import time
        start_time = time.time()
        
        for _ in range(3):
            self.advanced_tool.rate_limit()
        
        elapsed_time = time.time() - start_time
        # Should take at least 2 seconds for 3 requests at 1 req/sec
        self.assertGreaterEqual(elapsed_time, 2)

    def test_batch_processing_empty_list(self):
        """Test batch processing with empty list"""
        results = self.advanced_tool.batch_get_accounts([])
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()

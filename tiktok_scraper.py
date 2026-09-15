"""
TikTok Account Information Extractor
Retrieves account creation date and device information from TikTok profiles
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional
import re

class TikTokAccountInfo:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.api_endpoints = {
            'user_info': 'https://www.tiktok.com/api/user/detail/',
            'user_feed': 'https://www.tiktok.com/api/post/item_list'
        }

    def get_account_info(self, username: str) -> Optional[Dict]:
        """
        Fetch TikTok account information including creation date and device info
        
        Args:
            username (str): TikTok username (without @)
            
        Returns:
            Dict: Account information or None if not found
        """
        try:
            # Normalize username
            username = username.lstrip('@')
            
            # Attempt to fetch user profile
            url = f"https://www.tiktok.com/api/user/detail/?uniqueId={username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_user_data(data, username)
            else:
                print(f"Error: Unable to fetch data for @{username} (Status: {response.status_code})")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error fetching account info: {str(e)}")
            return None

    def _parse_user_data(self, data: Dict, username: str) -> Dict:
        """
        Parse user data from TikTok API response
        
        Args:
            data (Dict): Raw API response
            username (str): Username for reference
            
        Returns:
            Dict: Parsed account information
        """
        try:
            user_details = data.get('userDetail', {})
            user = user_details.get('user', {})
            
            # Extract account creation timestamp
            create_time = user.get('createTime', 0)
            creation_date = datetime.fromtimestamp(create_time) if create_time else "Unknown"
            
            # Extract device information from signature or user agent traces
            device_info = self._extract_device_info(user_details)
            
            account_info = {
                'username': username,
                'user_id': user.get('id', 'Unknown'),
                'display_name': user.get('nickname', 'Unknown'),
                'signature': user.get('signature', ''),
                'creation_date': str(creation_date),
                'creation_timestamp': create_time,
                'verified': user.get('verified', False),
                'private_account': user.get('privateAccount', False),
                'follower_count': user.get('followerCount', 0),
                'following_count': user.get('followingCount', 0),
                'video_count': user.get('videoCount', 0),
                'device_info': device_info,
                'avatar_url': user.get('avatarLarger', ''),
                'bio': user.get('signature', '')
            }
            
            return account_info
            
        except Exception as e:
            print(f"Error parsing user data: {str(e)}")
            return None

    def _extract_device_info(self, user_details: Dict) -> Dict:
        """
        Extract device information from user details
        
        Args:
            user_details (Dict): User details from API
            
        Returns:
            Dict: Device information
        """
        try:
            stats = user_details.get('stats', {})
            user = user_details.get('user', {})
            
            # Extract from available fields
            device_info = {
                'device_model': 'Unknown',
                'os_type': 'Unknown',
                'app_version': 'Unknown',
                'browser_info': user.get('userAgent', 'Unknown') if user.get('userAgent') else 'Unknown'
            }
            
            # Parse user agent if available
            user_agent = user.get('userAgent', '')
            if user_agent:
                device_info['browser_info'] = user_agent
                if 'iPhone' in user_agent:
                    device_info['device_model'] = 'iPhone'
                    device_info['os_type'] = 'iOS'
                elif 'Android' in user_agent:
                    device_info['device_model'] = 'Android Device'
                    device_info['os_type'] = 'Android'
                elif 'Windows' in user_agent:
                    device_info['os_type'] = 'Windows'
                elif 'Mac' in user_agent:
                    device_info['os_type'] = 'macOS'
            
            return device_info
            
        except Exception as e:
            print(f"Error extracting device info: {str(e)}")
            return {'device_model': 'Unknown', 'os_type': 'Unknown'}

    def get_first_video_info(self, username: str) -> Optional[Dict]:
        """
        Get information about the user's first video (oldest upload)
        
        Args:
            username (str): TikTok username
            
        Returns:
            Dict: First video information
        """
        try:
            username = username.lstrip('@')
            # This would require additional API calls to fetch video history
            # Implementation depends on TikTok API availability
            print("First video extraction requires additional API access")
            return None
            
        except Exception as e:
            print(f"Error fetching first video: {str(e)}")
            return None


def main():
    """
    Example usage of TikTok Account Info tool
    """
    tool = TikTokAccountInfo()
    
    # Example: Fetch account information
    username = input("Enter TikTok username (without @): ").strip()
    
    if username:
        print(f"\nFetching information for @{username}...")
        account_info = tool.get_account_info(username)
        
        if account_info:
            print("\n" + "="*50)
            print("TIKTOK ACCOUNT INFORMATION")
            print("="*50)
            print(json.dumps(account_info, indent=2))
            print("="*50)
        else:
            print("Unable to retrieve account information.")
    else:
        print("No username provided.")


if __name__ == "__main__":
    main()
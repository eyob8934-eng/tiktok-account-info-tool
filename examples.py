"""
Usage examples for TikTok Account Info Tool
"""

from tiktok_scraper import TikTokAccountInfo
import json

def example_single_account():
    """
    Example 1: Fetch information for a single account
    """
    print("Example 1: Single Account Lookup")
    print("-" * 50)
    
    tool = TikTokAccountInfo()
    account_info = tool.get_account_info("tiktok")
    
    if account_info:
        print(f"Username: {account_info['username']}")
        print(f"Created: {account_info['creation_date']}")
        print(f"Device: {account_info['device_info']['device_model']}")
        print(f"Followers: {account_info['follower_count']:,}")
        print(f"Videos: {account_info['video_count']}")
    print()


def example_batch_accounts():
    """
    Example 2: Fetch information for multiple accounts
    """
    print("Example 2: Batch Account Lookup")
    print("-" * 50)
    
    usernames = ["tiktok", "cristiano", "khaby.lame"]
    tool = TikTokAccountInfo()
    results = []
    
    for username in usernames:
        print(f"Fetching @{username}...")
        account_info = tool.get_account_info(username)
        if account_info:
            results.append({
                'username': account_info['username'],
                'creation_date': account_info['creation_date'],
                'followers': account_info['follower_count'],
                'device': account_info['device_info']['device_model']
            })
    
    print("\nResults:")
    print(json.dumps(results, indent=2))
    print()


def example_export_to_json():
    """
    Example 3: Export account information to JSON file
    """
    print("Example 3: Export to JSON")
    print("-" * 50)
    
    tool = TikTokAccountInfo()
    account_info = tool.get_account_info("tiktok")
    
    if account_info:
        with open('account_info.json', 'w') as f:
            json.dump(account_info, f, indent=2)
        print("Account information exported to account_info.json")
    print()


def example_compare_accounts():
    """
    Example 4: Compare account creation dates and metrics
    """
    print("Example 4: Account Comparison")
    print("-" * 50)
    
    usernames = ["tiktok", "instagram"]
    tool = TikTokAccountInfo()
    accounts = []
    
    for username in usernames:
        account_info = tool.get_account_info(username)
        if account_info:
            accounts.append(account_info)
    
    if len(accounts) == 2:
        print("\nComparison Results:")
        print(f"Older Account: {accounts[0]['username']} ({accounts[0]['creation_date']})")
        print(f"Newer Account: {accounts[1]['username']} ({accounts[1]['creation_date']})")
        
        follower_diff = accounts[0]['follower_count'] - accounts[1]['follower_count']
        print(f"Follower Difference: {abs(follower_diff):,}")
    print()


def example_device_analysis():
    """
    Example 5: Analyze device information across accounts
    """
    print("Example 5: Device Analysis")
    print("-" * 50)
    
    usernames = ["tiktok", "cristiano", "khaby.lame", "addisonfirewasabi"]
    tool = TikTokAccountInfo()
    device_stats = {}
    
    for username in usernames:
        account_info = tool.get_account_info(username)
        if account_info:
            device = account_info['device_info']['device_model']
            device_stats[username] = device
    
    print("\nDevice Distribution:")
    for username, device in device_stats.items():
        print(f"  @{username}: {device}")
    print()


def example_account_verification():
    """
    Example 6: Check account verification status and creation date
    """
    print("Example 6: Account Verification & Age")
    print("-" * 50)
    
    usernames = ["tiktok", "cristiano"]
    tool = TikTokAccountInfo()
    
    for username in usernames:
        account_info = tool.get_account_info(username)
        if account_info:
            print(f"\n@{username}")
            print(f"  Verified: {account_info['verified']}")
            print(f"  Created: {account_info['creation_date']}")
            print(f"  Private: {account_info['private_account']}")
            print(f"  Public Info: Videos={account_info['video_count']}, "
                  f"Followers={account_info['follower_count']:,}, "
                  f"Following={account_info['following_count']:,}")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("TikTok Account Info Tool - Usage Examples")
    print("=" * 50)
    print()
    
    # Run examples
    try:
        example_single_account()
        example_batch_accounts()
        example_export_to_json()
        example_compare_accounts()
        example_device_analysis()
        example_account_verification()
    except Exception as e:
        print(f"Error running examples: {str(e)}")
        print("Please ensure you have internet connection and valid API access.")
    
    print("=" * 50)
    print("Examples completed!")
    print("=" * 50)
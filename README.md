# TikTok Account Information Tool

A Python tool to retrieve TikTok account creation dates and device model information.

## Features

- ✅ Extract account creation date and timestamp
- ✅ Retrieve device model and OS information
- ✅ Get account statistics (followers, following, video count)
- ✅ Extract account verification status
- ✅ Retrieve user profile information
- ✅ Parse device information from user agent data

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/eyob8934-eng/tiktok-account-info-tool.git
cd tiktok-account-info-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Run the script and enter a TikTok username:

```bash
python tiktok_scraper.py
```

Example output:
```
Enter TikTok username (without @): username
==================================================
TIKTOK ACCOUNT INFORMATION
==================================================
{
  "username": "username",
  "user_id": "123456789",
  "display_name": "Display Name",
  "creation_date": "2020-05-15 10:30:45",
  "creation_timestamp": 1589536245,
  "verified": true,
  "private_account": false,
  "follower_count": 1000000,
  "following_count": 500,
  "video_count": 250,
  "device_info": {
    "device_model": "iPhone",
    "os_type": "iOS",
    "app_version": "Unknown",
    "browser_info": "Mozilla/5.0..."
  }
}
==================================================
```

### Python Script Integration

```python
from tiktok_scraper import TikTokAccountInfo

# Initialize the tool
tool = TikTokAccountInfo()

# Get account information
account_info = tool.get_account_info("username")

if account_info:
    print(f"Account created: {account_info['creation_date']}")
    print(f"Device: {account_info['device_info']['device_model']}")
    print(f"Followers: {account_info['follower_count']}")
```

## API Response Fields

| Field | Description |
|-------|-------------|
| `username` | TikTok username |
| `user_id` | Unique user ID |
| `display_name` | Account display name |
| `creation_date` | Account creation date (formatted) |
| `creation_timestamp` | Unix timestamp of account creation |
| `verified` | Whether account is verified |
| `private_account` | Whether account is private |
| `follower_count` | Number of followers |
| `following_count` | Number of accounts followed |
| `video_count` | Total videos uploaded |
| `device_info` | Device and OS information |
| `avatar_url` | Profile picture URL |
| `bio` | Account bio/signature |

## Device Information

The tool attempts to extract device information from:
- User agent strings
- TikTok API responses
- Account metadata

Common device models detected:
- iPhone (iOS)
- Android
- Web browsers (Windows/macOS)

## Limitations

⚠️ **Important Notes:**

1. **API Availability**: TikTok's official API has strict limitations. This tool uses publicly available endpoints.
2. **Rate Limiting**: TikTok may rate limit requests. Use responsibly.
3. **Device Detection**: Device model detection relies on available metadata and may not always be accurate.
4. **Account Privacy**: Private accounts may have limited public information available.
5. **Terms of Service**: Ensure compliance with TikTok's Terms of Service when using this tool.

## Troubleshooting

### "Unable to fetch data" error
- Verify the username is correct (without @ symbol)
- Check your internet connection
- Try again after a few minutes (may be rate limited)

### Device information showing "Unknown"
- The account may not have this information publicly available
- Device detection relies on user agent data from old videos

## Legal Disclaimer

This tool is for educational and research purposes only. Users are responsible for ensuring their use complies with:
- TikTok's Terms of Service
- Applicable laws and regulations
- Respect for user privacy

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions, please create an issue on the GitHub repository.

---

**Last Updated:** 2026-09-15

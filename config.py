"""
Configuration settings for TikTok Account Info Tool
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
TIKTOK_API_BASE_URL = "https://www.tiktok.com/api"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Headers Configuration
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
}

# Output Configuration
OUTPUT_FORMAT = 'json'  # 'json', 'csv', 'txt'
EXPORT_DIR = './exports'
LOG_DIR = './logs'

# Rate Limiting
REQUESTS_PER_SECOND = 1
REQUESTS_PER_HOUR = 100

# Debug Mode
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Cache Configuration
ENABLE_CACHE = True
CACHE_DURATION = 3600  # seconds (1 hour)
CACHE_DIR = './cache'

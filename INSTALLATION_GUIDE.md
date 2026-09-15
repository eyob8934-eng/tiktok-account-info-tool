# TikTok Account Analysis Toolkit - Expert Installation Guide

## 🎯 Complete Setup Instructions

### **Prerequisites**
- Python 3.8 or higher
- Pip (Python Package Manager)
- Git (for cloning repository)
- 500MB free disk space
- For Termux users: Termux app installed on Android

---

## 📱 **Installation on Different Platforms**

### **A) Windows 10/11 Installation**

#### Step 1: Install Python
```bash
# Download from https://www.python.org/downloads/
# Run installer and CHECK "Add Python to PATH"

# Verify installation
python --version
pip --version
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/eyob8934-eng/tiktok-account-info-tool.git
cd tiktok-account-info-tool
```

#### Step 3: Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt

# Install additional required packages
pip install selenium webdriver-manager beautifulsoup4 requests lxml
```

#### Step 5: Install Chrome/Chromium
```bash
# Option A: Download Chrome
# Visit: https://www.google.com/chrome/

# Option B: Install via Chocolatey (Windows Package Manager)
choco install chromium

# Option C: Download Chromium directly
# Visit: https://www.chromium.org/getting-involved/download-chromium
```

#### Step 6: Verify Installation
```bash
python -c "from selenium import webdriver; print('Selenium OK')"
python -c "import beautifulsoup4; print('BeautifulSoup OK')"
```

---

### **B) Linux (Ubuntu/Debian) Installation**

#### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install Python & Dependencies
```bash
sudo apt install python3 python3-pip python3-venv git -y

# Verify
python3 --version
pip3 --version
```

#### Step 3: Clone Repository
```bash
git clone https://github.com/eyob8934-eng/tiktok-account-info-tool.git
cd tiktok-account-info-tool
```

#### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
pip install selenium webdriver-manager beautifulsoup4 requests lxml
```

#### Step 6: Install Chromium
```bash
sudo apt install chromium-browser -y
# OR
sudo apt install google-chrome-stable -y
```

#### Step 7: Run Tool
```bash
python3 termux_browser_scraper.py
```

---

### **C) macOS Installation**

#### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python
```bash
brew install python@3.11

# Verify
python3 --version
pip3 --version
```

#### Step 3: Clone Repository
```bash
git clone https://github.com/eyob8934-eng/tiktok-account-info-tool.git
cd tiktok-account-info-tool
```

#### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
pip install selenium webdriver-manager beautifulsoup4 requests lxml
```

#### Step 6: Install Chrome
```bash
brew install --cask google-chrome
# OR
brew install --cask chromium
```

#### Step 7: Run Tool
```bash
python3 termux_browser_scraper.py
```

---

### **D) Termux (Android) Installation - EXPERT SETUP**

#### Step 1: Install Termux
- Download from: https://f-droid.org/en/packages/com.termux/
- Install & Open Termux

#### Step 2: Update Termux
```bash
apt update
apt upgrade -y
```

#### Step 3: Install Python & Dependencies
```bash
apt install python python-pip git -y
apt install chromium -y  # Critical for Termux
```

#### Step 4: Clone Repository
```bash
git clone https://github.com/eyob8934-eng/tiktok-account-info-tool.git
cd tiktok-account-info-tool
```

#### Step 5: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

#### Step 6: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install selenium webdriver-manager beautifulsoup4 requests lxml
```

#### Step 7: Configure Chromium for Termux
```bash
# Create script to find Chromium
echo '#!/bin/bash' > /data/data/com.termux/files/usr/bin/chromium-wrapper.sh
echo 'exec /data/data/com.termux/files/usr/bin/chromium "$@"' >> chromium-wrapper.sh
chmod +x chromium-wrapper.sh
```

#### Step 8: Run Tool
```bash
python termux_browser_scraper.py
```

---

## 🔧 **Troubleshooting Installation Issues**

### **Issue 1: "Chrome/Chromium not found"**
```bash
# Solution 1: Install webdriver-manager
pip install webdriver-manager

# Solution 2: Manually specify Chrome path in script
# Edit termux_browser_scraper.py, line with binary_location:
# Windows:
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Linux:
options.binary_location = "/usr/bin/google-chrome"

# Mac:
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### **Issue 2: "Selenium module not found"**
```bash
# Reinstall dependencies
pip uninstall selenium -y
pip install selenium --upgrade
```

### **Issue 3: "Permission denied" on Linux**
```bash
# Add execute permissions
chmod +x tiktok-account-info-tool
chmod +x *.py

# Run with python directly
python3 script_name.py
```

### **Issue 4: Termux - "Chromium binary path not found"**
```bash
# Check Chromium installation
which chromium
ls -la /data/data/com.termux/files/usr/bin/ | grep chromium

# Reinstall if needed
apt remove chromium -y
apt install chromium -y
```

### **Issue 5: "Port already in use"**
```bash
# Find and kill process using port
lsof -i :9222  # For headless debugging
kill -9 <PID>
```

---

## 📋 **Complete Requirements File Contents**

```txt
requests>=2.28.0
python-dateutil>=2.8.2
beautifulsoup4>=4.11.0
selenium>=4.10.0
webdriver-manager>=3.9.1
lxml>=4.9.3
certifi>=2023.7.22
charset-normalizer>=3.3.2
idna>=3.4
urllib3>=2.0.7
```

---

## 🚀 **Quick Start After Installation**

### **Run Basic Script**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run single account fetch
python termux_browser_scraper.py

# Follow prompts to enter TikTok username
```

### **Run Forensic Analysis**
```bash
python forensic_analysis_engine.py
```

### **Run Comparative Analysis**
```bash
python comparative_analysis_tool.py
```

---

## ✅ **Verification Checklist**

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All requirements installed (pip list)
- [ ] Selenium can import successfully
- [ ] Chrome/Chromium installed
- [ ] WebDriver can initialize
- [ ] Script runs without errors

---

## 📞 **Support & Debugging**

### **Enable Debug Mode**
```python
# Add to script
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Check Selenium Version**
```bash
pip show selenium
```

### **Test WebDriver**
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://www.tiktok.com")
print(driver.title)
driver.quit()
```

---

## 🎉 **Installation Complete!**

You're now ready to use the TikTok Account Analysis Toolkit. Start with:
```bash
python termux_browser_scraper.py
```

**Need help?** Check the repository issues or documentation.

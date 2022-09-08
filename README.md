# TASK

## Installation
1. Run
### Linux
```
sudo apt-get install python3-venv
python3 -m venv .venv
source .venv/bin/activate
```

### macOS
```
python3 -m venv .venv
source .venv/bin/activate
```

### Windows
```
py -3 -m venv .venv
.venv\scripts\activate
```

2. Configure your environment variables: cp .env.example .env
3. Run `pip install selenium`
4. Run `pip install python-dotenv[cli]`
5. Use the Google Chrome and install the current release 'https://chromedriver.chromium.org/downloads'
6. If you use in MacOs you need to open terminal and:
```
cd <path-of-chromedriver>
xattr -d com.apple.quarantine chromedriver
```
7. Run the project `dotenv run -- python index.py`

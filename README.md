# NewsPilot AI

An AI-powered automated media publishing system that scrapes trending news, generates high-quality articles with OpenAI, creates cinematic AI cover images, and automatically publishes content to WeChat Official Accounts.

---

## Features

- Scrape trending news automatically
- Generate AI-written articles
- Create AI-generated cover images
- Auto upload to WeChat Official Account
- Save Markdown backups locally
- Daily scheduled automation
- Original source attribution
- Disclaimer generation
- Multi-source news aggregation

---

## Supported Sources

- 36Kr
- Yicai
- Caixin

You can easily add more sources.

---

## Tech Stack

- Python
- OpenAI API
- BeautifulSoup4
- Requests
- Schedule
- WeChat Official Account API

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourname/newspilot-ai.git

cd newspilot-ai

Install dependencies:
pip install -r requirements.txt

Configuration

Open:
</>BASH
auto_wechat_system.py

Configure:
</>python
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

WECHAT_APP_ID = "YOUR_WECHAT_APP_ID"

WECHAT_APP_SECRET = "YOUR_WECHAT_APP_SECRET"

Run
</>BASH
python auto_wechat_system.py

Workflow
Scrape trending news
Extract article content
Generate AI article
Generate cinematic AI image prompt
Generate AI cover image
Upload cover image to WeChat
Publish article draft automatically
Save local Markdown backup

Example Use Cases
AI media automation
WeChat article automation
News aggregation
AI content farms
AI newsletter systems
AI publishing pipelines

WeChat Official Account Requirements

You need:

WeChat Official Account
AppID
AppSecret
IP whitelist configured

Official platform:

https://mp.weixin.qq.com/


OpenAI API

Get your API key:

https://platform.openai.com/


Disclaimer

This project is for educational and research purposes only.

Users are responsible for complying with:

OpenAI policies
WeChat platform rules
Copyright laws
News licensing regulations

Do not use this project for illegal scraping or copyright infringement.


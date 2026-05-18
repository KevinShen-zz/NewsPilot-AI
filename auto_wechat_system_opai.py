# -*- coding: utf-8 -*-

"""
Auto WeChat AI News System (OpenAI Version)

Features:
1. Automatically scrape trending news
2. Extract article content
3. Generate WeChat articles using OpenAI
4. Generate AI cover image prompts
5. Generate unique AI cover images
6. Upload drafts to WeChat Official Account
7. Add source links automatically
8. Save Markdown files
9. Daily scheduled automation

Author: YourName
License: MIT
"""

import json
import time
import requests
import schedule

from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from openai import OpenAI


# =========================================================
# CONFIG
# =========================================================

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

WECHAT_APP_ID = "YOUR_WECHAT_APP_ID"

WECHAT_APP_SECRET = "YOUR_WECHAT_APP_SECRET"

OPENAI_IMAGE_MODEL = "gpt-image-1"

OPENAI_CHAT_MODEL = "gpt-4.1-mini"


# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# =========================================================
# AUTO WECHAT SYSTEM
# =========================================================

class AutoWechatSystem:

    def __init__(self):

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124 Safari/537.36"
            )
        }

    # =====================================================
    # SCRAPE NEWS
    # =====================================================

    def scrape_articles(
        self,
        url: str
    ) -> List[Dict]:

        articles = []

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=15
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            links = soup.find_all("a")

            for link in links[:150]:

                title = link.get_text(strip=True)

                href = link.get("href")

                if title and len(title) > 12 and href:

                    if href.startswith("/"):

                        base_url = (
                            url.split("//")[0]
                            + "//"
                            + url.split("/")[2]
                        )

                        href = base_url + href

                    articles.append({

                        "title": title,

                        "url": href,

                        "source": url
                    })

            return articles[:10]

        except Exception as e:

            print(f"Scrape failed: {e}")

            return []

    # =====================================================
    # FETCH HOT ARTICLES
    # =====================================================

    def fetch_hot_articles(
        self,
        count: int = 5
    ) -> List[Dict]:

        all_articles = []

        sources = [

            "https://36kr.com/newsflashes/catalog/1",

            "https://www.yicai.com",

            "https://www.caixin.com"
        ]

        for source in sources:

            print(f"Scraping: {source}")

            all_articles.extend(
                self.scrape_articles(source)
            )

        unique_articles = []

        seen_titles = set()

        for article in all_articles:

            if article["title"] not in seen_titles:

                unique_articles.append(article)

                seen_titles.add(article["title"])

        return unique_articles[:count]

    # =====================================================
    # FETCH ARTICLE CONTENT
    # =====================================================

    def fetch_article_content(
        self,
        url: str
    ) -> str:

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=15
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            paragraphs = soup.find_all("p")

            content = []

            for p in paragraphs:

                text = p.get_text(strip=True)

                if len(text) > 20:

                    content.append(text)

            return "\n".join(content)[:5000]

        except Exception as e:

            print(f"Content fetch failed: {e}")

            return ""

    # =====================================================
    # GENERATE ARTICLE
    # =====================================================

    def generate_wechat_article(
        self,
        title,
        content,
        source,
        source_url
    ):

        prompt = f"""
Write a high-quality WeChat-style article
based on the following news.

Requirements:

1. Engaging introduction
2. Clear subheadings
3. Analytical insights
4. Storytelling style
5. Professional tone
6. Around 1200-1500 words
7. Suitable for social media publishing
8. Add a discussion question at the end

News Title:
{title}

Source:
{source}

Original URL:
{source_url}

News Content:
{content}
"""

        try:

            response = client.chat.completions.create(

                model=OPENAI_CHAT_MODEL,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are a professional "
                            "news editor and writer."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.8
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"OpenAI generation failed: {e}")

            return "Generation failed."

    # =====================================================
    # GENERATE IMAGE PROMPT
    # =====================================================

    def generate_cover_prompt(
        self,
        title
    ):

        prompt = f"""
Create a cinematic AI image prompt
for a news cover image.

Requirements:

- futuristic
- cinematic lighting
- ultra realistic
- dramatic atmosphere
- technology news style
- highly detailed
- 16:9 composition
- no text
- no watermark

News title:
{title}
"""

        try:

            response = client.chat.completions.create(

                model=OPENAI_CHAT_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"Prompt generation failed: {e}")

            return (
                "cinematic futuristic technology "
                "news cover, ultra realistic"
            )

    # =====================================================
    # GENERATE COVER IMAGE
    # =====================================================

    def generate_cover_image(
        self,
        image_prompt
    ):

        filename = (
            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + "_cover.png"
        )

        try:

            result = client.images.generate(

                model=OPENAI_IMAGE_MODEL,

                prompt=image_prompt,

                size="1536x1024"
            )

            image_url = result.data[0].url

            print("Downloading AI cover image...")

            image_response = requests.get(
                image_url,
                stream=True,
                timeout=120
            )

            with open(filename, "wb") as f:

                for chunk in image_response.iter_content(1024):

                    if chunk:
                        f.write(chunk)

            print(f"Cover image saved: {filename}")

            return filename

        except Exception as e:

            print(f"Image generation failed: {e}")

            return None

    # =====================================================
    # SAVE MARKDOWN
    # =====================================================

    def save_markdown(
        self,
        title,
        content
    ):

        safe_title = (
            title
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
        )

        filename = (

            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            + "_"

            + safe_title[:50]

            + ".md"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        print(f"Markdown saved: {filename}")

    # =====================================================
    # GET WECHAT ACCESS TOKEN
    # =====================================================

    def get_access_token(self):

        url = (
            "https://api.weixin.qq.com/cgi-bin/token"
            f"?grant_type=client_credential"
            f"&appid={WECHAT_APP_ID}"
            f"&secret={WECHAT_APP_SECRET}"
        )

        try:

            response = requests.get(url)

            data = response.json()

            return data.get("access_token")

        except Exception as e:

            print(f"Token fetch failed: {e}")

            return None

    # =====================================================
    # UPLOAD COVER IMAGE
    # =====================================================

    def upload_cover_image_to_wechat(
        self,
        access_token,
        image_path
    ):

        url = (
            "https://api.weixin.qq.com/"
            "cgi-bin/material/add_material"
            f"?access_token={access_token}"
            "&type=image"
        )

        try:

            with open(image_path, "rb") as f:

                files = {
                    "media": f
                }

                response = requests.post(
                    url,
                    files=files
                )

            result = response.json()

            print(result)

            return result.get("media_id")

        except Exception as e:

            print(f"Upload failed: {e}")

            return None

    # =====================================================
    # PUBLISH WECHAT DRAFT
    # =====================================================

    def publish_wechat_draft(
        self,
        title,
        content,
        source_url,
        cover_path
    ):

        access_token = self.get_access_token()

        if not access_token:

            print("Access token failed")

            return

        thumb_media_id = (
            self.upload_cover_image_to_wechat(
                access_token,
                cover_path
            )
        )

        if not thumb_media_id:

            print("Cover upload failed")

            return

        url = (
            "https://api.weixin.qq.com/"
            "cgi-bin/draft/add"
            f"?access_token={access_token}"
        )

        payload = {

            "articles": [

                {

                    "title": title,

                    "author": "AI News Assistant",

                    "digest": title[:120],

                    "content": content,

                    "content_source_url": source_url,

                    "thumb_media_id": thumb_media_id,

                    "show_cover_pic": 1
                }
            ]
        }

        try:

            response = requests.post(

                url,

                data=json.dumps(
                    payload,
                    ensure_ascii=False
                ).encode("utf-8")
            )

            result = response.json()

            print("Draft publish result:")
            print(result)

        except Exception as e:

            print(f"WeChat publish failed: {e}")

    # =====================================================
    # MAIN WORKFLOW
    # =====================================================

    def run(self):

        print("\n======================")
        print("Starting AI News Workflow")
        print("======================\n")

        articles = self.fetch_hot_articles(5)

        for article in articles:

            try:

                print(
                    f"Processing: "
                    f"{article['title']}"
                )

                content = self.fetch_article_content(
                    article["url"]
                )

                if not content:

                    print("Empty content skipped")

                    continue

                wechat_article = (
                    self.generate_wechat_article(
                        article["title"],
                        content,
                        article["source"],
                        article["url"]
                    )
                )

                cover_prompt = (
                    self.generate_cover_prompt(
                        article["title"]
                    )
                )

                print("Cover Prompt:")
                print(cover_prompt)

                cover_path = (
                    self.generate_cover_image(
                        cover_prompt
                    )
                )

                wechat_article += f"""

<hr>

<h3>Source</h3>

<p>{article['source']}</p>

<h3>Original Article</h3>

<p>
<a href="{article['url']}">
Read Original
</a>
</p>

<h3>Disclaimer</h3>

<p>
This article was partially generated
with AI assistance for informational
purposes only.
</p>

<p>
All copyrights belong to the original
authors and media sources.
</p>
"""

                self.save_markdown(
                    article["title"],
                    wechat_article
                )

                if cover_path:

                    self.publish_wechat_draft(
                        article["title"],
                        wechat_article,
                        article["url"],
                        cover_path
                    )

                print("Done.\n")

                time.sleep(5)

            except Exception as e:

                print(f"Processing failed: {e}")

                continue


# =========================================================
# SCHEDULE
# =========================================================

system = AutoWechatSystem()


def job():

    system.run()


schedule.every().day.at("08:00").do(job)

print("AI WeChat News System Started")
print("Scheduled daily at 08:00")

# Run immediately once
job()

while True:

    schedule.run_pending()

    time.sleep(30)
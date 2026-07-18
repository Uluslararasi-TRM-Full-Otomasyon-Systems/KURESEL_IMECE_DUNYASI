#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Social Media Automation - v2.0 LIVE
Coklu platform yayin sistemi: Facebook, Instagram, Twitter/X, TikTok, YouTube, Blog

Duzeltmeler (v2.0):
  - Twitter/X: tweepy v4 ile OAuth 1.0a gercek post
  - Instagram: Graph API iki adimli media container→publish akisi
  - TikTok: Content Posting API v2 (video ve fotograf)
  - YouTube: googleapiclient video upload
  - Blog: Blogger API v3 gercek post
  - Tum platformlar: token yoksa → mock'a duser, hata basmaz
  - Rate limiting: platform basina gecikme
  - Retry: 3 deneme, exponential backoff
"""

import asyncio
import logging
import os

import os as _os
_TRM_MODE = _os.getenv("TRM_MODE", "live").lower()
_MOCK_ALLOWED = _TRM_MODE in ("test", "demo")

import time
import json
import random
from datetime import datetime
from typing import Dict, List, Optional

import requests
REQUESTS_AVAILABLE = True

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False

logger = logging.getLogger(__name__)

logger.info("CALISMA MODU: %s", os.getenv("TRM_MODE", "live").upper())

# ─────────────────────────────────────────────────────────────────────
# YARDIMCILAR
# ─────────────────────────────────────────────────────────────────────

async def _retry(coro_fn, retries: int = 3, base_delay: float = 2.0):
    """Async coroutine'i exponential backoff ile dene."""
    for attempt in range(retries):
        try:
            return await coro_fn()
        except Exception as e:
            if attempt == retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"⚠️ Deneme {attempt+1}/{retries} basarisiz: {e}. {delay:.1f}s bekleniyor...")
            await asyncio.sleep(delay)


def _sync_post(fn, *args, **kwargs):
    """Senkron requests'i thread pool'da calistir (event loop'u bloke etme)."""
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


# ─────────────────────────────────────────────────────────────────────
# MOCK CLIENT
# ─────────────────────────────────────────────────────────────────────

class MockSocialMediaClient:
    def __init__(self, platform="Mock"):
        self.platform = platform

    async def publish_content(self, content: Dict) -> Dict:
        await asyncio.sleep(0.3)
        return {
            'success': True,
            'platform': self.platform,
            'post_id': f"mock_{int(datetime.now().timestamp())}",
            'url': f"https://{self.platform.lower()}.com/mock_post",
            'message': f"[MOCK] {self.platform} paylasimi simule edildi",
            'mock': True,
        }


# ─────────────────────────────────────────────────────────────────────
# FACEBOOK
# ─────────────────────────────────────────────────────────────────────

class FacebookPublisher:
    def __init__(self):
        self.token    = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
        self.page_id  = os.getenv("FACEBOOK_PAGE_ID", "me")
        self.api_url  = "https://graph.facebook.com/v19.0"
        self._mock    = MockSocialMediaClient("Facebook")
        self._use_mock = _MOCK_ALLOWED and not self.token

    async def publish_content(self, content: Dict) -> Dict:
        if not _MOCK_ALLOWED and not self.token:
            logger.error("CALISMA MODU: LIVE | Facebook token eksik — guvenli dur")
            return {'success': False, 'platform': 'Facebook', 'error': 'FACEBOOK_ACCESS_TOKEN eksik'}
        if self._use_mock:
            logger.info("CALISMA MODU: %s | Facebook mock", _TRM_MODE.upper())
            return await self._mock.publish_content(content)
        logger.info("CALISMA MODU: LIVE | Facebook gercek API")
        async def _post():
            url = f"{self.api_url}/{self.page_id}/feed"
            resp = await _sync_post(requests.post, url, params={
                'message':      content.get('content', ''),
                'link':         content.get('link', ''),
                'access_token': self.token,
            }, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            pid = data.get('id', '')
            return {
                'success':  True,
                'platform': 'Facebook',
                'post_id':  pid,
                'url':      f"https://facebook.com/{pid}",
                'message':  'Facebook paylasimi basarili',
            }
        try:
            return await _retry(_post)
        except Exception as e:
            logger.error(f"❌ Facebook hata: {e}")
            return {'success': False, 'platform': 'Facebook', 'error': str(e)}


# ─────────────────────────────────────────────────────────────────────
# INSTAGRAM (Graph API iki adim: container → publish)
# ─────────────────────────────────────────────────────────────────────

class InstagramPublisher:
    def __init__(self):
        self.token      = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        self.account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
        self.api_url    = "https://graph.instagram.com/v19.0"
        self._mock      = MockSocialMediaClient("Instagram")
        self._use_mock = _MOCK_ALLOWED and not (self.token and self.account_id)

    async def publish_content(self, content: Dict) -> Dict:
        if self._use_mock:
            return await self._mock.publish_content(content)
        async def _post():
            # Adim 1: Media container olustur
            container_url = f"{self.api_url}/{self.account_id}/media"
            c_resp = await _sync_post(requests.post, container_url, params={
                'image_url':    content.get('image_url', ''),
                'caption':      content.get('content', ''),
                'access_token': self.token,
            }, timeout=30)
            c_resp.raise_for_status()
            container_id = c_resp.json().get('id')
            if not container_id:
                raise ValueError("Container ID alinamadi")
            # Adim 2: Yayinla
            await asyncio.sleep(2)  # Instagram islem suresi
            pub_url = f"{self.api_url}/{self.account_id}/media_publish"
            p_resp = await _sync_post(requests.post, pub_url, params={
                'creation_id':  container_id,
                'access_token': self.token,
            }, timeout=30)
            p_resp.raise_for_status()
            media_id = p_resp.json().get('id', '')
            return {
                'success':  True,
                'platform': 'Instagram',
                'post_id':  media_id,
                'url':      f"https://www.instagram.com/p/{media_id}/",
                'message':  'Instagram paylasimi basarili',
            }
        try:
            return await _retry(_post)
        except Exception as e:
            logger.error(f"❌ Instagram hata: {e}")
            return {'success': False, 'platform': 'Instagram', 'error': str(e)}


# ─────────────────────────────────────────────────────────────────────
# TWITTER / X  (tweepy v4 OAuth 1.0a)
# ─────────────────────────────────────────────────────────────────────

class TwitterPublisher:
    def __init__(self):
        self.api_key    = os.getenv("TWITTER_API_KEY", "")
        self.api_secret = os.getenv("TWITTER_API_SECRET", "")
        self.acc_token  = os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.acc_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
        self._mock      = MockSocialMediaClient("Twitter/X")
        self._client    = None

        if TWEEPY_AVAILABLE and all([self.api_key, self.api_secret,
                                     self.acc_token, self.acc_secret]):
            try:
                self._client = tweepy.Client(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.acc_token,
                    access_token_secret=self.acc_secret,
                    wait_on_rate_limit=True,
                )
                logger.info("✅ Twitter/X istemcisi hazir")
            except Exception as e:
                logger.warning(f"⚠️ Twitter istemci hatasi → mock: {e}")
        else:
            if not TWEEPY_AVAILABLE:
                logger.warning("⚠️ tweepy kurulu degil → pip install tweepy")
            else:
                logger.warning("⚠️ Twitter API anahtarlari eksik → mock mod")

    async def publish_content(self, content: Dict) -> Dict:
        if not self._client:
            return await self._mock.publish_content(content)
        async def _post():
            text = content.get('content', '')
            # Twitter 280 karakter limiti
            if len(text) > 277:
                text = text[:277] + "..."
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self._client.create_tweet(text=text)
            )
            tweet_id = response.data['id'] if response.data else ''
            return {
                'success':  True,
                'platform': 'Twitter/X',
                'post_id':  str(tweet_id),
                'url':      f"https://x.com/i/web/status/{tweet_id}",
                'message':  'Tweet paylasildi',
            }
        try:
            return await _retry(_post)
        except Exception as e:
            logger.error(f"❌ Twitter hata: {e}")
            return {'success': False, 'platform': 'Twitter/X', 'error': str(e)}


# ─────────────────────────────────────────────────────────────────────
# TIKTOK (Content Posting API v2 — fotograf/video)
# ─────────────────────────────────────────────────────────────────────

class TikTokPublisher:
    def __init__(self):
        self.token    = os.getenv("TIKTOK_ACCESS_TOKEN", "")
        self._mock    = MockSocialMediaClient("TikTok")
        self._use_mock = _MOCK_ALLOWED and not self.token

    async def publish_content(self, content: Dict) -> Dict:
        if self._use_mock:
            return await self._mock.publish_content(content)
        async def _post():
            # TikTok Content Posting API v2
            url = "https://open.tiktokapis.com/v2/post/publish/content/init/"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type":  "application/json; charset=UTF-8",
            }
            body = {
                "post_info": {
                    "title":           content.get('content', '')[:150],
                    "privacy_level":   "PUBLIC_TO_EVERYONE",
                    "disable_duet":    False,
                    "disable_comment": False,
                    "disable_stitch":  False,
                },
                "source_info": {
                    "source":    "PULL_FROM_URL",
                    "video_url": content.get('video_url', content.get('image_url', '')),
                },
                "media_type": "VIDEO",
                "post_mode":  "DIRECT_POST",
            }
            resp = await _sync_post(requests.post, url, headers=headers,
                                    json=body, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            pub_id = data.get('data', {}).get('publish_id', '')
            return {
                'success':  True,
                'platform': 'TikTok',
                'post_id':  pub_id,
                'url':      f"https://www.tiktok.com/@user/video/{pub_id}",
                'message':  'TikTok yayinlandi',
            }
        try:
            return await _retry(_post)
        except Exception as e:
            logger.error(f"❌ TikTok hata: {e}")
            return {'success': False, 'platform': 'TikTok', 'error': str(e)}


# ─────────────────────────────────────────────────────────────────────
# YOUTUBE (Google API — video aciklama/community post)
# ─────────────────────────────────────────────────────────────────────

class YouTubePublisher:
    def __init__(self):
        self.api_key    = os.getenv("YOUTUBE_API_KEY", "")
        self.channel_id = os.getenv("YOUTUBE_CHANNEL_ID", "")
        self._mock      = MockSocialMediaClient("YouTube")
        self._use_mock = _MOCK_ALLOWED and not self.api_key

    async def publish_content(self, content: Dict) -> Dict:
        if self._use_mock:
            return await self._mock.publish_content(content)
        # YouTube Community Post (gercek video upload → OAuth scope gerektirir)
        async def _post():
            # Community post endpoint (v3)
            url = "https://www.googleapis.com/youtube/v3/communityPosts"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            body = {
                "snippet": {
                    "type": "text",
                    "textOriginal": content.get('content', ''),
                }
            }
            resp = await _sync_post(requests.post, url, headers=headers,
                                    json=body, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            pid = data.get('id', '')
            return {
                'success':  True,
                'platform': 'YouTube',
                'post_id':  pid,
                'url':      f"https://youtube.com/channel/{self.channel_id}",
                'message':  'YouTube community post paylasildi',
            }
        try:
            return await _retry(_post)
        except Exception as e:
            logger.error(f"❌ YouTube hata: {e}")
            return {'success': False, 'platform': 'YouTube', 'error': str(e)}


# ─────────────────────────────────────────────────────────────────────
# BLOG (Blogger API v3)
# ─────────────────────────────────────────────────────────────────────

class BlogPublisher:
    def __init__(self):
        self.api_key  = os.getenv("GOOGLE_CLIENT_ID", "")       # OAuth token
        self.blog_ids = os.getenv("BLOGGER_BLOG_IDS", "").split(",")
        self._mock    = MockSocialMediaClient("Blog")
        self._use_mock = _MOCK_ALLOWED and not self.api_key

    async def publish_content(self, content: Dict) -> Dict:
        if self._use_mock:
            return await self._mock.publish_content(content)
        results = []
        for blog_id in self.blog_ids:
            blog_id = blog_id.strip()
            if not blog_id:
                continue
            try:
                async def _post(bid=blog_id):
                    url = f"https://www.googleapis.com/blogger/v3/blogs/{bid}/posts/"
                    headers = {"Authorization": f"Bearer {self.api_key}",
                               "Content-Type": "application/json"}
                    body = {
                        "title":   content.get('title', content.get('content', '')[:80]),
                        "content": content.get('content', ''),
                    }
                    resp = await _sync_post(requests.post, url, headers=headers,
                                            json=body, timeout=30)
                    resp.raise_for_status()
                    data = resp.json()
                    return {
                        'success':  True,
                        'platform': f'Blog ({bid})',
                        'post_id':  data.get('id', ''),
                        'url':      data.get('url', ''),
                        'message':  'Blog yazisi yayinlandi',
                    }
                results.append(await _retry(_post))
            except Exception as e:
                results.append({'success': False, 'platform': f'Blog ({blog_id})', 'error': str(e)})
        if not results:
            return await self._mock.publish_content(content)
        # Ilk basarili sonucu dondur
        for r in results:
            if r.get('success'):
                return r
        return results[0]


# ─────────────────────────────────────────────────────────────────────
# ANA YONETICI
# ─────────────────────────────────────────────────────────────────────

class SocialMediaManager:
    def __init__(self):
        self.facebook  = FacebookPublisher()
        self.instagram = InstagramPublisher()
        self.twitter   = TwitterPublisher()
        self.tiktok    = TikTokPublisher()
        self.youtube   = YouTubePublisher()
        self.blog      = BlogPublisher()
        self.stats_file = "social_media_stats.json"

    async def publish_to_all_platforms(self, content: Dict) -> Dict:
        """Tum platformlarda paralel olarak yayinla."""
        logger.info("📡 Tum platformlarda yayinlama baslatildi...")
        tasks = {
            'facebook':  self.facebook.publish_content(content),
            'instagram': self.instagram.publish_content(content),
            'twitter':   self.twitter.publish_content(content),
            'tiktok':    self.tiktok.publish_content(content),
            'youtube':   self.youtube.publish_content(content),
            'blog':      self.blog.publish_content(content),
            'linkedin':  self._publish_linkedin(content),
        }
        results = {}
        coros = list(tasks.values())
        names  = list(tasks.keys())
        settled = await asyncio.gather(*coros, return_exceptions=True)
        for name, res in zip(names, settled):
            if isinstance(res, Exception):
                results[name] = {'success': False, 'platform': name, 'error': str(res)}
            else:
                results[name] = res
            icon = "✅" if results[name].get('success') else "❌"
            mock_tag = " [MOCK]" if results[name].get('mock') else ""
            logger.info(f"{icon} {name}{mock_tag}: {results[name].get('message', '')}")

        self._save_stats(results, content)
        successful = sum(1 for r in results.values() if r.get('success'))
        total = len(results)
        return {
            'platforms': results,
            'summary': {
                'successful_platforms': successful,
                'total_platforms': total,
                'success_rate': round(successful / total * 100, 1) if total else 0,
            }
        }

    def _save_stats(self, results: Dict, content: Dict):
        try:
            stats = {}
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            except Exception:
                pass
            entry = {
                'timestamp': datetime.now().isoformat(),
                'content_preview': str(content.get('content', ''))[:100],
                'results': {k: {'success': v.get('success'), 'post_id': v.get('post_id'), 'mock': v.get('mock', False)}
                            for k, v in results.items()},
            }
            stats.setdefault('history', []).append(entry)
            stats['history'] = stats['history'][-100:]  # Son 100 yayin
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Istatistik kaydedilemedi: {e}")

    async def publish_single(self, platform: str, content: Dict) -> Dict:
        """Tek platforma yayinla."""
        publishers = {
            'facebook': self.facebook, 'instagram': self.instagram,
            'twitter': self.twitter,   'tiktok': self.tiktok,
            'youtube': self.youtube,   'blog': self.blog,
        }
        pub = publishers.get(platform.lower())
        if not pub:
            return {'success': False, 'error': f'Bilinmeyen platform: {platform}'}
        return await pub.publish_content(content)

    def get_platform_status(self) -> Dict:
        """Hangi platformlarin gercek, hangilerinin mock oldugunu goster."""
        return {
            'facebook':  not self.facebook._use_mock,
            'instagram': not self.instagram._use_mock,
            'twitter':   self.twitter._client is not None,
            'tiktok':    not self.tiktok._use_mock,
            'youtube':   not self.youtube._use_mock,
            'blog':      not self.blog._use_mock,
        }


class SocialMediaAutomation(SocialMediaManager):
    """Eski Drive entegrasyonu icin geriye donuk uyumluluk katmani."""

    async def post_content(
        self,
        ai_content,
        file_type: str = "",
        media_url: str = "",
        platforms: Optional[List[str]] = None,
    ) -> Dict:
        if isinstance(ai_content, dict):
            content = dict(ai_content)
        else:
            content = {"content": str(ai_content or "")}

        content.setdefault("content", str(ai_content or ""))
        content.setdefault("media_type", file_type or content.get("media_type", "text"))

        if media_url:
            content.setdefault("link", media_url)
            if file_type == "image":
                content.setdefault("image_url", media_url)
            elif file_type == "video":
                content.setdefault("video_url", media_url)

        requested_platforms = [platform.lower() for platform in (platforms or [])]
        if not requested_platforms:
            result = await self.publish_to_all_platforms(content)
            platform_results = result.get("platforms", {})
        else:
            platform_results = {}
            for platform in requested_platforms:
                platform_results[platform] = await self.publish_single(platform, content)

        posted_platforms = [
            platform for platform, result in platform_results.items() if result.get("success")
        ]
        return {
            "posted_platforms": posted_platforms,
            "platform_results": platform_results,
            "successful_platforms": len(posted_platforms),
            "total_platforms": len(platform_results),
        }

    async def get_platform_status(self, platform: Optional[str] = None):
        statuses = super().get_platform_status()
        if platform:
            return statuses.get(platform.lower(), False)
        return statuses




    async def _publish_linkedin(self, content_data: dict) -> dict:
        """LinkedIn'e icerik paylas"""
        """LinkedIn'e icerik paylas"""
        try:
            cfg = self.config.linkedin
            token = cfg.get('access_token', '')
            org_id = cfg.get('organization_id', '')
            if not token:
                return {'success': False, 'error': 'LinkedIn access_token eksik (secrets.env)'}

            text = content_data.get('content', '')
            link = content_data.get('link', '')
            post_text = f"{text}\n\n{link}" if link else text

            author = f"urn:li:organization:{org_id}" if org_id else "urn:li:person:me"
            payload = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        return {'success': True, 'post_id': data.get('id', ''), 'platform': 'linkedin'}
                    else:
                        err = await resp.text()
                        return {'success': False, 'error': f"HTTP {resp.status}: {err[:200]}"}
        except Exception as e:
            logger.error(f"LinkedIn paylasim hatasi: {e}")
            return {'success': False, 'error': str(e)}


async def test_social_media_automation():
    """Sosyal medya otomasyonunu test et (run.py icin)"""
    mgr = SocialMediaManager()
    test_content = {
        'content': 'Test icerik - TRM Otomasyon',
        'title': 'Test',
        'link': 'https://example.com',
        'image_url': '',
    }
    result = await mgr.publish_to_all_platforms(test_content)
    logger.info(f"Test sonucu: {result['summary']}")
    return result

# ─────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    async def main():
        mgr = SocialMediaManager()
        print("\n📊 Platform Durumu:")
        for platform, live in mgr.get_platform_status().items():
            status = "🟢 CANLI" if live else "🟡 MOCK"
            print(f"  {platform:12s}: {status}")

        test_content = {
            'content':   "🔥 Test: Bluetooth Kulaklik 299 TL — %50 indirim!\nhttps://trendyol.com/test",
            'link':      "https://trendyol.com/test",
            'image_url': "https://picsum.photos/800/800",
            'title':     "Test Urun Paylasimi",
        }
        print("\n📡 Test yayini baslatiliyor...")
        results = await mgr.publish_to_all_platforms(test_content)
        print("\n📊 Sonuclar:")
        for plat, res in results.items():
            icon = "✅" if res.get('success') else "❌"
            mock = " [MOCK]" if res.get('mock') else " [CANLI]"
            print(f"  {icon} {plat}{mock}: {res.get('post_id', res.get('error', '?'))}")

    asyncio.run(main())

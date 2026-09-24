#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Stories Scraper
Scrapes stories from the current day (last 24 hours)

Uses the SAME endpoint and method as the reel extractor.

Usage:
    python instagramStoriesScraper.py <user_id>
"""

import requests
import json
import sys
import os
import time
import subprocess
import re
from datetime import datetime, timedelta
from urllib.parse import quote, urlencode, quote_from_bytes


def create_story_payload(user_id: str):
    """
    Create payload for fetching stories using the SAME method as reels.
    
    Stories use a different doc_id and query name than reels.
    """
    # Stories query uses a different doc_id
    doc_id = "29184890191114309"  # Stories endpoint doc_id
    
    # Get current timestamp for __d parameter
    current_time = int(datetime.now().timestamp())
    current_time_str = datetime.now().strftime('%Y%m%dT%H%M%S')
    
    # Get current rev - use subprocess with proper args
    try:
        rev_output = subprocess.check_output(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}'],
            stderr=subprocess.DEVNULL
        )
        rev = rev_output.strip().decode('utf-8')
    except:
        rev = "1048159918"  # Default fallback
    
    # Build payload similar to reel extractor
    # This mimics the Instagram session cookies
    import json
    variables = json.dumps({'user_id': user_id, 'max_id': '', 'first': 100})
    
    # Convert username to numeric user_id
    try:
        numeric_user_id = int(user_id)
    except ValueError:
        # Try to extract number from username - try common patterns
        for pattern in [r'\d+', r'(\d{4,})', r'(\d+)\.(\d+)']:
            match = re.search(pattern, user_id)
            if match:
                numeric_user_id = int(match.group(0))
                break
        else:
            raise ValueError(f"Cannot convert '{user_id}' to numeric user_id")
    
    payload = f"""
av=1&__d={current_time_str}&__user=0&__a=1&__req=q&__hs=20718.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev={rev}&__s=zkak6z%3At7hnq5%3Az992cx&__hsi=7688463637682775812&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyEiw50x609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q0HU1wEbUGdwtUeo9UaQ0Lo6-bwHwKG6Ufk0zU8oC1IwjUpwlAcwBwUQp1yU426V8aUuwm8jxK0-8KmUhw4rwXyFEaVE4616wAwj83KwRyrg5e&__csr=gQw8YcTqtgx55lrWYFay7XL-4bklFROlfF46E_BiliWnWR-j_apABWZqF6-mVVXKaGGExZjWtfBd7aOita9NRKqykHALQhbARKihA8CuAFaYWVmiJk9CKlaKCmui52qykTF6hEHBBzazHxmVlVXBl7x6ayFk5oCp1ebxucDUoxivyUgghgOXBm9KWmbKaDxWHGdZ5AG58KlU-uWUkKF9GxachF8KquibGfxvy88F84q1gAwcJ3bw5Zw08H-00Yp8cU4W07H8Qo9kawODu0ftws930Ro0hmw16q9yk0IE4ml0vQ5ozw2pUBpxM128xo1lE1zUO0TaiJ4yQ2G17xK1jwqEbQmVixm05MEvAy401JOw0BMUow3QS06EU3Sw3eo&__hsdp=g4d9Yj1AxbapbSdanklsHteLeyuPlc8wEB1yWKN0gJ1irq2o8F860x84e4i0Gxi1WglwkUoxtFAlJ0Ag9N0jwBxe4E5S1fw-BDwp69wn83swLx61mxiu1uwTxe16wgUgxK16wmFUsyoW2O0PVU0EO0Vo0xS0wo0zC0RUe86W07g84-3u0AO1e3O3m481PE3RwIw4rU6G0oe1vwcm09Sw2-UfE5O0Ulu8wqo2jo&__hblp=1y2CU5u3e3u7UkG8F9u8yUsxG6HwYwQzohDy-bAG54FoC1oCy8nwwwyzbo5qi1jGq2eqpdd0yQi2xrXDwyG9yoiwRwDDDwQyEfFpU62S9w_xCK6U-2-1swxwLzrCxe2Si8yUyu78463u4UeEK13Dy9UjwhEG2i2Gu6qy6dwwyU3fDw2eodosxSaz8W10wnU4Zo1A8eo21wdm7U1gU3nwUwrE0ZC081w8K3W1bwjo4-m36umcxW1p8iuq3O48623609DwIwbC1xU526oK0nu1vwsU5609Swa2ew8O16weq1kyEc8fEb8bU2BwXlUy1Eg2jo&__sjsp=g4dnYj5Mj9OIFAEjanklsHteLeyuOtswy2ya1aq2F1i01VAw&__comet_req=7&fb_dtsg=NAfzX6M8BkQ51T92E4tYI8L8KR3-ADsqsTa2QafU7bDemhKN896gT0w%3A17855905060073950%3A1785084411&jazoest=25831&lsd=tBGz0iqJiIOV4XEWSKFuHP&__spin_r=1048159918&__spin_b=trunk&__spin_t={current_time}&__crn=comet.igweb.PolarisStoriesV3ReelPageStandaloneRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisStoriesV3ReelPageStandaloneQuery&server_timestamps=true&variables={quote(variables, safe='')}&doc_id={doc_id}""".format(
        user_id=numeric_user_id,
        rev=rev
    )
    
    return payload


def scrape_instagram_stories(user_id: str):
    """
    Main function to scrape Instagram stories with error handling.
    
    Uses the same endpoint (https://www.instagram.com/graphql/query) and
    form-encoded method as the reel extractor.
    """
    try:
        payload = create_story_payload(user_id)
        print(payload)

        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'x-csrftoken': 'YuvV-QRvpR2Ggzgk0cTg1T',
            'x-ig-app-id': '936619743392459',
            'Cookie': 'csrftoken=YuvV-QRvpR2Ggzgk0cTg1T; mid=aOia4gALAAHSq3em2E34YEIFkMCC'
        }

        response = requests.post("https://www.instagram.com/graphql/query",
                                 headers=headers, data=payload, timeout=10)

        # Handle rate limiting
        if response.status_code == 429:
            return {
                "error": True,
                "status_code": 429,
                "message": "Rate limited. Please try again later."
            }

        # Handle not found
        if response.status_code == 404:
            return {
                "error": True,
                "status_code": 404,
                "message": "Stories not found or user has no stories."
            }

        # Handle other HTTP errors
        if response.status_code != 200:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": f"HTTP error: {response.status_code}"
            }

        data = response.json()

        # Check if stories data exists in response
        # Stories endpoint returns data in user.story_media
        if not data.get('data', {}).get('user', {}).get('story_media'):
            return {
                "error": True,
                "status_code": 404,
                "message": "Stories data not found in response"
            }

        # Save successful response
        filename = f'{user_id}_stories_response.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return {
            "error": False,
            "status_code": 200,
            "message": "Success",
            "filename": filename,
            "data": data
        }

    except ValueError as e:
        return {
            "error": True,
            "status_code": 400,
            "message": f"Invalid user_id: {str(e)}"
        }
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "status_code": 408,
            "message": "Request timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "status_code": 500,
            "message": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "error": True,
            "status_code": 500,
            "message": f"Unexpected error: {str(e)}"
        }


def download_stories(data, output_dir=".instagram_stories"):
    """Download story images from the scraped data."""
    import shutil
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy existing story folders if they exist
    if os.path.exists(".instagram_stories"):
        story_dirs = [d for d in os.listdir(".instagram_stories") 
                      if os.path.isdir(os.path.join(".instagram_stories", d))]
        for story_dir in story_dirs:
            shutil.copytree(
                os.path.join(".instagram_stories", story_dir),
                os.path.join(output_dir, story_dir),
                dirs_exist_ok=True
            )
    
    total_downloaded = 0
    user_id = data["data"]["user"]["user_id"]
    stories = data["data"]["user"].get("story_media", [])
    
    print(f"\nDownloading {len(stories)} stories...")
    
    for story in stories:
        story_id = story.get("id", "")
        image_urls = story.get("image_versions2", {}).get("photos", [])
        
        for img in image_urls:
            url = img.get("url")
            if url:
                filename = f"{user_id}_{story_id}_{img['width']}x{img['height']}.jpg"
                filepath = os.path.join(output_dir, user_id, filename)
                
                try:
                    print(f"  Downloading: {img['width']}x{img['height']}")
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        with open(filepath, "wb") as f:
                            f.write(response.content)
                        total_downloaded += 1
                        print(f"    ✓ Saved: {filepath}")
                    else:
                        print(f"    ❌ Failed: HTTP {response.status_code}")
                except Exception as e:
                    print(f"    ❌ Error: {e}")
    
    print(f"\n" + "="*60)
    print(f"Total downloaded: {total_downloaded}")
    print(f"Output directory: {output_dir}")
    print(f"Stories saved to: {output_dir}/{user_id}")
    print("="*60)
    
    return total_downloaded


def main():
    if len(sys.argv) < 2:
        print("Instagram Stories Scraper")
        print("="*60)
        print("\nUsage:")
        print("  python instagramStoriesScraper.py <user_id>")
        print("\nExamples:")
        print("  python instagramStoriesScraper.py instagram")
        print("  python instagramStoriesScraper.py 123456789")
        print("\nNote: Stories expire after 24 hours and require user to be online.")
        print("="*60)
        sys.exit(1)
    
    user_id = sys.argv[1]
    
    print("📖 Instagram Stories Scraper")
    print("="*60)
    print(f"Fetching stories for: {user_id}")
    print("(Stories from current day / 24 hours)")
    print("="*60)
    
    # Fetch stories
    result = scrape_instagram_stories(user_id)
    
    if result["error"]:
        print(f"\n❌ Error: {result['message']}")
        print("\nNote: Stories expire after 24 hours and require the user to be")
        print("online. If the user is offline, stories may not be available.")
        sys.exit(1)
    
    print("\n📥 Downloading stories...")
    print("="*60)
    
    # Download stories
    download_stories(result["data"])


if __name__ == "__main__":
    main()

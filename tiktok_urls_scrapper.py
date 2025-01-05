"""
Xpaths:
-> //div[@aria-label="Watch in full screen"]//a  (Video Urls Xpath)
-> //div[@aria-label="Watch in full screen"]//a//strong[@data-e2e="video-views"]  (Likes on that Video)

Get it in the format of .csv file:
Referenced in the file *tiktok_reference.csv*

Python Version: 12.5
"""

import asyncio
from playwright.async_api import async_playwright
import csv
from datetime import datetime

async def scrape_tiktok(query, max_videos=100):
    url = f"https://www.tiktok.com/search?q={query}"
    output_file = "tiktok_scraped_data.csv"
    vpn_extension_path = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Harsh\Extensions\omghfjlpggmjjaagoclmmobgdodcjboh\3.87.5_0"


    # Write CSV header
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sr_no", "date_time", "urls", "category", "likes"])

    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False)
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            args=[
                f"--disable-extensions-except={vpn_extension_path}",
                f"--load-extension={vpn_extension_path}"
            ]
        )
        # context = await browser.new_context()
        page = await browser.new_page()
        await page.goto(url, timeout=900000)

        scraped_data = []

        async def scroll_to_load():
            # Scroll until the bottom is reached or enough videos are collected
            previous_height = await page.evaluate("document.body.scrollHeight")
            while len(scraped_data) < max_videos:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)  # Wait for content to load
                current_height = await page.evaluate("document.body.scrollHeight")
                if current_height == previous_height:
                    break  # No more content to load
                previous_height = current_height

        await scroll_to_load()

        # Extract video URLs and views
        video_elements = await page.query_selector_all('//div[@data-e2e="search_top-item-list"]//div[@aria-label="Watch in full screen"]//a')
        view_elements = await page.query_selector_all('//div[@id="search-tabs"]/following-sibling::div[1]//div[@aria-label="Watch in full screen"]//a//strong[@data-e2e="video-views"]')

        for idx, (video_element, view_element) in enumerate(zip(video_elements, view_elements), start=1):
            if len(scraped_data) >= max_videos:
                break

            url = await video_element.get_attribute("href")
            views = await view_element.inner_text()

            scraped_data.append([
                idx,  # Serial Number
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date and Time
                url,
                query,  # Category
                views  # Views
            ])

        # Save to CSV
        with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(scraped_data)

        await browser.close()

    print(f"Scraped {len(scraped_data)} videos. Data saved to {output_file}")

# Replace "ASMR" with your desired search query
asyncio.run(scrape_tiktok("ASMR"))

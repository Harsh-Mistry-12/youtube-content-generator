from playwright.sync_api import sync_playwright
import json
import time

def save_cookies(cookies, file_path="cookies.json"):
    with open(file_path, "w") as f:
        json.dump(cookies, f, indent=4)
    print(f"Cookies saved to {file_path}")

def get_tiktok_cookies_with_vpn(vpn_extension_path):
    with sync_playwright() as p:
        # Launch browser with VPN extension enabled
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            args=[
                f"--disable-extensions-except={vpn_extension_path}",
                f"--load-extension={vpn_extension_path}",
                "--no-sandbox",
                "--start-maximized"
            ]
        )

        # Create a new page
        page = browser.new_page()
        
        # Add a small delay to ensure extension is loaded
        time.sleep(3)
        
        try:
            # Navigate to TikTok login page with wait until networkidle
            page.goto(
                "https://www.tiktok.com/login", 
                timeout=600000,
                wait_until="networkidle"
            )
            print("Successfully navigated to TikTok login page")
            
            # Wait for user to log in
            page.wait_for_selector("//div[@data-e2e='profile-icon']", timeout=60000)
            print("Login detected.")

            # Get cookies after login
            cookies = browser.cookies()
            save_cookies(cookies)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
        finally:
            browser.close()

# Provide the path to your VPN extension directory
vpn_extension_path = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Harsh\Extensions\omghfjlpggmjjaagoclmmobgdodcjboh\3.87.5_0"
get_tiktok_cookies_with_vpn(vpn_extension_path)
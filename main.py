from seleniumbase import SB
from selenium.webdriver.common.by import By
import time
import json
import os
import random  # Added for randomization
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def navigate_instagram(
    target_account, 
    username=os.getenv("INSTAGRAM_USERNAME"), 
    password=os.getenv("INSTAGRAM_PASSWORD")
):
    cookie_file = "cookies.json"
    base_url = "https://www.instagram.com/"
    target_url = f"{base_url}{target_account}/"

    with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
        if os.path.exists(cookie_file):
            # Open target page to establish domain context
            sb.open(target_url)
            time.sleep(5)
            # Load and add cookies
            with open(cookie_file, "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    sb.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Error adding cookie {cookie}: {e}")
            # Refresh to apply cookies and load authenticated session
            sb.open(target_url)
            time.sleep(5)
        else:
            # Log in if no cookies exist
            login_url = "https://www.instagram.com/accounts/login/"
            sb.open(login_url)
            time.sleep(5)
            sb.press_keys('input[name="username"]', username)
            sb.press_keys('input[name="password"]', password)
            sb.click('button[type="submit"]')
            time.sleep(10)  # Wait for login to complete
            # Save cookies for future sessions
            cookies = sb.get_cookies()
            with open(cookie_file, "w") as f:
                json.dump(cookies, f)
            # Navigate directly to target page
            sb.open(target_url)
            time.sleep(5)

        sb.save_screenshot("instagram_profile.png")
        print("Screenshot saved as 'instagram_profile.png'")
        time.sleep(2)
        
        # Get the number of followers
        followers = sb.get_text("ul li:nth-child(2) a span")
        
        followers_count = int(followers.replace(",", ""))
        print(f"Followers: {followers_count}")
        
        #click on followers
        sb.click("ul li:nth-child(2) a")
        
        #wait for load
        time.sleep(3)
        
        #screenshot
        sb.save_screenshot("followers.png")
        
        # Wait for the followers modal to appear and find its scrollable container
        modal = sb.driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")

        base_scroll_amount = 1000
        while True:
            current_scroll = sb.driver.execute_script("return arguments[0].scrollTop", modal)
            
            # Add randomization to scroll amount (base_scroll_amount ± 50)
            random_scroll = base_scroll_amount + random.randint(-50, 50)
            sb.driver.execute_script(f"arguments[0].scrollTop += {random_scroll}", modal)
            
            time.sleep(3)
            new_scroll = sb.driver.execute_script("return arguments[0].scrollTop", modal)
            if new_scroll == current_scroll:
                break

        #get modals children parent
        users_parent_container = sb.driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div")
        
        #save to HTML file
        with open(f"{target_account}_followers.html", "w", encoding="utf-8") as f:
            f.write(users_parent_container.get_attribute("outerHTML"))

            
       
        sb.save_screenshot("followers_bottom.png")
        print("Screenshot saved as 'followers_bottom.png'")
        
            
def extract_users(target):
    print("Extracting users...")

    with open(f"{target}_followers.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    users = []
    # Get the container holding all user divs
    master_div = soup.find("div", style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;")
    user_divs = master_div.find_all("div", recursive=False)
    print(f"Found {len(user_divs)} users")
    
    for user_div in user_divs:
        # Find the profile image using the alt text filter.
        img_tag = user_div.find("img", alt=lambda alt: alt and "profile picture" in alt)
        if not img_tag or not img_tag.get("src"):
            continue
        image = img_tag["src"]
        
        # Find the <a> tag that contains the username and profile link.
        a_tag = user_div.find("a", href=True)
        if not a_tag:
            continue
        link = a_tag["href"]
        username_span = a_tag.find("span", dir="auto")
        username = username_span.get_text(strip=True) if username_span else ""
        
        # Find the full name.
        # In this HTML snippet, the full name appears in a <span> outside the <a> tag.
        # Here we look for a span with a known class fragment (e.g., "x193iq5w")
        full_name_span = user_div.find("span", class_=lambda cls: cls and "x193iq5w" in cls)
        full_name = full_name_span.get_text(strip=True) if full_name_span else ""
        
        users.append({
            "image": image,
            "username": link.strip("/"),
            "full_name": full_name
        })
        
    #loop over users, print count where fields are empty
    username_count = 0
    name_count = 0
    for user in users:
        if not user["username"]:
            username_count += 1
        if not user["full_name"]:
            name_count += 1
            
        
            
    print(f"Found {username_count} users without a username")
    print(f"Found {name_count} users without a full name")
    
    return users


if __name__ == "__main__":
    start_time = time.time()
    target_account="fg.dae"
    navigate_instagram(target_account)
    users = extract_users(target_account)
    
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
        
    print(f"Users saved to 'users.json'")
    
    execution_time = time.time() - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(f"Execution time: {int(minutes)}:{seconds:.2f} minutes")
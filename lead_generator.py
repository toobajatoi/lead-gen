from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import csv
import re
import os
from urllib.parse import urljoin

# --- Configuration & Setup ---

def get_driver():
    """Initializes and returns a stealth Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Run in headless mode if on Render (or any server environment)
    if os.environ.get('RENDER'):
        print("Render environment detected. Running in headless mode.")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def load_linkedin_credentials():
    """Loads LinkedIn credentials from config.json."""
    if not os.path.exists('config.json'):
        print("Warning: `config.json` not found. LinkedIn scraping will be skipped.")
        return None, None
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            email = config.get("linkedin_email")
            password = config.get("linkedin_password")
            if not email or "YOUR_LINKEDIN_EMAIL" in email or not password or "YOUR_LINKEDIN_PASSWORD" in password:
                print("Warning: LinkedIn credentials in `config.json` are placeholders. Please update them.")
                return None, None
            return email, password
    except (json.JSONDecodeError, KeyError):
        print("Error: Could not read `config.json`. Please check its format.")
        return None, None

def login_to_linkedin(driver, email, password):
    """Logs into LinkedIn using provided credentials."""
    print("Attempting to log into LinkedIn...")
    try:
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Wait for either the home feed or a security check/error message
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.ID, "global-nav")),
                EC.presence_of_element_located((By.ID, "error-for-password")),
                EC.presence_of_element_located((By.CLASS_NAME, "form__input--captcha"))
            )
        )

        if "feed" in driver.current_url:
            print("LinkedIn login successful.")
            return True
        else:
            print("LinkedIn login failed. Check credentials or solve CAPTCHA if present.")
            return False
    except TimeoutException:
        print("Timeout during LinkedIn login. The page structure may have changed.")
        return False
    except Exception as e:
        print(f"An error occurred during LinkedIn login: {e}")
        return False

# --- Google Maps Scraping ---

def collect_place_urls(driver, query, max_results):
    """Phase 1: Scrolls through search results to collect unique business URLs."""
    driver.get(f"https://www.google.com/maps/search/{query.replace(' ', '+')}")
    print("Navigated to Google Maps search results...")

    try:
        feed_selector = "[role='feed']"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, feed_selector)))
        print("Results feed loaded. Collecting business URLs...")
    except TimeoutException:
        print("Error: Could not find results feed. The page structure may have changed.")
        return []

    urls = set()
    last_url_count = 0
    scroll_attempts = 0
    
    while len(urls) < max_results and scroll_attempts < 20:
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
        for link in links:
            href = link.get_attribute('href')
            if href and href not in urls:
                urls.add(href)

        if len(urls) >= max_results:
            print(f"Collected {len(urls)} URLs, reaching max results limit.")
            break

        try:
            scrollable_feed = driver.find_element(By.CSS_SELECTOR, feed_selector)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_feed)
            time.sleep(2.5)
        except Exception as e:
            print(f"Scrolling error: {e}. Ending URL collection.")
            break

        if len(urls) == last_url_count:
            scroll_attempts += 1
            print(f"No new URLs found in last scroll, attempt {scroll_attempts}/20.")
        else:
            last_url_count = len(urls)
            scroll_attempts = 0
            
    return list(urls)[:max_results]

def find_robust_detail(driver, icon_name, data_type):
    """Finds a detail (Address, Website, Phone) using multiple reliable methods."""
    try:
        element = driver.find_element(By.CSS_SELECTOR, f"button[data-item-id*='{icon_name}']")
        label = element.get_attribute("aria-label")
        if label:
            return label.replace(f"{data_type}:", "").strip()
    except Exception:
        pass
    
    try:
        element = driver.find_element(By.CSS_SELECTOR, f"a[aria-label*='{data_type}']")
        if data_type == "Website":
            return element.get_attribute('href')
        label = element.get_attribute("aria-label")
        if label:
            return label.replace(f"{data_type}:", "").strip()
    except Exception:
        pass
        
    return ""

def scrape_place_details(driver, url, linkedin_session_active):
    """Phase 2: Scrapes Google Maps details and performs a deep crawl of the website."""
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
    except TimeoutException:
        print(f"Failed to load details page for {url}")
        return None

    details = {
        'name': '', 'rating': '', 'reviews': '', 'category': '', 'address': '', 
        'website': '', 'phone': '', 'emails': [], 'contacts': [],
        'linkedin_company_url': '', 'facebook_url': '', 'instagram_url': '', 'twitter_url': '',
        'google_maps_url': url
    }

    try: details['name'] = driver.find_element(By.CSS_SELECTOR, "h1").text
    except Exception: pass
    try:
        rating_text = driver.find_element(By.CSS_SELECTOR, "div.fontBodyMedium > span[aria-label]").get_attribute('aria-label')
        if rating_text:
            parts = rating_text.replace(',', '').split()
            details['rating'] = parts[0]
            if len(parts) > 2 and "review" in parts[2].lower(): details['reviews'] = parts[1]
    except Exception: pass
    details['address'] = find_robust_detail(driver, 'address', 'Address')
    details['website'] = find_robust_detail(driver, 'website', 'Website')
    details['phone'] = find_robust_detail(driver, 'phone', 'Phone')
    try: details['category'] = driver.find_element(By.CSS_SELECTOR, "button[jsaction*='category']").text
    except Exception: pass
    
    if details['website']:
        print(f"  -> Website found: {details['website']}. Deep crawling for contacts and social media...")
        website_details = deep_crawl_website(driver, details['website'], linkedin_session_active)
        details.update(website_details)
    else:
        print("  -> No website found on Google Maps.")

    return details if details['name'] else None

# --- Deep Website Crawling & Contact Extraction ---

def deep_crawl_website(driver, website_url, linkedin_session_active):
    """
    Performs a deep crawl on a website to extract emails, social media links, and detailed contact information.
    """
    if not website_url.startswith('http'):
        website_url = 'https://' + website_url

    original_window = driver.current_window_handle
    
    # Data containers
    aggregated_emails = set()
    aggregated_socials = {
        'linkedin_company_url': set(), 'facebook_url': set(), 
        'instagram_url': set(), 'twitter_url': set()
    }
    aggregated_contacts = {} # Use dict to de-duplicate by name

    urls_to_visit = {website_url}
    
    # Phase 1: Discover key pages from the homepage
    driver.switch_to.new_window('tab')
    try:
        driver.get(website_url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        link_keywords = ['contact', 'about', 'team', 'staff', 'meet']
        all_links = driver.find_elements(By.TAG_NAME, 'a')
        for link in all_links:
            href = link.get_attribute('href')
            link_text = link.text.lower()
            if href and any(keyword in href.lower() or keyword in link_text for keyword in link_keywords):
                full_url = urljoin(website_url, href)
                urls_to_visit.add(full_url)
    except Exception as e:
        print(f"     Warning: Could not fully analyze homepage for links: {e}")
    finally:
        driver.close()
        driver.switch_to.window(original_window)

    # Phase 2: Visit each discovered page (up to 4) and extract info
    standalone_linkedin_profiles = set()
    for i, url_to_crawl in enumerate(list(urls_to_visit)[:4]):
        print(f"     -> Analyzing page {i+1}/{len(urls_to_visit)}: {url_to_crawl}")
        driver.switch_to.new_window('tab')
        try:
            driver.get(url_to_crawl)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            page_emails, page_socials, page_employees, page_linkedin_urls = extract_info_from_page(driver)
            
            aggregated_emails.update(page_emails)
            for platform, links in page_socials.items():
                aggregated_socials[platform].update(links)
            
            for emp in page_employees:
                if emp['name'] not in aggregated_contacts:
                    aggregated_contacts[emp['name']] = emp
            
            standalone_linkedin_profiles.update(page_linkedin_urls)
            
        except Exception as e:
            print(f"       Error analyzing {url_to_crawl}: {e}")
        finally:
            driver.close()
            driver.switch_to.window(original_window)

    # Phase 3: Scrape standalone LinkedIn profiles if session is active and not already found
    if linkedin_session_active:
        found_linkedin_urls = {c.get('linkedin_url') for c in aggregated_contacts.values() if c.get('linkedin_url')}
        profiles_to_scrape = list(standalone_linkedin_profiles - found_linkedin_urls)[:3] # Limit to 3 new profiles
        
        if profiles_to_scrape:
            print(f"     -> Found {len(profiles_to_scrape)} additional LinkedIn profiles to scrape...")
            for profile_url in profiles_to_scrape:
                profile_data = scrape_linkedin_profile(driver, profile_url)
                if profile_data and profile_data.get('name') not in aggregated_contacts:
                    aggregated_contacts[profile_data['name']] = profile_data

    # Consolidate final results
    final_details = {
        "emails": list(aggregated_emails),
        "contacts": list(aggregated_contacts.values()),
        "linkedin_company_url": next(iter(aggregated_socials['linkedin_company_url']), ''),
        "facebook_url": next(iter(aggregated_socials['facebook_url']), ''),
        "instagram_url": next(iter(aggregated_socials['instagram_url']), ''),
        "twitter_url": next(iter(aggregated_socials['twitter_url']), ''),
    }
    return final_details

def extract_info_from_page(driver):
    """Extracts all relevant information (emails, socials, employees) from the current page."""
    page_text = driver.find_element(By.TAG_NAME, 'body').text
    emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_text))
    
    # Extract social media links
    socials = {'linkedin_company_url': set(), 'facebook_url': set(), 'instagram_url': set(), 'twitter_url': set()}
    all_links = driver.find_elements(By.TAG_NAME, 'a')
    for link in all_links:
        href = link.get_attribute('href')
        if not href: continue
        if 'linkedin.com/company/' in href: socials['linkedin_company_url'].add(href.split('?')[0])
        elif 'facebook.com/' in href: socials['facebook_url'].add(href.split('?')[0])
        elif 'instagram.com/' in href: socials['instagram_url'].add(href.split('?')[0])
        elif 'twitter.com/' in href: socials['twitter_url'].add(href.split('?')[0])

    # Extract structured employee data
    employees = []
    linkedin_profile_urls = set()
    
    # Try to find common "team member" containers
    potential_containers = driver.find_elements(By.CSS_SELECTOR, 'div[class*="team"], div[class*="member"], div[class*="person"], li[class*="staff"]')
    for container in potential_containers:
        try:
            name_el = container.find_element(By.CSS_SELECTOR, 'h2, h3, h4, h5, h6')
            name = name_el.text.strip()

            title_el = container.find_element(By.CSS_SELECTOR, 'p, span[class*="title"], div[class*="role"], span[class*="job"]')
            title = title_el.text.strip()
            
            if name and title and len(name) < 50 and len(title) < 100:
                contact = {'name': name, 'title': title, 'email': '', 'linkedin_url': ''}
                try:
                    email_link = container.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]')
                    contact['email'] = email_link.get_attribute('href').replace('mailto:', '').split('?')[0]
                except NoSuchElementException: pass
                try:
                    linkedin_link = container.find_element(By.CSS_SELECTOR, 'a[href*="linkedin.com/in/"]')
                    contact['linkedin_url'] = linkedin_link.get_attribute('href').split('?')[0]
                except NoSuchElementException: pass
                employees.append(contact)
        except NoSuchElementException:
            continue

    # Also extract any standalone LinkedIn profile URLs on the page
    for link in all_links:
        href = link.get_attribute('href')
        if href and 'linkedin.com/in/' in href:
            linkedin_profile_urls.add(href.split('?')[0])

    return emails, socials, employees, linkedin_profile_urls

def scrape_linkedin_profile(driver, profile_url):
    """Scrapes name, title, and other details from a LinkedIn profile."""
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    profile_data = {'name': '', 'title': '', 'email': '', 'linkedin_url': profile_url}
    
    try:
        driver.get(profile_url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pv-top-card")))
        
        try: profile_data['name'] = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text
        except NoSuchElementException: print("         Could not find name element.")
            
        try: profile_data['title'] = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text
        except NoSuchElementException: print("         Could not find title element.")

    except TimeoutException: print(f"         Timeout loading {profile_url}")
    except Exception as e: print(f"         An error scraping {profile_url}: {e}")
    finally:
        driver.close()
        driver.switch_to.window(original_window)
        
    return profile_data if profile_data['name'] else None

# --- Data Handling ---

def save_results(businesses, query):
    """Saves the scraped data to JSON and CSV files."""
    if not businesses:
        print("No data to save.")
        return
        
    clean_query = re.sub(r'[^\w\s-]', '', query).strip().replace(' ', '_')
    json_filename = f"leads_{clean_query}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(businesses, f, indent=4, ensure_ascii=False)
    print(f"Results saved to {json_filename}")
    
    csv_filename = f"leads_{clean_query}.csv"
    fieldnames = [
        'name', 'rating', 'reviews', 'category', 'address', 'website', 'phone', 'emails', 
        'linkedin_company_url', 'facebook_url', 'instagram_url', 'twitter_url', 
        'contacts', 'google_maps_url'
    ]
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for business in businesses:
            business['emails'] = ', '.join(business.get('emails', []))
            
            # Format the contacts list into a readable string for the CSV
            contacts = business.get('contacts', [])
            contact_strings = []
            for c in contacts:
                parts = [c.get('name', 'N/A')]
                if c.get('title'): parts.append(f"({c.get('title')})")
                if c.get('email'): parts.append(f"<{c.get('email')}>")
                if c.get('linkedin_url'): parts.append(f"[{c.get('linkedin_url')}]")
                contact_strings.append(' '.join(parts))
            business['contacts'] = ' | '.join(contact_strings)
            
            writer.writerow(business)
    print(f"Results saved to {csv_filename}")

# --- Main Execution ---

def main():
    print("Lead Generator - LinkedIn Edition (v10.0)")
    print("=" * 50)

    # These are now hardcoded for the web app, but can be changed for direct script use
    try:
        query = input("Enter search query (e.g., 'restaurants in new york'): ").strip()
        if not query:
            print("No query entered. Exiting.")
            return
        
        max_results_str = input("Enter target number of leads (e.g., 50): ")
        max_results = int(max_results_str) if max_results_str.isdigit() else 50
    except (EOFError, KeyboardInterrupt):
        print("\nScript interrupted by web server. Exiting.")
        return

    driver = None
    linkedin_session_active = False
    try:
        email, password = load_linkedin_credentials()
        driver = get_driver()
        
        if email and password:
            linkedin_session_active = login_to_linkedin(driver, email, password)
        
        urls = collect_place_urls(driver, query, max_results)
        print(f"\nCollected {len(urls)} unique URLs. Now scraping details...")
        
        businesses = []
        for i, url in enumerate(urls):
            print(f"Processing {i+1}/{len(urls)}: {url[:70]}...")
            details = scrape_place_details(driver, url, linkedin_session_active)
            if details:
                businesses.append(details)
        
        print(f"\nScraping complete. Processed {len(businesses)} businesses.")
        save_results(businesses, query)
        
    except Exception as e:
        print(f"\nAn unexpected error occurred in main: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Initialize the WebDriver (assuming you have Chrome WebDriver)
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://firstmfg.com/collections/mens-jackets"

# Set to store visited URLs
visited_urls = set()

# Function to scrape links recursively
def scrape_links(url):
    try:
        # Add the URL to the set of visited URLs
        visited_urls.add(url)

        # Open the webpage
        driver.get(url)

        # Wait for all links to be loaded
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

        # Find all <a> elements
        link_elements = driver.find_elements(By.TAG_NAME, "a")

        # Extract the URLs from the elements
        for element in link_elements:
            link = element.get_attribute('href')
            if link and ("https://firstmfg.com/collections/" in link or "https://firstmfg.com/products/" in link) and link not in visited_urls:
                # Print the link
                print("Found:", link)
                # Recursively scrape links if needed
                scrape_links(link)
    except StaleElementReferenceException:
        # If StaleElementReferenceException occurs, refresh the page and retry
        print("StaleElementReferenceException occurred. Refreshing the page...")
        driver.refresh()
        scrape_links(url)

# Start scraping from the base URL
scrape_links(base_url)

# Close the WebDriver
driver.quit()
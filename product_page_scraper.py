import requests
import selenium 
from selenium import webdriver
import time 
import os 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def scrape_page_for_info(url, driver):
    # Selenium code to scrape information from the page
    # takes in a url and a driver to process 
    # retrieves product title, images, price, sku, sizes, price combos, colors/options and description


    # TITLE -------------------------------------------------------------
    section_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'product__section-title')]"))
    )
    title_text = section_title.text
    print("Title:", title_text)


    # PRODUCT IMAGES -------------------------------------------------------------
    carousel_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'js-carousel')]"))
    )

    image_elements = carousel_element.find_elements(By.TAG_NAME, "img")
    image_urls = [element.get_attribute("src") for element in image_elements]

    os.makedirs("images", exist_ok=True)
    folder_path = os.path.join("images", title_text)
    os.makedirs(folder_path, exist_ok=True)

    # Download and save each image
    for idx, url in enumerate(image_urls):
        response = requests.get(url)
        if response.status_code == 200:
            # filename = f"images/{title_text}{idx}.jpg"
            filename = os.path.join(folder_path, f"image{idx}.jpg")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image {idx} saved successfully.")
        else:
            print(f"Failed to download image {idx}.")


    # PRICE------------------
    price_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.price#product-price"))
    )
    price_text = price_div.text
    print("Price:", price_text)


    # SKU------------------
    sku_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'product__sku-value')]"))
    )
    sku_value = sku_element.text
    print("SKU:", sku_value)


    # SIZE-----------------
    size_elements = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".swatches__swatch--regular"))
    )

    size_values = [element.text for element in size_elements]
    print("Size Options:", size_values)


    # SIZE PRICE CHANGES -----------------
    previous_price = price_text

    # Loop through each size element
    for size_element in size_elements:
        # Click on the size element
        size_element.click()
        size_value = size_element.text.strip()
        
        # Wait for the price element to be visible
        price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.price#product-price"))
        )

        # Extract the price text
        price_text = price_element.text
        
        # Check if there is a price change
        if previous_price is not None and price_text != previous_price:
            print(f"Price changed for size {size_value}! Previous price: {previous_price}, New price: {price_text}")
        else:
            print(f"Price remained the same for size {size_value}.")

        # Update the previous price
        previous_price = price_text


    # SWATCHES ----------------------------------------------
    # Find all elements with class "swatches__container"
    swatches_containers = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "swatches__container"))
    )

    # Loop through each swatches container
    for swatches_container in swatches_containers:
        # Extract the option name text
        option_name = swatches_container.find_element(By.CLASS_NAME, "swatches__option-name").text.strip()
        print(f"Option Name: {option_name}")

        # Extract the values in "swatches__swatch"
        swatch_elements = swatches_container.find_elements(By.CLASS_NAME, "swatches__swatch")
        for swatch_element in swatch_elements:
            swatch_value = swatch_element.text.strip()
            print(f"Swatch Value: {swatch_value}")


    # TO DO: DESCRIPTION
        
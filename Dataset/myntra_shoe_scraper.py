# import bs4
# import time
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By


# options = Options()
# options.headless = True
# # Create your driver
# driver = webdriver.Firefox(options = options)

# url = "https://www.myntra.com/casual-shoes/skechers/skechers-men-dlux-walker-orford-slip-on-sneakers/24606750/buy"
# driver.get(url)

# print("----"*50)
# ele1 = driver.find_element(By.CLASS_NAME, value="pdp-name")
# print("ele1: ", ele1.get_attribute('innerHTML'))

# print("----"*50)
# ele2 = driver.find_element(By.CLASS_NAME, value="pdp-product-description-content")
# print("ele2: ", ele2.get_attribute('innerHTML'))

# print("----"*50)
# ele3 = driver.find_element(By.CLASS_NAME, value="index-tableContainer")
# print("ele3: ", ele3.get_attribute('innerHTML'))

# print("----"*50)
# ele4 = driver.find_elements(By.CLASS_NAME, value="image-grid-imageContainer")
# print("ele4: ", ele4[1].get_attribute('innerHTML'))

import re
import bs4
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# Initialize WebDriver with headless mode
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Read links from file
with open("output_links.txt", "r") as file:
    links = [line.strip() for line in file if line.strip()]

# Load the target webpage
url = "https://www.myntra.com/sports-shoes/hrx+by+hrithik+roshan/hrx-by-hrithik-roshan-women-white--pink-lace-up-running-shoes/23976344/buy"
driver.get(url)

# Extract elements
ele1 = driver.find_element(By.CLASS_NAME, "pdp-name").get_attribute("innerHTML").strip()
ele2_html = driver.find_element(By.CLASS_NAME, "pdp-product-description-content").get_attribute("innerHTML")
ele3_html = driver.find_element(By.CLASS_NAME, "index-tableContainer").get_attribute("innerHTML")

# Extract image URL
# Extracting image URL
ele4_html = driver.find_elements(By.CLASS_NAME, "image-grid-imageContainer")[1].get_attribute("innerHTML")
image_url_match = re.search(r'url\(&quot;(.*?)&quot;\)', ele4_html)
image_url = image_url_match.group(1) if image_url_match else ""

# Function to clean and format product description
def parse_description(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    text = ""
    
    for tag in soup.children:
        if tag.name == "b":  # Headers like "SPECIAL TECHNOLOGIES:"
            if text and text[-1] not in ".:":
                text += ". "
            text += tag.get_text(strip=True) + ": "
        elif tag.name == "ul":  # List items with numbering
            for i, li in enumerate(tag.find_all("li"), start=1):
                text += f"{i}. {li.get_text(strip=True)}, "
        elif tag.name == "br":  # Handle line breaks
            text += ", "
        else:  # General text
            text += tag.get_text(strip=True) + " "
    
    return text.strip()

# Function to parse product specifications
def parse_specifications(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    specs = []
    
    rows = soup.find_all("div", class_="index-row")
    for row in rows:
        key = row.find("div", class_="index-rowKey").get_text(strip=True)
        value = row.find("div", class_="index-rowValue").get_text(strip=True)
        specs.append(f"{key}: {value}")
    
    return ", ".join(specs)

# Extract and format text
description_text = parse_description(ele2_html)
specs_text = parse_specifications(ele3_html)
final_text = f"{ele1}. {description_text}. {specs_text}."

# Cleanup function for redundant punctuation and special characters
def clean_text(text):
    text = re.sub(r"\s*,\s*,+", ", ", text)  # Remove consecutive commas
    text = re.sub(r"\s*\.\s*\.", ".", text)  # Remove consecutive periods
    text = re.sub(r":\s*:", ":", text)  # Fix colons
    text = re.sub(r"\s*([.,:])", r"\1", text)  # Trim spaces before punctuation
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    return text

# Apply final cleanup
final_text = clean_text(final_text)

# Create final dictionary
product_data = {
    "text": final_text,
    "image_url": image_url
}

# Print the final dictionary
print(product_data)

# Close the browser
driver.quit()

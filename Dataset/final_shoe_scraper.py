import json
import re
import bs4
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm

# Initialize WebDriver
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Read links from file
with open("output_links.txt", "r") as file:
    links = [line.strip() for line in file if line.strip()]

base_url = "https://www.myntra.com/"
product_data_list = []

def parse_description(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    text = ""
    for tag in soup.children:
        if tag.name == "b":
            if text and text[-1] not in ".:":
                text += ". "
            text += tag.get_text(strip=True) + ": "
        elif tag.name == "ul":
            for i, li in enumerate(tag.find_all("li"), start=1):
                text += f"{i}. {li.get_text(strip=True)}, "
        elif tag.name == "br":
            text += ", "
        else:
            text += tag.get_text(strip=True) + " "
    return text.strip()

def parse_specifications(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    specs = []
    rows = soup.find_all("div", class_="index-row")
    for row in rows:
        key = row.find("div", class_="index-rowKey").get_text(strip=True)
        value = row.find("div", class_="index-rowValue").get_text(strip=True)
        specs.append(f"{key}: {value}")
    return ", ".join(specs)

def clean_text(text):
    text = re.sub(r"\s*,\s*,+", ", ", text)
    text = re.sub(r"\s*\.\s*\.", ".", text)
    text = re.sub(r":\s*:", ":", text)
    text = re.sub(r"\s*([.,:])", r"\1", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

for link in tqdm(links, total=len(links)):
    try:
        full_url = base_url + link
        driver.get(full_url)
        time.sleep(2)  # Allow page to load

        ele1 = driver.find_element(By.CLASS_NAME, "pdp-name").text.strip()
        ele2_html = driver.find_element(By.CLASS_NAME, "pdp-product-description-content").get_attribute("innerHTML")
        ele3_html = driver.find_element(By.CLASS_NAME, "index-tableContainer").get_attribute("innerHTML")

        # Extracting image URL
        ele4_html = driver.find_elements(By.CLASS_NAME, "image-grid-imageContainer")[1].get_attribute("innerHTML")
        image_url_match = re.search(r'url\(&quot;(.*?)&quot;\)', ele4_html)
        image_url = image_url_match.group(1) if image_url_match else ""

        description_text = parse_description(ele2_html)
        specs_text = parse_specifications(ele3_html)
        final_text = f"{ele1}. {description_text}. {specs_text}."
        final_text = clean_text(final_text)

        product_data_list.append({
            "text": final_text,
            "image_url": image_url
        })
    except Exception as e:
        print(f"Error processing {full_url}: {e}")

# Save data to JSON file
with open("test_scraped_data.json", "w") as json_file:
    json.dump(product_data_list, json_file, indent=4)

# Close the browser
driver.quit()
print("Scraping completed. Data saved to test_scraped_data.json.")

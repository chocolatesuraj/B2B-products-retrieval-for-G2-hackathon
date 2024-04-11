import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


techstars_startup_df = pd.DataFrame(
    columns= ["name", "location", "website"],
)

driver = webdriver.Chrome()

# Load the webpage
url = "https://www.techstars.com/portfolio"
driver.get(url)

# Function to check if new elements are loaded
def are_new_elements_loaded(prev_count):
    current_count = len(driver.find_elements(By.CSS_SELECTOR, 'span.jss1081'))
    return current_count > prev_count

# Scroll down incrementally until no new elements are found
prev_elements_count = 0
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
    time.sleep(3)  # Wait for a moment after scrolling
    if not are_new_elements_loaded(prev_elements_count):
        break
    prev_elements_count = len(driver.find_elements(By.CSS_SELECTOR, 'span.jss1081'))
    
elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'jss585') and contains(@class, 'jss587') and contains(@class, 'jss629') and contains(@class, 'jss643') and contains(@class, 'jss657')]")
all_startup_locations = driver.find_elements(By.XPATH, "//p[contains(@class, 'jss693') and contains(@class, 'jss1083') and contains(@class, 'jss728') and contains(@class, 'jss739')]")

for element in elements:
    try:
        startup_name = element.find_element(By.CSS_SELECTOR, 'span.jss1081').text
    except:
        startup_name = ""
        
    try:
        startup_url = element.find_element(By.CSS_SELECTOR, 'a.jss1089').get_attribute('href')
    except:
        print(startup_name) ##list out the startup names that don't have a URL
        startup_url = ""  # Assign an empty string if URL element is not found
        
        
    techstars_startup_df = techstars_startup_df.append({"name": startup_name, "location": "", "website": startup_url}, ignore_index=True)


url_list = []
tags_list = []
all_startup_locations = driver.find_elements(By.XPATH, "//p[contains(@class, 'jss693') and contains(@class, 'jss1083') and contains(@class, 'jss728') and contains(@class, 'jss739')]")
all_startup_locations = [i.text for i in  all_startup_locations] 

#Close the webdriver
driver.quit()

techstars_startup_df['location'] = all_startup_locations[::2] #extracting the locations out of the selected content
techstars_startup_df.to_csv("techstars_scraped.csv", index=False)
#API_KEY = your api 
#SEARCH_ENGINE_ID = your search eninge id 
url = 'https://www.googleapis.com/customsearch/v1'


import requests
from bs4 import BeautifulSoup
import requests
import google.generativeai as genai
import os
import pandas as pd

def search_google(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': API_KEY,
        'cx':SEARCH_ENGINE_ID,
        'num': 3
    }

    response = requests.get(url, params=params)
    results = response.json()

    if 'items' in results:
        urls = [item['link'] for item in results['items'] if item['link'].startswith('https')]
        print(urls)
        return urls
    else:
        print('No search results found.')
        return []
    

def scrape_website(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Concatenate headers scraped from the webpage
        headers_content = "\n".join(header.text.strip() for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        
        # Concatenate paragraphs scraped from the webpage
        paragraphs_content = "\n".join(p.get_text() for p in soup.find_all('p'))
        
        # Combine headers and paragraphs content
        combined_content = headers_content + "\n\n" + paragraphs_content
        print('Scraping successful')
        return url, combined_content
    else:
        return url, "Failed to retrieve the webpage"

def generate_content_from_string(input_string):
    print('Generating content...')
    prompt='given all the information about the company, check if the company migth be making any b2b software if its fine if your not 100% sure. print the company name and if you know the soaftware name print it or else print the compay name itslef. print as a list- [comapny name, [list of software name],link]'
    input_string = prompt+input_string
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_string)
    
    return response.text
    
def process_companies_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    
    final_generated_contents = []
    
    for company in df['name']:  # Assuming 'Company_Name' is the column containing company names
        search_results = search_google(company)
        combined_search_content = ""
        
        if search_results:
            for url in search_results:
                content,message = scrape_website(url)
                
                if message != "Failed to retrieve the webpage":
                    combined_search_content += content+ "\n\n"
                    
        if combined_search_content:
            generated_content = generate_content_from_string(combined_search_content)
            print(f"Generated content for {company}: {generated_content}")
    
    # # Combine all final generated contents
    # final_content = "\n\n".join(final_generated_contents)
    
    # return final_content

path='C:/Users/xgadg/OneDrive/Desktop/g2_hack/company.csv'
process_companies_from_csv(path)
# data=scrape_website('https://zoom.us/')
# print(data)

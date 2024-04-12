API_KEY = 'AIzaSyAPWp4X8lmphuaMY1eHsnqFw5DDqu1soO0'
SEARCH_ENGINE_ID = 'f4658cbb644034be9'
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
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Concatenate headers scraped from the webpage
        headers_content = "\n".join(header.text.strip() for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        
        # Concatenate paragraphs scraped from the webpage
        paragraphs_content = "\n".join(p.get_text() for p in soup.find_all('p'))
        
        # Combine headers and paragraphs content
        combined_content = headers_content + "\n\n" + paragraphs_content
        print("scraping",url ,"done")
        return url, combined_content
    
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return url, "Failed to retrieve the webpage"

def generate_content_from_string(input_string):
    print('Generating content...')
    prompt=prompt='''given all the information about the company,list the b2b software the company makes.
    rember company name might be the softwae name too.print in the format- company name, list of software name seprated by commas
    '''
    input_string = prompt+input_string
    genai.configure(api_key=API_KEY)
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
    ]
    model = genai.GenerativeModel('gemini-pro',safety_settings=safety_settings)
    response = model.generate_content(input_string)
    
    return response.text
comb100=' '   
def process_companies_from_csv(csv_path):
    global comb100
    df = pd.read_csv(csv_path)
    i=0
    final_generated_contents = []
    
    for company in df['name']:  # Assuming 'Company_Name' is the column containing company names
        i=i+1
        search_results = search_google(company)
        combined_search_content = ""
        
        if search_results:
            for url in search_results:
                content,message = scrape_website(url)
                
                if message != "Failed to retrieve the webpage":
                    combined_search_content += content+ "\n\n"
        if combined_search_content:
            generated_content = generate_content_from_string(combined_search_content)
            print(f"{generated_content}")
            try:
                with open('C:/Users/xgadg/OneDrive/Desktop/g2_hack/gpt.txt', 'a') as the_file:
                    the_file.write(f"{generated_content}\n")  # Adding a newline for clarity
                    print('done writing')
                    comb100+=generated_content+ "\n\n"          

            except Exception as e:
                print(f"An error occurred: {e}")
        if(i==10):
            comb100= comb100 +"remove all lines that say couldnt find any b2b product and make in a csv format with company name,software products"
            generated_content = generate_content_from_string(comb100)
            print(f"{generated_content}")
            try:
                with open('C:/Users/xgadg/OneDrive/Desktop/g2_hack/clean.txt', 'a') as the_file:
                    the_file.write(f"{generated_content}\n")  # Adding a newline for clarity
                    print('done writing')
                    comb100=''
                    i=0

            except Exception as e:
                print(f"An error occurred: {e}")
                comb100=''
                i=0


        
    
    # # Combine all final generated contents
    # final_content = "\n\n".join(final_generated_contents)
    
    # return final_content

path='C:/Users/xgadg/OneDrive/Desktop/g2_hack/not_found_companies.csv'
process_companies_from_csv(path)
# data=scrape_website('https://zoom.us/')
# print(data)

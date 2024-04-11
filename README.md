# software-retrieval-for-G2-hackathon
![Image Alt text](/architecture.png "Architecture")

# software-retrieval-for-G2-hackathon

## ![Image Alt text](/architecture.png "Architecture")

## Requirements

- Python version 3.11.3 or higher
- Google Cloud account with:
  - Generative Language API
  - Custom Search API
- Search engine ID from Google's Programmable Search Engine
- Packages listed in `requirements.txt`

## Steps to Run

### 1. Get List of New Companies

You can get a list of new companies by either scraping the websites listed below or directly downloading the CSV files from the websites:

- [Techstars Portfolio](https://www.techstars.com/portfolio)
- [HK Companies Registry](https://data.gov.hk/en-data/dataset/hk-cr-crdata-list-newly-registered-companies-2324)
- [10,000 Startups](https://10000startups.com/our-startups)
- [Internshala](https://internshala.com/internships/matching-preferences/)
- [Endless Frontier Labs](https://endlessfrontierlabs.com/startups/)

### 2. Run Scraper

After obtaining the list of new companies, run the following command to scrape additional details:

```bash
python scraper.py

REQUIREMENTS:
Python version 3.11.3 or higher
google cloud account with 
  Generative Language API
  Custom Search API
search engine id from googles programable seach engine 
pip install -r requirements.txt

STEPS TO RUN:
get list of new companies by either scraping a website or directly downloading csv from website 
https://www.techstars.com/portfolio
https://data.gov.hk/en-data/dataset/hk-cr-crdata-list-newly-registered-companies-2324
https://10000startups.com/our-startups
https://internshala.com/internships/matching-preferences/
https://endlessfrontierlabs.com/startups/

then run 
python scraper.py

then run 
pyhton g2_filter.py 
to filter companies that are already on g2

then run 
python main.py




# software-retrieval-for-G2-hackathon
![Image Alt text](/architecture.png "Architecture")

# software-retrieval-for-G2-hackathon

## ![Image Alt text](/architecture.png "Architecture")

## Overview

This project aims to find B2B software for [G2](https://www.g2.com/) 

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
```


then run 
```bash
python scraper.py
```
then run
```bash
python g2_filter.py
```
to filter companies that are already on g2

then run
```bash
python main.py
```



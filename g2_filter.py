import requests
import json
import csv
import time

# Function to return a structured form of the JSON response
def return_response_dict(results):
    results_string = results.content.decode()
    results_dict = json.loads(results_string)
    return results_dict

# Load the API key from the config.json file
with open('config.json') as f:
    config = json.load(f)
api_key = config.get('API_ACCESS_TOKEN')

# Set the headers for the API request
headers = {
    "Authorization": f"Token token={api_key}",
    "Content-Type": "application/vnd.api+json"
}
not_found_companies = []
# Open the CSV file and read the companies
with open('final.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        company = row['name']
        url = row['website']

        # Extract the domain from the URL
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]

        # Construct the API request URL with the domain
        params = {
            "filter[domain]": domain,
            "page[size]": 1
        }

        try:
            start_time = time.time()
            product_results = requests.get("https://data.g2.com/api/v1/products", headers=headers, params=params, timeout=10)
            end_time = time.time()
            product_dict = return_response_dict(product_results)

            # Check if the company exists in the G2 data
            if product_dict["data"]:
                print(f"Company '{company}' found in G2. URL: {url}")
            else:
                # Company not found in G2 data, check if the URL exists
                slug = company.lower().replace(" ", "-")
                params = {
                    "filter[slug]": slug,
                    "page[size]": 1
                }
                product_results = requests.get("https://data.g2.com/api/v1/products", headers=headers, params=params, timeout=10)
                product_dict = return_response_dict(product_results)
                if product_dict["data"]:
                    print(f"Company '{company}' found in G2. URL: {url}")
                else:
                    print(f"Company '{company}' not found in G2. URL: {url} | Slug: {slug}")
                    not_found_companies.append({"name": company, "website": url})

        except requests.exceptions.Timeout:
            print(f"Timeout error for {company} ({url})")
        except Exception as e:
            print(f"Error for {company} ({url}): {e}")


with open('not_found_companies.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'website']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company in not_found_companies:
        writer.writerow(company)

print(f"Wrote {len(not_found_companies)} not found companies to 'not_found_companies.csv'.")

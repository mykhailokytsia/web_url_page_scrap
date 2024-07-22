import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_quotes(base_url, start_page, end_page):
    quotes = []
    authors = []

    for page in range(start_page, end_page + 1):
        url = f"{base_url}/page/{page}/"
        response = requests.get(url)

        if response.status_code == 200:
            response.encoding = 'utf-8'  # Ensure the response is treated as UTF-8
            soup = BeautifulSoup(response.text, "html.parser")

            for quote in soup.find_all('div', class_='quote'):
                text = quote.find('span', class_='text').get_text(strip=True)
                author = quote.find('small', class_='author').get_text(strip=True)
                quotes.append(text)
                authors.append(author)
        else:
            print(f"Page {page} does not exist. Status code: {response.status_code}")
            break  # Exit the loop if the page does not exist

    # Check if any results were found
    if quotes and authors:
        # Save the results to a CSV file
        df = pd.DataFrame({'Quote': quotes, 'Author': authors})
        df.to_csv('quotes.csv', index=False, encoding='utf-8-sig')
        print("CSV file created successfully with the following quotes and authors:")
        print(df)
    else:
        print("No quotes found.")

if __name__ == "__main__":
    base_url = 'http://quotes.toscrape.com'  # Base URL of the site to scrape
    start_page = 1  # Starting page
    end_page = 10  # Ending page (can be adjusted as needed)
    scrape_quotes(base_url, start_page, end_page)

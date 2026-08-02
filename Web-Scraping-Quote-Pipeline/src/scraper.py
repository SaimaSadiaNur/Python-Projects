import time
import requests
from bs4 import BeautifulSoup


def scrape_all_quotes() -> list[dict]:
    """Scrapes all quotes across all pages from quotes.toscrape.com.

    Returns a list of dictionaries containing quote text, author, and tags.
    """
    all_quotes = []
    page_number = 1

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print("Starting web scraping pipeline...")

    while True:
        url = f"http://quotes.toscrape.com/page/{page_number}/"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        quotes_on_page = soup.find_all("div", class_="quote")

        if not quotes_on_page:
            print(f"Scraping complete! Reached end at page {page_number}.")
            break

        for quote_div in quotes_on_page:
            quote_text = quote_div.find("span", class_="text").text.strip()
            author_text = quote_div.find("small", class_="author").text.strip()
            tags_list = [tag.text.strip() for tag in quote_div.find_all("a", class_="tag")]

            all_quotes.append({
                "quote": quote_text,
                "author": author_text,
                "tags": tags_list
            })

        print(f"   Fetched {len(quotes_on_page)} quotes from page {page_number}")
        page_number += 1
        time.sleep(0.5)

    print(f" Total quotes collected: {len(all_quotes)}\n")
    return all_quotes


if __name__ == "__main__":
    quotes_data = scrape_all_quotes()
    print("Sample record:", quotes_data[0])

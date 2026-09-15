"""
Online Book Marketplace Web Scraper

Scrapes book data from https://books.toscrape.com/
and saves a cleaned CSV file to data/books_cleaned.csv.
"""

from pathlib import Path
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def get_soup(url: str) -> BeautifulSoup:
    """Request a webpage and return a parsed BeautifulSoup object."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_stock_amount(product_url: str) -> int | None:
    """Visit a product page and extract the number of copies in stock."""
    soup = get_soup(product_url)

    availability = soup.select_one("p.instock.availability")
    if availability is None:
        return None

    match = re.search(r"\((\d+) available\)", availability.get_text(" ", strip=True))
    return int(match.group(1)) if match else None


def scrape_books() -> pd.DataFrame:
    """Scrape all catalogue pages and return the collected data."""
    records = []
    page_url = START_URL

    while page_url:
        soup = get_soup(page_url)
        books = soup.select("article.product_pod")

        for book in books:
            title = book.h3.a.get("title", "").strip()

            price_text = book.select_one("p.price_color").get_text(strip=True)
            price_gbp = float(
                price_text.replace("£", "").replace("Â", "").strip()
            )

            rating_classes = book.select_one("p.star-rating").get("class", [])
            rating_word = next(
                (value for value in rating_classes if value in RATING_MAP),
                None,
            )
            review = RATING_MAP.get(rating_word)

            availability = book.select_one("p.instock.availability").get_text(
                " ", strip=True
            )

            relative_link = book.h3.a["href"]
            product_url = requests.compat.urljoin(page_url, relative_link)
            stock_amount = extract_stock_amount(product_url)

            records.append(
                {
                    "Title": title,
                    "Price_GBP": price_gbp,
                    "Review": review,
                    "Availability": availability,
                    "Stock_Amount": stock_amount,
                }
            )

            # Small pause to avoid sending requests too aggressively.
            time.sleep(0.05)

        next_button = soup.select_one("li.next a")

        if next_button:
            page_url = requests.compat.urljoin(page_url, next_button["href"])
        else:
            page_url = None

    return pd.DataFrame(records)


def main() -> None:
    """Run the scraper and save the cleaned dataset."""
    df = scrape_books()

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "books_cleaned.csv"
    df.to_csv(output_path, index=False)

    print(f"Rows collected: {len(df):,}")
    print(f"Saved dataset to: {output_path}")
    print(df.head())


if __name__ == "__main__":
    main()

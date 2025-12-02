import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# ---------------------------
# CONFIG
# ---------------------------

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ---------------------------
# HELPERS
# ---------------------------

def get_page(url: str) -> str:
    """Download page HTML."""
    print(f"Fetching: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_books(html: str) -> list[dict]:
    """Extract book data from a single page."""
    soup = BeautifulSoup(html, "lxml")
    books = []

    articles = soup.select("article.product_pod")
    for art in articles:
        # title
        title = art.h3.a["title"]

        # price text, e.g. "£51.77" or sometimes appears as "Â51.77"
        price_text = art.select_one("p.price_color").get_text(strip=True)

        # availability
        availability = art.select_one("p.instock.availability").get_text(strip=True)

        # rating (e.g. "Three", "Four")
        rating_tag = art.select_one("p.star-rating")
        rating = rating_tag["class"][1] if rating_tag and len(rating_tag["class"]) > 1 else None

        books.append(
            {
                "title": title,
                "price_raw": price_text,
                "availability": availability,
                "rating": rating,
            }
        )

    return books


# ---------------------------
# SCRAPER
# ---------------------------

def scrape_books(num_pages: int = 5) -> pd.DataFrame:
    """
    Scrape the first num_pages pages from books.toscrape.com
    and return a pandas DataFrame.
    """
    all_books: list[dict] = []

    for page in range(1, num_pages + 1):
        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}catalogue/page-{page}.html"

        html = get_page(url)
        page_books = parse_books(html)
        print(f"  -> found {len(page_books)} books on page {page}")
        all_books.extend(page_books)

    df = pd.DataFrame(all_books)

    # -------- PRICE CLEANING FIX --------
    # Remove anything that is NOT a digit or dot (handles £, Â, etc.)
    df["price_clean"] = (
        df["price_raw"]
        .str.replace(r"[^0-9.]", "", regex=True)   # keep only 0–9 and .
        .astype(float)
    )
    # ------------------------------------

    return df


# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":
    print("Starting BooksToScrape project...")

    # scrape first 5 pages (you can change 5 to 10, etc.)
    df_books = scrape_books(num_pages=5)

    print(f"\nFinished scraping. Total rows: {df_books.shape[0]}")
    print("\nFirst few rows:")
    print(df_books.head())

    # ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # save to CSV
    output_path = os.path.join("data", "books_data.csv")
    df_books.to_csv(output_path, index=False)

    print(f"\nData saved to {output_path}")

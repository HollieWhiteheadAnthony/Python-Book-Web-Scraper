# Online Book Marketplace Web Scraper

A Python web-scraping project that collects product information from the practice website **Books to Scrape** and transforms the results into a clean, analysis-ready dataset.

This project was originally completed as part of my Data Analytics coursework and was later reorganized and documented as a portfolio project.

## Project Goal

The goal of this project was to practice the full early-stage data workflow:

1. Request data from a website.
2. Parse HTML content.
3. Navigate multiple pages.
4. Extract structured product information.
5. Clean and transform the collected data.
6. Export the finished dataset for analysis.

## Data Collected

For each book, the scraper collects:

- Title
- Price
- Review rating
- Availability
- Stock amount

The scraper follows the site's pagination until all available catalogue pages have been processed.

## Tools Used

- Python
- Requests
- BeautifulSoup
- Pandas
- Regular Expressions
- Selenium / browser inspection during development

## Workflow

### 1. Request the webpage

The project begins by sending an HTTP request to the catalogue page and checking that the response is successful.

### 2. Parse the HTML

BeautifulSoup is used to locate each book listing and extract the relevant fields.

### 3. Handle pagination

The scraper continues through catalogue pages until no `next` page is available.

### 4. Visit individual product pages

The catalogue page shows whether a book is in stock, but the exact stock quantity is stored on the individual product page. The scraper follows each product link to collect that value.

### 5. Clean the data

The raw scraped values are converted into analysis-friendly formats:

- Price is converted from text to a numeric value.
- Text-based star ratings are converted to integers from 1 to 5.
- Stock text is parsed to extract the numeric quantity.

### 6. Export the results

The final DataFrame is saved as:

`data/books_cleaned.csv`

</> Markdown
## Example Output

![Sample scraper output](images/sample-output.png)

| Title | Price_GBP | Review | Availability | Stock_Amount |
|---|---:|---:|---|---:|
| A Light in the Attic | 51.77 | 3 | In stock | 22 |
| Tipping the Velvet | 53.74 | 1 | In stock | 20 |
| Soumission | 50.10 | 1 | In stock | 20 |

## How to Run

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

Run the scraper:

```bash
python scraper.py
```

The cleaned CSV file will be created inside the `data` folder.

## Skills Demonstrated

This project demonstrates:

- Web scraping
- HTML parsing
- Pagination
- Data extraction
- Data cleaning
- Data-type conversion
- Regular expressions
- Pandas DataFrames
- CSV export
- Basic error handling
- Reproducible project organization

## Portfolio Note

The website used in this project, Books to Scrape, is specifically designed for practicing web scraping.

The original coursework produced a dataset of approximately 1,000 book records. This repository reorganizes that work into a cleaner, reproducible project format suitable for GitHub.

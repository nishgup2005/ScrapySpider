# PHHC Crawler

This project is a Scrapy-based web crawler for extracting case data from the Punjab and Haryana High Court website (https://www.phhc.gov.in/home.php?search_param=free_text_search_judgment). It collects data for all available case types over the last two months, in daily chunks, and exports the results to Excel and CSV formats.

## Features
- Crawls all case types and all days in the last two months
- Handles form-based search and pagination automatically
- Extracts all columns and links from the results table
- Logs cases where the site asks to "refine your query"
- Exports results to both `results.xlsx` (Excel) and `results.csv` (CSV)
- Highly configurable and easy to extend

## Project Structure
```
phhc_crawler/
├── phhc_crawler/
│   ├── __init__.py
│   ├── items.py           # Scrapy item definitions
│   ├── middlewares.py     # (Default) Scrapy middlewares
│   ├── pipelines.py       # Excel export pipeline (pandas)
│   ├── settings.py        # Scrapy settings (CSV & Excel export, logging)
│   └── spiders/
│       ├── __init__.py
│       ├── newspider.py   # Main spider for PHHC crawling
│       └── phhc_spider.py # (Optional/legacy) Additional spider(s)
├── crawl.log              # Log output (including refine your query warnings)
├── results.csv            # CSV export of crawl results
├── results.xlsx           # Excel export of crawl results
├── scrapy.cfg             # Scrapy project config
└── .gitignore
```

## Setup Instructions

### 1. Install Dependencies
This project requires Python 3.8+ and the following packages:
- Scrapy
- pandas
- openpyxl

Install them with:
```bash
pip install scrapy pandas openpyxl
```

### 2. Run the Crawler
From the project root, run:
```bash
scrapy crawl phhc_case_form_dynamic
```

- Results will be saved to `results.xlsx` and `results.csv`.
- Logs (including 'refine your query' warnings) are saved in `crawl.log`.

### 3. Configuration
- **Case types and date range**: Controlled in `newspider.py`.
- **Logging and output**: Controlled in `settings.py`.
- **Excel export logic**: See `pipelines.py`.

## Customization
- To crawl only specific case types, edit the logic in `parse_case_types` in `newspider.py`.
- To change output file names or formats, edit `settings.py` and/or `pipelines.py`.

## Notes
- The spider respects the website's robots.txt by default.
- This project is for research and legal data analysis only. Please use responsibly.

## License
This project is provided as-is for educational and research purposes.

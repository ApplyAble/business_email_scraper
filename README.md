# Google Scraper

Scrapes google entries for data on businesses

### Input
Filename: `businesses.csv`
| Business | ... |
| -------- | --- |
| Bagel Boys Brisbane | ... |
| The bakeologists | ... |


### Output
| title                                         | email             | snippet                                                                                  | other fields ... |
| --------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------- | ---------------- |
| The Bagel Boys - Brisbane QLD                 | example@email.com | For the last five years The Bagel Boys have been supplying Brisbane with the tastiest... | ...              |
| The Bagel Boys - Overview, News & Competitors |                   | Brisbane's Original Bagel Bakery                                                         | ...              |
| ...                                           | ...               | ...                                                                                      | ...              |
| The Bakeologists - Time Out                   | ...               | The Bakeologists cream filled pastry ... Our guide                                       | ...              |
| The Bakeologists, New Farm, Brisbane          | email@example.com | View reviews, menu, contact, location, and more                                          | ... |

___
### Setup

Install Dependencies
- Install: `python` and `anaconda`
- create a conda env: `conda create -n some_name`
- Install scrapy: `pip install scrapy`

Setup
- `git clone` this repo
- Make a `businesses.csv` file with your data *(see input format)*
- You need to use a proxy if you want to scrape at any reasonable scale. *If you don’t, you could get flagged and get your IP-banned*
    - Create a scraperapi account: follow [this link](https://www.scraperapi.com/signup)
- Paste your API key into the `.env` file as `API_KEY=<your_api_key>`

GPT3
- make an [OpenAI](https://labs.openai.com/) account and get the API keys
- Paste the API keys into `.env` as `OPEN_API_KEY=<your_key>`

___
### Run
`scrapy crawl google -o output.csv`
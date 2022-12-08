# URL Scraper

A python script to scrape URLs from major search engines. [Search dork](https://en.wikipedia.org/wiki/Google_hacking) is supported, dork multiple search engines at once.

![screenshot](https://user-images.githubusercontent.com/38415384/206352739-13188e02-e5ec-47e8-a94c-1ad61e331c66.png)

## Supported search engines

+ Google
+ Bing
+ Yahoo
+ DuckDuckGo

## Requirements

+ `Python 3.10`
+ `requests`
+ `beautifulsoup4`

## Usage

1. Clone the repository.
2. Install the dependencies & activate virtual environemnt.

    ```console
    $ pipenv install
    $ pipenv shell
    ```

3. Run the program.

    ```console
    $ python scraper.py
    ```

4. Follow the prompt.
5. Obtain results from the `output/` folder.

---

> **Note**: Program is intentionally slowed (humanized) to prevent being locked-out from search engines.

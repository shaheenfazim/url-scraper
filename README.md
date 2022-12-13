# URL Scraper

A python script to scrape URLs from major search engines. [Search dork](https://en.wikipedia.org/wiki/Google_hacking) is supported, dork multiple search engines at once.

![Screenshot 2022-12-13 171627](https://user-images.githubusercontent.com/21116180/207310027-12832f47-9e25-4ad5-89c1-e530adef92a1.png)

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

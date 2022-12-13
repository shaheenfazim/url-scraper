"""
█ █ █▀█ █
█▄█ █▀▄ █▄▄


█▀ █▀▀ █▀█ ▄▀█ █▀█ █▀█ █▀▀ █▀█
▄█ █▄▄ █▀▄ █▀█ █▀▀ █▀▀ ██▄ █▀▄

"""


# standard
import re
import sys
import time
import random
import datetime
from pathlib import Path
from dataclasses import dataclass
from urllib.parse import quote_plus

# external
import requests
from bs4 import BeautifulSoup


@dataclass(frozen=True, slots=True)
class TermColors:
    """
    Terminal colors
    """
    GREEN = '\033[92m'
    BOLD_GREEN = '\033[1;92m'
    RED = '\033[91m'
    BOLD_RED = '\033[1;91m'
    YELLOW = '\033[93m'
    BOLD_YELLOW = '\033[1;93m'
    BLUE = '\033[94m'
    BOLD_BLUE = '\033[1;94m'
    WHITE = '\033[97m'
    BOLD_WHITE = '\033[1;97m'
    END_C = '\033[0m'


def bing(stub: str) -> str:
    """
    URL resolver for bing
    """
    if not stub.startswith('http'):
        return f'https://www.bing.com{stub}'
    if stub.startswith('https://www.bing.com/ck/a?!&&p='):
        source = requests.get(url=stub, headers=header, timeout=30)
        if match := re.search(r'var u = "(.*?)";', source.text):
            return re.split(r'\?msclkid=|\&msclkid=', match[1])[0]
    return stub


def yahoo(stub: str) -> str:
    """
    URL resolver for yahoo
    """
    if stub.startswith('https://r.search.yahoo.com/_ylt='):
        source = requests.get(url=stub, headers=header, timeout=30)
        if match := re.search(r'window.location.replace\("(.*?)"\);', source.text):
            return match[1]
    return stub


def content_parser(
    choice: str, file_path: Path, soup: BeautifulSoup, base_url: str, query: str,
) -> str | None:
    """
    HTML content parser
    """
    parse_array_find: dict[str, tuple[str, dict[str, str]]] = {
        '1': ('a', {'id': 'pnnext'}),
        '2': ('a', {'class': 'sb_pagN'}),
        '3': ('a', {'class': 'next'}),
        '4': ('div', {'class': 'nav-link'})
    }

    parse_array_find_all: dict[str, tuple[str, dict[str, str]]] = {
        '1': ('div', {'class': 'yuRUbf'}),
        '2': ('h2', {}),
        '3': ('h3', {}),
        '4': ('h2', {}),
    }

    engine_specific = {
        '1': callable,  # stub for later use
        '2': bing,
        '3': yahoo,
        '4': callable,  # stub for later use
    }

    next_pg_elm = soup.find(*parse_array_find[choice])
    page_titles = soup.find_all(*parse_array_find_all[choice])

    for pg_t in page_titles:
        if not pg_t or not (anchor := pg_t.find('a', href=True)):
            continue
        if choice in '23':
            try:
                link = engine_specific[choice](anchor['href'])
            except requests.RequestException as exp:
                print(f'{TermColors.BOLD_YELLOW}\nW: {exp}{TermColors.END_C}')
                continue
        else:
            link = anchor['href']
        print(f'{TermColors.BLUE}{link}{TermColors.END_C}')
        with open(file=file_path, encoding='utf-8', mode='at') as out_f:
            out_f.write(f'{link}\n')

    if choice == '4':
        return f'{base_url}/search?q={query}&s=64&o=json'

    if not next_pg_elm or not (next_url := next_pg_elm.get('href')):
        print('END OF PAGE REACHED ')
        return None

    return f'{next_url}' if choice == '3' else f'{base_url}{next_url}'


def web_scraper(
    choice: str, file_path: Path, base_url: str, query: str, pg_count: int
) -> None:
    """
    Search enginge URL scraper
    """
    url, current_page = f'{base_url}/search?q={query}', 1

    while current_page <= pg_count:
        print(f'\nPAGE: {current_page}/{pg_count} [{url}]')

        try:
            # TODO: use better retry mechanism
            response = requests.get(url=url, headers=header, timeout=30)
        except requests.RequestException as exp:
            print(f'{TermColors.BOLD_YELLOW}\nW: {exp}{TermColors.END_C}')
            break

        if response.status_code != 200:
            print(f'{TermColors.BOLD_YELLOW}\nW: Site Unreachable{TermColors.END_C}')
            print(response.text)
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        if not (url := content_parser(choice, file_path, soup, base_url, query)):
            break

        current_page += 1
        if current_page <= pg_count:
            print(f'MOVING TO PAGE {current_page}')
            time.sleep(random.randint(5, 15))
        else:
            print('PAGE COUNT REACHED')


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
}


def asker() -> tuple[str, str, int]:
    """
    Ask user for input
    """
    # user choice
    u_choice = input(
        f'{TermColors.BOLD_GREEN}\n\t1: GOOGLE SEARCH\n'
        + '\t2: BING SEARCH \n\t3: YAHOO SEARCH\n'
        + f'\t4: DUCKDUCKGO\n\t5: RUN ALL{TermColors.END_C}\n'
        + f'\n{TermColors.BOLD_GREEN}[*]{TermColors.END_C} Choose engine (1-5): '
    )
    if u_choice not in '12345':
        raise ValueError('Bad choice! Select values from 1 - 5')

    # url encoded query
    u_query = quote_plus(
        input(f'{TermColors.BOLD_BLUE}[i]{TermColors.END_C} Enter query: ')
    )
    # print(f'Encoded query: {query}')

    # page count
    pg_count = int(
        input(
            f'{TermColors.BOLD_WHITE}[x]{TermColors.END_C} Enter page count: ')
    )
    if pg_count <= 0:
        raise ValueError('Page count must be >= 1')

    return (u_choice, u_query, pg_count)


def main():
    """
    Main function
    """
    engine_data = {
        '1': ('google.list', 'https://www.google.com'),
        '2': ('bing.list', 'https://www.bing.com'),
        '3': ('yahoo.list', 'https://search.yahoo.com'),
        '4': ('duckduckgo.list', 'https://duckduckgo.com/html'),
    }

    # create out_f folder
    op_dir = Path('output')
    op_dir.mkdir(parents=True, exist_ok=True)

    try:
        user_choice, user_query, page_count = asker()
    except ValueError as err:
        print(f'{TermColors.BOLD_RED}\nE: {err}{TermColors.END_C}')
        sys.exit(1)

    if user_choice == '5':
        for idx, engine in enumerate(engine_data.values()):
            url_list_file, base_url = engine
            print(
                f'{TermColors.BOLD_GREEN}\n{idx+1}: '
                + f'{url_list_file.rstrip(".list").upper()} SEARCH{TermColors.END_C}'
            )
            web_scraper(
                str(idx+1), op_dir / url_list_file,
                base_url, user_query, page_count
            )
        sys.exit(0)

    url_list_file, base_url = engine_data[user_choice]
    web_scraper(
        user_choice, op_dir / url_list_file,
        base_url, user_query, page_count
    )


if __name__ == '__main__':
    print(
        f'\n[{datetime.datetime.now()}]\n'
        + f'\n\t{TermColors.BOLD_GREEN}█ █ █▀█ █{TermColors.END_C}\n'
        + f'\t{TermColors.BOLD_BLUE}█▄█ █▀▄ █▄▄{TermColors.END_C}\n'
        + f'\n\n\t{TermColors.BOLD_GREEN}█▀ █▀▀ █▀█ ▄▀█ █▀█ █▀█ █▀▀ █▀█{TermColors.END_C}\n'
        + f'\t{TermColors.BOLD_BLUE}▄█ █▄▄ █▀▄ █▀█ █▀▀ █▀▀ ██▄ █▀▄{TermColors.END_C}\n'
    )
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\n{TermColors.BOLD_RED}Terminated by user{TermColors.END_C}')

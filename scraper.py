import re
import os
import time
import random
import requests
import datetime
import urllib.parse

from bs4 import BeautifulSoup

class bcolors:
   GREEN = '\033[92m'
   BGREEN = '\033[1;92m'
   RED = '\033[91m'
   BRED = '\033[1;91m'
   YELLOW = '\033[93m'
   BYELLOW = '\033[1;93m'
   BLUE = '\033[94m'
   BBLUE = '\033[1;94m'
   WHITE = '\033[97m'
   BWHITE = '\033[1;97m'
   ENDC = '\033[0m'

cloak = datetime.datetime.now()
print ("[%s]" % cloak)
print(f'\n\t{bcolors.BGREEN}█ █ █▀█ █{bcolors.ENDC}\n\t{bcolors.BBLUE}█▄█ █▀▄ █▄▄{bcolors.ENDC}\n')
print(f'\n\t{bcolors.BGREEN}█▀ █▀▀ █▀█ ▄▀█ █▀█ █▀█ █▀▀ █▀█{bcolors.ENDC}\n\t{bcolors.BBLUE}▄█ █▄▄ █▀▄ █▀█ █▀▀ █▀▀ ██▄ █▀▄{bcolors.ENDC}\n\t\t    - made with \033[5;91m💚{bcolors.ENDC} by fazim')

#CREATE OUTPUT FOLDER
if not os.path.exists('output'):
   os.mkdir('output')

#SAVE SCRAPED RESULTS
def save(link):
   with open('./output/%s' % listing, 'a') as output:
        output.write('%s\n' % link)
   output.close()

#BING URL SOLVER
def bing(link):
   if link.startswith("https://www.bing.com/ck/a?!&&p="):
        source = requests.get(link,headers=headers)
        head = 'var u = "'
        tail = '";'
        match = re.search(f'{head}(.*?){tail}', source.text)
        if match:
                check = match.group(1)
                link = re.split('\?msclkid=|\&msclkid=',check)[0]
                return link
        else:
                return link
   elif not link.startswith("http"):
        #SOLVE BING LOCAL URLS
        link = 'https://www.bing.com' + link
        return link

   else:
        return link

#YAHOO URL SOLVER
def yahoo(link):
   if link.startswith("https://r.search.yahoo.com/_ylt="):
        source = requests.get(link,headers=headers)
        head = 'window.location.replace\("'
        tail = '"\);'
        match = re.search(f'{head}(.*?){tail}', source.text)
        if match:
                link = match.group(1)
                return link
        else:
                return link
   else:
        return link

#SEARCH ENGINE URL SCRAPER
def scrape(choice,query,pages):
   url = f"{base}/search?q={query}"
   run = True
   count = 1

   while run == True:
        print(f"\nPAGE: {count}/{pages} [{url}]")

        #RETRY REQUESTS WHEN CONNECTION FAILS 
        while True:
                try:
                        response = requests.get(url,headers=headers)
                except:
                        #RETRY
                        continue
                break
        if response.status_code != 200:
                print(f'{bcolors.BRED}\nERROR: SITE UNREACHABLE{bcolors.ENDC}')
                print(response.text)
                break

        #🍲
        soup = BeautifulSoup(response.content,'html.parser')
                    
        if choice == '1':
                next = soup.find('a', {'id' : 'pnnext'})
                titles=soup.findAll('div', {'class' : 'yuRUbf'})
        elif choice == '2':
                next = soup.find('a', {'class' : 'sb_pagN'})
                titles=soup.findAll('h2')
        elif choice == '3':
                next = soup.find('a', {'class' : 'next'})
                titles=soup.findAll('h3')
        elif choice == '4':
                next = soup.find('div', {'class' : 'nav-link'})
                titles=soup.findAll('h2')
                pos = 14
        else:
                print(f"{bcolors.BRED}\nERROR: UNEXPECTED CHOICE ERROR{bcolors.ENDC}")  

        for i in titles:
                #USING TRY TO AVOID ERROR (TypeError: 'NoneType' object is not subscriptable)
                try:
                        a=i.find('a', href=True)
                        if choice == '2':link = bing(a['href'])
                        elif choice == '3':link = yahoo(a['href'])
                        else:link = a['href']
                        print(f"{bcolors.GREEN}%s{bcolors.ENDC}" % link)
                        save(link)
                except:
                        #SKIP
                        pass
                           
        if next is None:
                print("END OF PAGE REACHED")
                run = False
                break          
        else: 
                if choice == '4':
                        pos = pos + 50
                        url = f"{base}/search?q={query}&s={pos}&o=json" 
                        run = True
                else:
                        nexturl = next.get('href')
                        if nexturl is None:
                                print("END OF PAGE REACHED")
                                run = False
                                break 
                        else:
                                if choice == '3':url = nexturl    
                                else:url = f"{base}{nexturl}"
                                run = True
                        
        if count >= pages:
                print("PAGE COUNT REACHED")
                run = False
                break
        else:
                count = count + 1
                print(f'MOVING TO PAGE {count}')
                #SLEEP TO AVOID SEARCH ENGINE LOCK-OUT
                time.sleep(random.randint(5,15)) 


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}

choice = input(f"{bcolors.BGREEN}\n\t1: GOOGLE SEARCH\n\t2: BING SEARCH \n\t3: YAHOO SEARCH\n\t4: DUCKDUCKGO\n\t5: RUN ALL{bcolors.ENDC}\n\n{bcolors.BGREEN}[*]{bcolors.ENDC} Choose engine (1-5): ")

query = input(f"{bcolors.BBLUE}[i]{bcolors.ENDC} Enter query: ")
#URL ENCODE STRING
query = urllib.parse.quote_plus(query)
#print(f'Encoded query: {query}')


pages = input(f"{bcolors.BWHITE}[x]{bcolors.ENDC} Enter page count: ")
#CHECK IF INTEGER 
try:
   pages = int(pages)
except ValueError:
   print(f"{bcolors.BRED}\nERROR: INTEGER REQUIRED{bcolors.ENDC}")
   exit()

#MENU
if choice == '1':
   base = 'https://www.google.com'
   listing = 'google.list'
   scrape('1',query,pages)
elif choice == '2':
   base = 'https://www.bing.com'
   listing = 'bing.list'
   scrape('2',query,pages)
elif choice == '3':
   base = 'https://search.yahoo.com'
   listing = 'yahoo.list'
   scrape('3',query,pages)
elif choice == '4':
   base = 'https://duckduckgo.com/html'
   listing = 'duckduckgo.list'
   scrape('4',query,pages)
elif choice == '5':
   print(f"{bcolors.BGREEN}\n1: GOOGLE SEARCH{bcolors.ENDC}")
   base = 'https://www.google.com'
   listing = 'google.list'
   scrape('1',query,pages)
   print(f"{bcolors.BGREEN}\n2: BING SEARCH{bcolors.ENDC}")
   base = 'https://www.bing.com'
   listing = 'bing.list'
   scrape('2',query,pages)
   print(f"{bcolors.BGREEN}\n3: YAHOO SEARCH{bcolors.ENDC}")
   base = 'https://search.yahoo.com'
   listing = 'yahoo.list'
   scrape('3',query,pages)   
   print(f"{bcolors.BGREEN}\n3: DUCKDUCKGO{bcolors.ENDC}")
   base = 'https://duckduckgo.com/html'
   listing = 'duckduckgo.list'
   scrape('4',query,pages)
else:
   print(f"{bcolors.BRED}\nERROR: INVALID CHOICE{bcolors.ENDC}")
   exit()

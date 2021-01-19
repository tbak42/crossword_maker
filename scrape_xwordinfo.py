import urllib.request
from bs4 import BeautifulSoup

with urllib.request.urlopen('https://www.xwordinfo.com/AllTimePops?length=8') as response:
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    words_by_count = {}

    for c in soup.find_all('td', class_='count'):
        print("$$$$$$$$$$$")
        count = int(c.text.strip())
        words_by_count[count] = []
        p = c.parent
        for a in p.find_all('a', href=True):
            #print(a)
            #print(a['href'])
            if a['href'].find('/Finder?word') != -1:
                #print('good!')
                #print(a.text.strip())
                words_by_count[count].append(a.text.strip())
    print(words_by_count)

    """
    for a in soup.find_all('a', href=True):
        print(a)
        print(a['href'])
        if a['href'].find('/Finder?word') != -1:
            print('good!')
            print(a.text.strip())
    """

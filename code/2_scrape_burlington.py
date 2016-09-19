# example with Burlington news - data all on multiple pages
# strictly need to reload pages

import requests
from bs4 import BeautifulSoup
import urlparse
import unicodecsv
import time

# Item is <div class="newsItem">...</div>
def parse(item, base_url):
    # Q: Does it get the first <a> tag?
    # First one: "Healthy Kids Community Challenge Burlington wants your ideas"
    title = item.a.text.strip()

    # Gets the href element
    url = urlparse.urljoin(base_url, item.a['href'])

    # i.e. "Posted Thursday, September 15, 2016"
    date = item.select('.newsItem_PostedDate')[0].text
    # i.e. "Thursday, September 15, 2016"
    date = date.replace('Posted ', '').strip()
    return (title, date, url)


urlformat = 'https://www.burlington.ca/en/Modules/News/search.aspx?feedId=\0b11ae3a-b049-4262-8ca4-762062555538&page=%s'

htmlpages = []
page = 1
sleeplvl = 5
while page <= 5:
    # --> 'https://www.burlington.ca/en/Modules/News/search.aspx?feedId=\0b11ae3a-b049-4262-8ca4-762062555538&page={{{{{%1}}}}}'
    url = urlformat % page
    print 'requesting url: %s' % url

    # Get the page based on request library
    request = requests.get(url)

    # Pushes the inner array to the htmlpages array
    htmlpages.append(request.text)

    # Increment page number
    page = page + 1
    print 'sleeping for %s seconds' % sleeplvl
    # To avoid getting blocked
    time.sleep(sleeplvl)


results = []
for html in htmlpages:
    print 'parsing results...'
    # BS-processed soup
    soup = BeautifulSoup(html)

    # Array of .newsItem elements in an array
    soupitems = soup.select('.newsItem')

    # For each <div class="newsItem">, appyl parse
    parsedresults = [parse(row, url) for row in soupitems]
    print 'extracted %s results' % len(parsedresults)
    #  Concats to the results array
    results.extend(parsedresults)

print 'completed parsing with %s results' % len(results)

fname = 'burlington_news.csv'
print 'writine results to file: %s' % fname
with open(fname, 'wb') as csvfile:
    csvwriter = unicodecsv.writer(csvfile, encoding='utf-8',
                                  delimiter=',', quotechar='"')
    csvwriter.writerow(('title', 'date', 'url'))
    csvwriter.writerows(results)

print 'writing results complete'

# example with Mississauga news - single html page with all results

# requests the page
import requests

# BS: the HTML parser
from bs4 import BeautifulSoup

# for urljoin
import urlparse

# creates csv
import unicodecsv


def parse(row, base_url):
    # assign 1st entry in td to _
    # assign 2nd entry in td to item -> keeping this
    _, item = row.select('td')
    # _ is:
    # <td>
    #   <img src="/ecity/images/bullet_.png" alt="" />&nbsp;&nbsp;
    # </td>

    # item is:
    # <td>
    #   <a href="/portal/cityhall/pressreleases?paf_gear_id=9700020&itemId=6300734q&backUrl=%2Fportal%2Fcityhall%2Fpressreleases%3Fpaf_gear_id%3D9700020">34th Mississauga Urban Design Awards Celebrate Design Excellence</a>
    #   <br/>
    #   Sep 15, 2016
    #   <br/>
    #   <br/>
    # </td>

    # gets href text from <a href>
    link = item.a.extract()
    # gets date from <a href> link
    date = item.text.strip()

    # gets text from the link
    title = link.text.strip()

    # base url for page + link object href attribute
    url = urlparse.urljoin(base_url, link['href'])

    return (title, date, url)

url = 'http://www.mississauga.ca/portal/cityhall/pressreleases?paf_gear_id=\9700020&returnUrl=%2Fportal%2Fcityhall%2Fpressreleases'

print 'requesting url: %s' % url
request = requests.get(url)
# TODO: validation that request came back successfully
html = request.text

print 'parsing results...'

# Downloads HTML in memory
soup = BeautifulSoup(html)
# Selects $(".blockcontentclear tr") array of elements
souprows = soup.select(".blockcontentclear tr")


# returns result of parsing each element in souprows
results = [parse(row, url) for row in souprows]
print 'completed parsing with %s results' % len(results)



fname = 'misssissauga_news.csv'

print 'writine results to file: %s' % fname

# What does with open() do?
with open(fname, 'wb') as csvfile:
    # create csv
    csvwriter = unicodecsv.writer(csvfile, encoding='utf-8', delimiter=',', quotechar='"')
    csvwriter.writerow(('title', 'date', 'url'))
    csvwriter.writerows(results)

print 'writing results complete'

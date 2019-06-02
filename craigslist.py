# Imports
import urllib2
from bs4 import BeautifulSoup
from notify_run import Notify
import time

# Setup
notify = Notify()

while True:
    print('checking for new ads...')

    # Making soup
    search_url = 'https://vancouver.craigslist.org/search/cta?hasPic=1&bundleDuplicates=1&searchNearby=2&nearbyArea=621&nearbyArea=473&nearbyArea=471&nearbyArea=381&nearbyArea=380&nearbyArea=382&nearbyArea=622&nearbyArea=177&nearbyArea=472&min_price=1000&max_price=10000&auto_make_model=toyota&min_auto_year=1995&max_auto_miles=275000&auto_bodytype=7&auto_bodytype=9'
    search_page = urllib2.urlopen(search_url)
    search_soup = BeautifulSoup(search_page, 'html.parser')

    # Initializing array for ad links and names
    #   each element of ads is a 2-element array containing a matching href and title
    ads = []

    # Loop to populate ads array
    for a_att in search_soup.find_all('a', attrs={'class': 'result-title hdrlnk'}):
        href = a_att.get('href')
        title = a_att.text
        ad_element = [href, title]
        ads.append(ad_element)

    # Print all ads and links
    # print(datetime.datetime.now())
    # for ad in ads:
    #    for s in ad:
    #        print(s)
    #    print()

    # Make an array where each element is a line from existing_ads.txt
    f = open("existing_ads.txt", "r")
    existing_ads = []
    for line in f:
        line_no_nl = line[:-1]
        existing_ads.append(line_no_nl)

    f.close()
    f = open("existing_ads.txt", "a")

    # Find items that are in ads but not existing_ads
    for ad in ads:
        if ad[0] not in existing_ads:
            print(ad[0])
            # Send notification about new ad
            s = 'new Craigslist ad: ' + ad[0] + '  ' + ad[1]
            print(s)
            notify.send(s)

            # Add new ad to existing_ads.txt
            f.write(ad[0]+'\n')

    f.close()

    print('waiting 10 mins ...')
    # Loop every hour
    time.sleep(600)


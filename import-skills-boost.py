from urllib import request
from bs4 import BeautifulSoup
import re

with request.urlopen('https://bit.ly/gcp-bab501a') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    badges = soup.find('div', attrs={'class': 'profile-badges'})

    badge_data = dict()
    
    for badgeEl in badges:
        badge = badgeEl.findNext('span')
        badgeName = badge.text.strip('\r\n')
        badgeName = re.sub("\s\s+" , " ", badgeName)

        if badgeName != '':
            completion = badge.find_next_sibling().text.strip('\r\n')
            completion = re.sub("\s\s+" , " ", completion)

            badge_data[badgeName] = completion

    print(len(badge_data))
    print(badge_data)
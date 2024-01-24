from sys import argv
from bs4 import BeautifulSoup
import re
from urllib import request

try:
    with request.urlopen('https://bit.ly/gcp-bab501a') as f:
        contents = f.read()

        soup = BeautifulSoup(contents, 'html.parser')

        badges = soup.find('div', attrs={'class': 'profile-badges'})

        badge_data = dict()
        
        for badgeEl in badges:
            badge = badgeEl.findNext('span')
            badgeName = badge.text.strip('\r\n')
            badgeName = re.sub('\s\s+' , ' ', badgeName)

            if badgeName != '':
                completion = badge.find_next_sibling().text.strip('\r\n')
                completion = re.sub('\s\s+' , ' ', completion)

                # Add styling to badge thumbnail
                thumbnail = badgeEl.findNext('a')
                thumbnail.find('img').attrs['style'] = 'max-width: 10rem;'

                badge_data[badgeName] = [thumbnail, completion]

        print('{} badge(s) found.'.format(len(badge_data)))

        if len(argv) == 1:
            limit = 3
            print('Limit has been set to default of {}.'.format(limit))
        else:
            limit = int(argv[1])

        print('Up to {} badge(s) will be printed.\n'.format(limit))

        generate_readme_text(badge_data, limit)

except Exception as e:
    print("An error occurred: ", e)
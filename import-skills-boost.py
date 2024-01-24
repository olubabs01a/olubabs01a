from sys import argv
from bs4 import BeautifulSoup
import re
from urllib import request

def generate_readme_text(badges: dict, limit = 3):
    updates = '<!-- start latest badges -->\n';

    if len(badges) < limit or limit <= 0:
        limit = len(badges)

    count = 1
    for badgeKey in badges.keys():
        completion = badges[badgeKey][1]
        row = '- ' + completion + '\n'
        row += '{}'.format(badges[badgeKey][0])

        print('Badge #{} found => {}, {}\n'.format(count, badgeKey, completion))

        updates += row;
        count += 1
        
        if count > limit:
            break

    updates += '<!-- end latest badges -->';

    # Rewrite README with new post content
    fileName = 'README.md'
    currentText = open(fileName, mode='r', encoding='utf8').read();

    badgePattern = r'<!-- start latest badges -->\S*\s*<!-- end latest badges -->'
    matches = re.search(badgePattern, currentText)

    if matches:
        newText = re.compile(badgePattern).sub(updates, currentText)

        try:
            with open('README.md', mode='w', encoding='utf8') as f:
                f.write(newText)
                f.close()
        except:
            # Restore original content on failure
            with open('README.md', mode='w', encoding='utf8') as f:
                f.write(currentText)
                f.close()
            raise

    else:
        raise Exception('Badge destination pattern not found in {}'.format(fileName))

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
                thumbnail.find('img').attrs['style'] = ['max-width: 10rem;']

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
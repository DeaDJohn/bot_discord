import re
import json
import requests
from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup
from socket import timeout

fifa = {
    #'15': 'FIFA15',
    #'16': 'FIFA16',
    #'17': 'FIFA17',
    #'18': 'FIFA18',
    #'19': 'FIFA19',
    '23': 'FIFA23'
}

cardColumns = ['ID', 'Name', 'Rating', 'Price', 'SkillsMoves', 'WeakFoot',
               'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
               'Phyiscality', 'Popularity', 'BaseStats', 'InGameStats',
               'Revision', 'Position', 'WorkRate', 'Height', 'Club',
               'Country', 'League', 'NationPic', 'ClubPic', 'PlayerPic']

detailedColumns = ['ID', 'Acceleration', 'Added on', 'Age', 'Aggression',
                   'Agility', 'Att. WR', 'Balance', 'Ball Control', 'Club',
                   'Composure', 'Crossing', 'Curve', 'Def. WR', 'Defending',
                   'Diving', 'Dribbling', 'FK. Accuracy', 'Finishing', 'Foot',
                   'Fullname', 'Handling', 'Heading Accuracy', 'Height', 'Interceptions',
                   'Intl. Rep', 'Jumping', 'Kicking', 'League', 'Long Passing',
                   'Long Shots', 'Marking', 'Nation', 'Origin', 'Pace', 'Passing',
                   'Penalties', 'Physicality', 'Positioning', 'R.Face', 'Reactions',
                   'Reflexes', 'Revision', 'Shooting', 'Short Passing', 'Shot Power',
                   'Skills', 'Sliding Tackle', 'Sprint Speed', 'Stamina', 'Standing Tackle',
                   'Strength', 'Vision', 'Volleys', 'Weak Foot', 'Weight']

C = open('FutBinCards'+ fifa.key +'.csv', 'w')
C.write(','.join(cardColumns) + '\n')
D = open('FutBinDetailed'+ fifa.key +'.csv', 'w')
D.write(','.join(detailedColumns) + '\n')
C.close()
D.close()

for key, value in fifa.items():
    id = 0
    ID = 0
    print('Doing ' + value)
    req = Request('https://www.futbin.com/' + key + '/players' , headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imageapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Dnt": "1","Host": "httpbin.org","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",})

    webpage = urlopen(req , timeout=10000).read()
    #FutBin = requests.get(webpage, headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imageapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9″,"Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Dnt": "1","Host": "httpbin.org","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",})
    bs = BeautifulSoup(webpage, 'html.parser')
    print( bs.findAll('li', {'class': 'page-item'}) )
    try:
        TotalPages = str(bs.findAll('li', {'class': 'page-item '})[-1].text).strip()
    except IndexError:
        TotalPages = str(bs.findAll('li', {'class': 'page-item'})[-2].text).strip()
    print('Number of pages to be parsed for FIFA ' + key + ' is ' + TotalPages + ' Pages')
    for page in range(1, int(TotalPages) + 1):
        url = 'https://www.futbin.com/' + key + '/players?page=' + str(page)
        req = Request(url , headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imageapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Dnt": "1","Host": "httpbin.org","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",})

        webpage = urlopen(req , timeout=10000).read()
        #FutBin = requests.get('https://www.futbin.com/' + key + '/players?page=' + str(page), headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imageapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "Dnt": "1","Host": "httpbin.org","Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
        bs = BeautifulSoup(webpage, 'html.parser')
        table = (bs.find('table', {'id': 'repTb'}))
        tbody = table.find('tbody')
        extracted = tbody.findAll('tr', {'class': re.compile('player_tr_\d+')})
        Card = []
        for cardDetails in extracted:
            teamLeague = [i['data-original-title'] for i in cardDetails.findAll('a', {'href': re.compile('^/19/players\?page=')})]
            name = str(cardDetails.text).strip().replace('\n', ' ').split('           ')[0]
            cardDetails = str(cardDetails.text).strip().replace('\n', ' ').replace(' \\ ', '\\').replace(' | ', '|').split('       ')[1]
            workRate = re.search('\w\\\\\w', cardDetails, re.IGNORECASE).group(0) if re.search('\w\\\\\w', cardDetails, re.IGNORECASE) else None
            cardDetails = re.sub("\w\\\\\w", "", cardDetails)
            match_Height = re.search("\w+\|\d\'\d+\"", cardDetails, re.IGNORECASE).group(0)
            cardDetails = re.sub("\w+\|\d\'\d+\"", "", cardDetails)
            body = [re.findall("\s(\D*\s\D+)", cardDetails, re.IGNORECASE)[1].split()[0]]
            revision = re.findall("\s(\D*\s\D+)", cardDetails, re.IGNORECASE)[1].split()[1:]
            cardDetails = re.sub("\s\D*\s\D+", " ", cardDetails)
            cardDetails = cardDetails.split()
            cardDetails.insert(0, name)
            cardDetails.insert(0, id)
            body.extend([workRate, match_Height])
            cardDetails.extend([' '.join(revision)])
            cardDetails.extend(body)
            cardDetails.extend(teamLeague)
            Card.append(cardDetails)
            print(cardDetails)
            id += 1
        webpages = ['https://www.futbin.com' + str(i['data-url']).replace(' ', '%20') for i in extracted]
        overall = {}
        for webpage in webpages:
            d = {}
            json_data = ''
            req = Request(url , headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imageapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Dnt": "1","Host": "httpbin.org","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",})
            print(url)
            profile = urlopen(req , timeout=1000000).read()
            bs = BeautifulSoup(profile, 'html.parser')
            #profile = requests.get(webpage, headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imageapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Dnt": "1","Host": "httpbin.org","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",})
            #bs = BeautifulSoup(profile.text, 'html.parser')
            images = [i['src'] for i in bs.findAll('img', id=re.compile('player_nation|player_club|player_pic'))[0:3]]
            Card[webpages.index(webpage)].extend(images)
            info = bs.find('div', {'id': 'info_content'})
            print(info)
            if (info):
                d.update(dict(zip([str(i.text).replace('Name', 'Fullname').strip() for i in info.findAll('th')], [str(i.text).strip() for i in info.findAll('td')])))
                detailedStats = bs.findAll('div', {'class': 'col-md-4 col-lg-4 col-6'})
                for i in detailedStats:
                    d.update(dict(zip(([j.text for j in i.findAll('span', 'ig-stat-name-tooltip')]), [str(j.text).strip() for j in i.findAll('div', 'stat_val')])))
                overall[ID] = d
                json_data += json.dumps(overall, indent=4, separators=(',', ': '), sort_keys=True)
            ID += 1
        df = pd.DataFrame(Card)
        print(df)
        df.to_csv('FutBinCards19.csv', mode='a', header=False, sep=',', encoding='utf-8', index=False)
        pd.read_json(json_data).transpose().to_csv('FutBinDetailed19.csv', mode='a', header=False, sep=',', encoding='utf-8', index=True)
import re
import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint

def get_data_from_indeed(work, location="Paris", end_date=0, start=0):
    res = []
    if start == 0:
        resp = urllib.request.urlopen(
                "http://www.indeed.fr/emplois?q=%s&l=%s&sort=date"
                % (work, location)
        )
    else:
        resp = urllib.request.urlopen(
                "http://www.indeed.fr/emplois?q=%s&l=%s&sort=date&&start=%d"
                % (work, location, start)
        )
    max_date = 0
    soup = BeautifulSoup(resp, 'html.parser')
    for job in soup.find_all('div', attrs={'class': ' row result'}):
        sponsor = False
        title = job.find("h2", attrs={'class': 'jobtitle'}).a.text
        #print(title)
        link = job.find_all('a',
                attrs={'class': 'turnstileLink'})[0]['href']
        #print("\tLink: www.indeed.com%s" % link)

        company = job.find_all('span', attrs={'class': 'company'})
        if company is not None and company != []:
            company = company[0].text.strip()
        else:
            company = None
        #print("\tCompany: %s" % company)

        location = job.find_all('span', attrs={'class': 'location'})
        if location is not None and location != []:
            location = location[0].text.strip()
        else:
            location = None
        #print("\tlocation: %s" % location)

        date_str = job.find_all('span',
                attrs={'class': 'date'})[0].text.strip()
        if date_str == "Aujourd'hui" or date_str == "Publiée à l'instant":
            date = 0
        elif re.search('il y a \d heures?', date_str):
            date = 0
        else: 
            date = int(re.findall('il y a (\d+)\+? jours?', date_str)[0])
        #print("\tdate: %s" % date)
        if date == 30:
            continue
        if date <= max_date:
            res.append((title, company, location, date, link))
        max_date = max(max_date, date)

    if max_date < end_date:
        res += get_data_from_indeed(work, location, end_date, start+10)

    return res


if __name__ == "__main__":
    data = get_data_from_indeed("Cybersecurite", "Paris", end_date=5)
    pprint(data)

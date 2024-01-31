import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint

headers = Headers(os='win', browser='Chrome')

url = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers.generate())
url_text = url.text


soup = BeautifulSoup(url_text, 'lxml')
tags = soup.find(id="a11y-main-content")
divs_tag = tags.find_all('div', class_="serp-item")

list_all = []

for div_tag in divs_tag:
    link_tag = div_tag.find('a', class_="bloko-link")
    absolutely_link = link_tag['href']

    url1 = requests.get(absolutely_link, headers=headers.generate())
    url_text1 = url1.text
    soup1 = BeautifulSoup(url_text1, 'lxml')

    content_tags = soup1.find('div', class_="g-user-content").text.strip()
    if 'Django'.lower() in content_tags.lower() or 'Flask'.lower() in content_tags.lower():
        salary_tag = soup1.find('div', class_="vacancy-title")
        salary_text = salary_tag.find('span')


        if salary_text is None:
            salary = 'З/п неуказана'
        else:
            salary = salary_text.text
            salary = salary.replace('\xa0', ' ')


        company_tags = soup1.find('span', class_="vacancy-company-name")
        company_tag = company_tags.find('span')
        company_text = company_tag.text

        city_tags = soup1.find('div', class_="bloko-columns-row")
        city_tag = city_tags.find('p', class_="vacancy-creation-time-redesigned").text
        city_tag = city_tag.replace('\xa0', ' ')


        list_all.append({
            'link': absolutely_link,
            'salary': salary,
            'company': company_text,
            'city': city_tag
        })

pprint(list_all)

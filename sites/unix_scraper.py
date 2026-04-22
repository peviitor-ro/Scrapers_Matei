# Company ---> unix
# Link ------> https://www.unixauto.ro/cariera/cautator

import re

import requests
from bs4 import BeautifulSoup

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)


def extract_city(text):

    city_name = text.split(',', 1)[0].strip()

    city_map = {
        'Cluj Napoca': 'Cluj-Napoca',
        'Târgu Mureș': 'Targu-Mures',
        'Targu Mures': 'Targu-Mures',
        'Bucuresti 6.': 'Bucuresti',
        'Bucuresti 3.': 'Bucuresti',
        'Bucuresti 4.': 'Bucuresti',
    }

    city_name = re.sub(r'\s+', ' ', city_name)

    return city_map.get(city_name, city_name)


def scraper():
    response = requests.get('https://www.unixauto.ro/cariera/cautator', verify=False, timeout=30)
    soup = BeautifulSoup(response.text, 'lxml')
    job_list = []

    for job in soup.select('section.karrierjobs a.karrierjob'):
        title = job.select_one('h3.karrierjob__h3')
        location_tag = job.select_one('.karrierjob__cimek p.karrierjob__p:not(.karrierjob__p-show-more)')

        if not title or not location_tag:
            continue

        location_text = location_tag.get('title') or location_tag.get_text(strip=True)
        city_name = extract_city(location_text)

        job_list.append(Item(
            job_title=title.get_text(strip=True),
            job_link='https://www.unixauto.ro' + str(job.get('href')),
            company='Unix',
            country='Romania',
            county=get_county(city_name),
            city=city_name,
            remote='on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "Unix"
    logo_link = "https://www.unixauto.ro/assets/images/UNIX_RO.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

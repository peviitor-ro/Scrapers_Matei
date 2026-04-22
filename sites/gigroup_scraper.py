# Company ---> GiGroup
# Link ------> https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca
import requests
from bs4 import BeautifulSoup
from __utils import (
    get_county,
    Item,
    UpdateAPI,
)


def _normalize_city(title: str, city: str) -> str:

    if '-' in city:
        city = city.split('-')[0].strip()

    if city == 'Cluj':
        city = 'Cluj-Napoca'

    if title == 'Director Sucursala':
        return 'Targu-Mures'

    if title in ('Tehnician de calitate', 'Operator turnatorie'):
        return 'Pitești'

    return city


def scraper():

    # scrape data from GiGroup scraper.
    response = requests.get('https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca/', timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    # list with data
    job_list = []

    for job in soup.select('article.workRow'):
        title_block = job.select_one('div.titleBlock a')
        if not title_block:
            continue

        title = title_block.get_text(strip=True)
        location_nodes = job.select('div.span8 div.workCol2 h3')

        if len(location_nodes) < 2:
            continue

        location_text = location_nodes[1].get_text(strip=True).split(',')[0].strip()
        location_clear = _normalize_city(title, location_text)

        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = title_block.get('href'),
            company = 'GiGroup',
            country = 'Romania',
            county = get_county(location_clear),
            city = location_clear,
            remote = 'on-site',
        ).to_dict())


    return job_list


def main():

    company_name = "GiGroup"
    logo_link = "https://w5b2c9z3.rocketcdn.me/wp-content/themes/gi-group/images/gi-group-child-logo@2x.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()

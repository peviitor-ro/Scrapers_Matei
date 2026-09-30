# Company ---> GiGroup
# Link ------> https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca
from urllib.parse import urljoin

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)

BASE_URL = 'https://ro.gigroup.com'
JOBS_LINK = f'{BASE_URL}/oferta-noastra-de-locuri-de-munca/'


def _clean_city(city: str) -> str:

    city = ' '.join(city.split())

    # location is built like "Bucuresti - Sectorul 6" -> keep only the city
    if ' - ' in city:
        city = city.split(' - ')[0].strip()

    if city == 'Cluj':
        city = 'Cluj-Napoca'

    return city


def _get_location(job) -> str:

    for row in job.select('div.job-item-meta-row'):

        if row.select_one('span.bi-geo-alt'):
            return ' '.join(row.get_text(' ', strip=True).split())

    return ''


def _get_city_and_county(location: str):

    # location is built like "Darasti-Ilfov, Ilfov, Bucuresti - Ilfov"
    parts = [part.strip() for part in location.split(',') if part.strip()]

    if not parts:
        return '', None

    city = _clean_city(parts[0])

    for candidate in (city, *(_clean_city(part) for part in parts[1:])):
        county = get_county(candidate)

        if county:
            return candidate, county

    return city, None


def scraper():

    # scrape data from GiGroup scraper.
    soup = GetStaticSoup(JOBS_LINK)

    # list with data
    job_list = []

    for job in soup.select('article.ggp-job-item'):

        title_link = job.select_one('div.ggp-job-title-wrapper a.ggp-job-title-url')

        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        link = title_link.get('href')

        if not link:
            continue

        city, county = _get_city_and_county(_get_location(job))

        if not city:
            continue

        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = urljoin(BASE_URL, link),
            company = 'GiGroup',
            country = 'Romania',
            county = county,
            city = city,
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

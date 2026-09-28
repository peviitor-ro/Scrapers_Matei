# Company ---> Auto1 Group
# Link ------> https://www.auto1-group.com/en/jobs/?country=Romania

import requests

from __utils import (
    Item,
    UpdateAPI,
    get_county,
)

SEARCH_API = 'https://www.auto1-group.com/smart-recruiters/jobs/search/'
JOBS_PAGE = 'https://www.auto1-group.com/en/jobs/'
RESULTS_PER_PAGE = 50
MAX_PAGES = 20


def _search_jobs(page):

    response = requests.post(
        SEARCH_API,
        json={
            'filters': {'country': 'Romania'},
            'options': {'currentPage': page, 'resultsPerPage': RESULTS_PER_PAGE},
        },
        headers={'Content-Type': 'application/json'},
    )

    if response.status_code != 200:
        return [], 0

    jobs = response.json().get('jobs', {})

    return jobs.get('hits', []), jobs.get('total', {}).get('value', 0)


def _normalize_city(job_source):

    town = job_source.get('translatedCity') or job_source.get('locationCity') or ''

    if town in ('Bucharest', 'București'):
        return 'Bucuresti'

    return town


def scraper():

    # scrape data from Auto1 Group scraper.

    job_list = []
    page = 1

    while page <= MAX_PAGES:
        jobs, total = _search_jobs(page)

        if not jobs:
            break

        for job in jobs:
            source = job.get('_source', {})
            town = _normalize_city(source)

            # get jobs items from response
            job_list.append(Item(
                job_title = source.get('title', ''),
                job_link = f'{JOBS_PAGE}{source.get("url", "")}',
                company = 'auto1',
                country = 'Romania',
                county = get_county(town),
                city = town,
                remote = 'remote' if source.get('remote') else 'on-site',
            ).to_dict())

        if len(job_list) >= total:
            break

        page = page + 1

    return job_list


def main():

    company_name = "auto1"
    logo_link = "https://www.auto1-group.com/images/logo-auto1-group-v4.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

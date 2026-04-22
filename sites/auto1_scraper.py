# Company ---> Auto1 Group
# Link ------> https://www.auto1-group.com/en/jobs/?country=Romania

import json
from html import unescape

from __utils import (
    GetRequestJson,
    GetStaticSoup,
    Item,
    UpdateAPI,
    get_county,
)


def _extract_jobs(json_data):

    jobs_data = json_data.get('jobs', {})
    hits = jobs_data.get('hits', [])

    if isinstance(hits, dict):
        return hits.get('hits', [])

    return hits


def _get_jobs_from_page():

    soup = GetStaticSoup('https://www.auto1-group.com/en/jobs/?country=Romania')
    jobs_node = soup.select_one('#smart-recruiters-job-data')

    if not jobs_node:
        return []

    jobs_json = jobs_node.get('data-initial-jobs', '')
    if not jobs_json:
        return []

    json_data = json.loads(unescape(jobs_json))

    return [
        job for job in _extract_jobs(json_data)
        if job.get('_source', {}).get('locationCountry') == 'Romania'
    ]


def _normalize_city(job_source):

    town = job_source.get('translatedCity') or job_source.get('locationCity') or ''

    if town in ('Bucharest', 'București'):
        return 'Bucuresti'

    return town


def scraper():
    # scrape data from Auto1 Group scraper.

    page = 1
    job_list = []

    while True:

        json_data = GetRequestJson(f"https://www.auto1-group.com/smart-recruiters/jobs/search/?page={page}&country=Romania")

        if not isinstance(json_data, dict):
            jobs = _get_jobs_from_page()
        else:
            jobs = _extract_jobs(json_data)

        if not jobs:
            break

        for job in jobs:
            source = job.get('_source', {})
            town = _normalize_city(source)

            # get jobs items from response
            job_list.append(Item(
                job_title = source['title'],
                job_link = f'https://www.auto1-group.com/en/jobs/{source["url"]}',
                company = 'auto1',
                country = 'Romania',
                county = get_county(town),
                city = town,
                remote = 'remote' if source.get('remote') else 'on-site',
            ).to_dict())

        if not isinstance(json_data, dict):
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

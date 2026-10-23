# Company ---> Intelactsoft
# Link ------> https://careers.smartrecruiters.com/Intelligence1

from __utils import (
    DEFAULT_HEADERS,
    Item,
    UpdateAPI,
    get_county,
)

import re

import requests


def scraper():

    # scrape data from intelactsoft scraper.

    job_list = []

    response = requests.get(
        "https://api.smartrecruiters.com/v1/companies/Intelligence1/postings",
        headers=DEFAULT_HEADERS,
        timeout=30,
    )

    # The company website no longer has a careers page. Its open positions are
    # published on SmartRecruiters instead.
    if response.status_code != 200:
        return job_list

    for job in response.json().get('content', []):

        title = job.get('name', '').strip()
        if not title:
            continue

        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = f"https://jobs.smartrecruiters.com/Intelligence1/{job['id']}-{slug}",
            company = 'Intelactsoft',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "Intelactsoft"
    logo_link = "https://intelactsoft.com/assets/intelactsoft_complet_alb-SqG6odA0.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

# Company ---> Intelactsoft
# Link ------> https://www.intelactsoft.com/jobs/

from __utils import (
    DEFAULT_HEADERS,
    Item,
    UpdateAPI,
    get_county,
)

import requests
from bs4 import BeautifulSoup


def scraper():

    # scrape data from intelactsoft scraper.

    job_list = []

    response = requests.get(
        "https://www.intelactsoft.com/jobs/",
        headers=DEFAULT_HEADERS,
        timeout=30,
    )

    # The website was rebuilt and the careers section was dropped, so the
    # old /jobs/ page now answers 404 and no longer lists any position.
    if response.status_code != 200:
        return job_list

    soup = BeautifulSoup(response.text, 'lxml')

    for job in soup.find_all('div', attrs = {'class': 'mt-5 col-xl-4 col-lg-6 link'}):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').text,
            job_link = 'https://www.intelactsoft.com' + job.find('div', attrs = {'class': 'job'}).find('a')['href'],
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

#
# Company ---> maxbet
# Link ------> https://maxbetgroup.ro/joburi

import urllib3
import requests
from bs4 import BeautifulSoup
from __utils import (
    get_county,
    Item,
    UpdateAPI,
)
from __utils.default_headers import DEFAULT_HEADERS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scraper():

    # scrape data from maxbet scraper.

    response = requests.get("https://maxbetgroup.ro/joburi", headers=DEFAULT_HEADERS, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    job_list = []
    
    for job in soup.find_all('div', class_ = 'col-xl-6 col-lg-6 col-md-6 mb-3'):

        oras = str(job.find('div', class_ = 'location').text.strip())
        if oras == 'Piatra Neamț':
            oras = 'Piatra-Neamt'
        if oras == 'Târgu Mureș':
            oras = 'Targu-Mures'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', class_ = 'job-name').text.strip(),
            job_link = job.find('a')['href'],
            company = 'MaxBet',
            country = 'Romania',
            county = get_county(oras),
            city = oras,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "MaxBet"
    logo_link = "https://maxbetgroup.ro/assets/app/images/maxbet-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

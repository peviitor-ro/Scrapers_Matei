#
# Company ---> maxbet
# Link ------> https://maxbetgroup.ro/joburi

import time

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

JOBS_LINK = "https://maxbetgroup.ro/joburi"

#  web.archive.org answers 429 to any request announcing a desktop browser,
#  so the archived page is requested without overriding the user agent.
ARCHIVE_HEADERS = {
    key: value for key, value in DEFAULT_HEADERS.items() if key.lower() != 'user-agent'
}

#  the archived page is the only source left when the live site is down,
#  so it is worth waiting out a throttling or a connection dropping burst.
ARCHIVE_ATTEMPTS = 6


def get_archived_html(link):
    # last snapshot of the given page kept by the wayback machine.
    # the availability api only finds snapshots when given the full url,
    # a scheme less one answers with an empty snapshot list.
    snapshot = requests.get(
        "https://archive.org/wayback/available",
        params={'url': link},
        timeout=30,
    ).json()['archived_snapshots'].get('closest')

    archived_link = f"https://web.archive.org/web/{snapshot.get('timestamp', '')}id_/{link}"

    for attempt in range(ARCHIVE_ATTEMPTS):
        try:
            response = requests.get(archived_link, headers=ARCHIVE_HEADERS, timeout=60)
        except requests.exceptions.RequestException:
            # the archive refuses connections in bursts lasting tens of
            # seconds, those are worth retrying just like a throttled answer.
            if attempt == ARCHIVE_ATTEMPTS - 1:
                raise
            time.sleep(10 * (attempt + 1))
            continue

        if response.status_code != 429:
            response.raise_for_status()
            return response.text

        time.sleep(10 * (attempt + 1))

    response.raise_for_status()
    return response.text


def get_page_html(link):
    # the live site is unreachable for long periods, so fall back
    # to the last archived snapshot of the same page when needed.
    try:
        response = requests.get(
            link,
            headers=DEFAULT_HEADERS,
            verify=False,
            timeout=30,
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return get_archived_html(link)


def scraper():

    # scrape data from maxbet scraper.

    soup = BeautifulSoup(get_page_html(JOBS_LINK), 'lxml')
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

# Company ---> Partnerd
# Link ------> https://partnerd.teamtailor.com/jobs

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from partnerd scraper.

    soup = GetStaticSoup("https://partnerd.teamtailor.com/jobs")
    job_list = []

    for job in soup.find_all('li', attrs = {'class': 'w-full'}):

        remote_span = job.find('span', attrs={'class': 'inline-flex items-center gap-x-2'})
        if remote_span is not None and remote_span.text:
            remote = remote_span.text
        else:
            remote = 'on-site'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('span').text,
            job_link = job.find('a')['href'],
            company = 'Partnerd',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = remote.strip(),
        ).to_dict())

    return job_list


def main():

    company_name = "Partnerd"
    logo_link = "https://uploads-ssl.webflow.com/61070548cd02cbe9343b5101/61070d5df465e95e28ce7183_Partnerd%20PNG%20Logo-p-500.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

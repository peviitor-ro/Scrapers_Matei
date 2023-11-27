
# Company ---> IGTSolutions
# Link ------> https://www.igtsolutions.com/romania/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from IGTSolutions scraper.

    soup = GetStaticSoup("https://www.igtsolutions.com/romania/")
    job_list = []

    for job in soup.find_all('tr'):

        # get jobs items from response
        job_list.append(Item(
            job_title= job.find('td', attrs = {'class': 'column-1'}).text,
            job_link = job.find('td', attrs = {'class': 'column-3'}).find('a')['href'],
            company = 'IGTSolutions',
            country = 'Romania',
            county = '',
            city = '',
            remote = 'remote',
        ).to_dict())

    return job_list


def main():

    company_name = "IGTSolutions"
    logo_link = "https://www.igtsolutions.com/wp-content/uploads/2022/07/igt-solutions-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

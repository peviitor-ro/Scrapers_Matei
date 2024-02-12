
# Company ---> inspet
# Link ------> https://www.inspet.ro/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from inspet scraper.

    soup = GetStaticSoup("https://www.inspet.ro/cariere/")
    job_list = []
    soup2 = soup.find('table', class_ = 'jobs-table')

    for job in soup2.find_all('tr'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('a').text.strip(),
            job_link = job.find('a')['href'],
            company = 'Inspet',
            country = 'Romania',
            county = get_county('Ploiesti'),
            city = 'Ploiesti',
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "Inspet"
    logo_link = "https://www.inspet.ro/wp-content/themes/inspet/images/logo.png?v=1.1"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

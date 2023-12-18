# Company ---> Intelactsoft
# Link ------> https://www.intelactsoft.com/jobs/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from intelactsoft scraper.

    soup = GetStaticSoup("https://www.intelactsoft.com/jobs/")
    job_list = []

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
    logo_link = "https://www.intelactsoft.com/wp-content/themes/intelactsoft/assets/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

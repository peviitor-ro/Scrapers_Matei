# Company ---> simplex
# Link ------> https://simplex.ro/posturi-vacante/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from simplex scraper.

    soup = GetStaticSoup("https://simplex.ro/posturi-vacante/")
    job_list = []
    
    for job in soup.find('ul', class_ = 'job-list').find_all('li'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('a').text.strip(),
            job_link = job.find('a')['href'],
            company = 'Simplex',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "Simplex"
    logo_link = "https://simplex.ro/image/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

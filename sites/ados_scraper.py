# Company ---> ados
# Link ------> https://www.adosfresh.ro/cariera/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from ados scraper.

    soup = GetStaticSoup("https://www.adosfresh.ro/cariera/")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'vc_row wpb_row vc_inner vc_row-fluid'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h3').text.strip(),
            job_link = job.find('a')['href'],
            company= 'Ados',
            country = 'Romania',
            county = '',
            city = '',
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "Ados"
    logo_link = "https://www.adosfresh.ro/wp-content/uploads/2023/10/logo-ados-footer-230.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

# Company ---> agrime
# Link ------> https://ag-prime.com/careers/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from agprime scraper.

    soup = GetStaticSoup("https://ag-prime.com/careers/")
    job_list = []
    
    for job in soup.find_all('div', attrs = {'class': 'job-column'}):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').text,
            job_link = job.find('a')['href'],
            company = 'AgPrime',
            country = 'Romania',
            county = get_county('Cluj-Napoca'),
            city = 'Cluj-Napoca',
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "AgPrime"
    logo_link = "https://ag-prime.com/wp-content/uploads/2022/06/cropped-cropped-agprimelogonewmoto.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

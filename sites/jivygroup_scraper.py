# Company ---> jivygroup
# Link ------> https://www.jivygroup.com/careers/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from jivygroup scraper.

    soup = GetStaticSoup("https://www.jivygroup.com/careers/")
    job_list = []
    
    for job in soup.find_all('article', class_ = 'eael-grid-post eael-post-grid-column'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('a', class_= 'eael-grid-post-link').text.strip(),
            job_link = job.find('a')['href'],
            company = 'JivyGroup',
            country = 'Romania',
            county = '',
            city = '',
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "jivygroup"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    # UpdateAPI().update_jobs(company_name, jobs)
    # UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

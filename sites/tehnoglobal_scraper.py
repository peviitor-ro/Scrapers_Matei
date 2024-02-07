# Company ---> tehnoglobal
# Link ------> https://www.tehnoglobal.ro/cariere/posturi-vacante

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from tehnoglobal scraper.

    soup = GetStaticSoup("https://www.tehnoglobal.ro/cariere/posturi-vacante")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'item-job'):
        title = job.find('h5').text.strip()
        if title == title.upper():
            get_remote = 'on-site'
        else: get_remote = ''
        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = job.find('h5').find('a')['href'],
            company = 'TehnoGlobal',
            country = 'Romania',
            county = get_county('Cluj-Napoca'),
            city = 'Cluj-Napoca',
            remote = get_remote,
        ).to_dict())

    return job_list


def main():

    company_name = "TehnoGlobal"
    logo_link = "https://www.tehnoglobal.ro/style/images/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

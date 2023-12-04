# Company ---> TemaEnergy
# Link ------> https://tema-energy.ro/despre-noi/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from temaenergy scraper.

    soup = GetStaticSoup("https://tema-energy.ro/despre-noi/cariere/")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'col-md-6 col-sm-6 col-xs-12'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', class_ = 'col-md-12 col-sm-12 col-xs-12 post_title_page').find('a').text.strip(),
            job_link = job.find('a')['href'],
            company = 'TemaEnergy',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "TemaEnergy"
    logo_link = "https://tema-energy.ro/wp-content/plugins/website-logo/images/logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

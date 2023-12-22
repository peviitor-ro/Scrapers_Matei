# Company ---> rodbun
# Link ------> https://rodbun.ro/cariere/cariere-oportunitati/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from rodbun scraper.

    soup = GetStaticSoup("https://rodbun.ro/cariere/cariere-oportunitati/")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'minti_masonrygrid_item masonry_image masonry_rl'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('span').text.strip(),
            job_link = job.find('a')['href'],
            company = 'rodbun',
            country = 'Romania',
            county = '',
            city = '',
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "rodbun"
    logo_link = "https://rodbun.ro/wp-content/uploads/2018/09/logo_red_small.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

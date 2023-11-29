# Company ---> reomedical
# Link ------> https://reo-medical.ro/cariere-2/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from reomedical scraper.

    soup = GetStaticSoup("https://reo-medical.ro/cariere-2/")
    job_list = []
    
    for job in soup.find_all('div', attrs = {'data-widget_type': 'image-box.default'}):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4', attrs = {'class': 'elementor-image-box-title'}).text,
            job_link = job.find('a')['href'],
            company = 'ReoMedical',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "ReoMedical"
    logo_link = "https://reo-medical.ro/wp-content/uploads/2021/08/REO-Medical-aparatura-medicala-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

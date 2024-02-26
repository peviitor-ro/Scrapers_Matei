# Company ---> karcher
# Link ------> https://www.kaercher.com/ro/despre-kaercher/cariere/posturi-vacante.html

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from karcher scraper.

    soup = GetStaticSoup("https://www.kaercher.com/ro/despre-kaercher/cariere/posturi-vacante.html")
    job_list = []
    
    for job in soup.find_all('section', class_ = ''):
        title = job.find('a', class_= 'btn btn-yellow')
        if title:
            title = title.text.strip()
            # get jobs items from response
            job_list.append(Item(
                job_title = title,
                job_link = job.find('a', class_= 'btn btn-yellow')['href'],
                company = 'Karcher',
                country = 'Romania',
                county = get_county('Bucuresti'),
                city = 'Bucuresti',
                remote= 'on-site',
            ).to_dict())

    return job_list


def main():

    company_name = "Karcher"
    logo_link = "https://s1.kaercher-media.com/versions/2023.22.1/static/img/kaercher_logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

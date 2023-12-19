
# Company ---> leviatan
# Link ------> https://leviatan.ro/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from leviatan scraper.

    soup = GetStaticSoup("https://leviatan.ro/cariere/")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'row max_width no-padding'):

        all_links = job.find_all('a')
        last_link = all_links[-1] if all_links else None
        last_href = last_link.get('href')

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').text.strip(),
            job_link = last_href,
            company = 'Leviatan',
            country = 'Romania',
            county = '',
            city = '',
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "Leviatan"
    logo_link = "https://leviatan.ro/wp-content/uploads/2021/11/png-color-leviatan.png.webp"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

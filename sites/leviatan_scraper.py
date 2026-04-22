
# Company ---> leviatan
# Link ------> https://leviatan.ro/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from leviatan scraper.

    soup = GetStaticSoup("https://leviatan.ro/cariere/")
    job_list = []

    # Leviatan does not expose job locations in the careers cards.
    # The company contact page lists the HQ in Splaiul Unirii 165, Sector 3, Bucuresti.
    city = 'Bucuresti'
    county = get_county(city)

    for job in soup.select('.blog-posts .blog-item .heading.title a.-unlink'):
        job_href = job.get('href')

        if not job_href or '/category/' in job_href:
            continue

        # get jobs items from response
        job_list.append(Item(
            job_title = job.text.strip(),
            job_link = job_href,
            company = 'Leviatan',
            country = 'Romania',
            county = county,
            city = city,
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

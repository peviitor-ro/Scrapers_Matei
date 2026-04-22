# Company ---> jti
# Link ------> https://jobs.jti.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def _translate_city(city: str) -> str:

    city_map = {
        'BUCHAREST': 'Bucuresti',
    }

    city = city.strip().upper()

    if city in city_map:
        return city_map[city]

    return city.title()


def scraper():

    # scrape data from jti scraper.
    base_url = "https://jobs.jti.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO&locale=ro_RO"
    page_number = 0
    job_list = []
    while True:
        url = f"{base_url}&startrow={page_number}" if page_number else base_url
        soup = GetStaticSoup(url)
        jobs = soup.select('table#searchresults tbody tr.data-row')

        if not jobs:
            break

        for job in jobs:
            title_link = job.select_one('a.jobTitle-link')
            location = job.select_one('span.jobLocation')

            if not title_link or not location:
                continue

            get_city = _translate_city(location.get_text(strip=True).split(',')[0])

            job_list.append(Item(
                job_title = title_link.text.strip(),
                job_link = 'https://jobs.jti.com' + str(title_link['href']),
                company = 'jti',
                country = 'Romania',
                county = get_county(get_city),
                city = get_city,
                remote = '',
            ).to_dict())

        if len(jobs) < 25:
            break

        page_number += 25

    return job_list


def main():

    company_name = "jti"
    logo_link = "https://pbs.twimg.com/profile_images/978547423822909440/dp5cg3vJ_400x400.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

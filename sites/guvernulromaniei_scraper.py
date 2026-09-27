from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)

BASE_URL = "https://posturi.gov.ro/toate-posturile/"


def parse_location(location: str):
    """location is either 'CITY, County' or just a county name."""
    if "," in location:
        city, county = (part.strip() for part in location.split(",", 1))
    else:
        city = county = location.strip()
    return city, county


def scraper():

    # scrape data from guvernulromaniei scraper.

    job_list = []
    page = 1

    while True:
        soup = GetStaticSoup(f"{BASE_URL}?pg_page={page}")
        jobs = soup.find_all('article', class_='pg-card')
        if not jobs:
            break

        for job in jobs:
            city, county = parse_location(
                job.find('div', class_='pg-card-city').find('span').text.strip()
            )
            job_list.append(Item(
                job_title=job.find('div', class_='pg-card-h').text.strip(),
                job_link=job.find('a', class_='pg-card-link')['href'],
                company='GuvernulRomaniei',
                country='Romania',
                county=county,
                city=city,
                remote='remote' if not city else 'on-site',
            ).to_dict())

        page += 1

    return job_list


def main():

    company_name = "GuvernulRomaniei"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHuEEV_LDvi5RpRoyxZYAX2InVXfC2Kzq1cQ&usqp=CAU"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

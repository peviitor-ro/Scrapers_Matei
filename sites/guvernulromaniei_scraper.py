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
        try:
            soup = GetStaticSoup(f"{BASE_URL}?pg_page={page}")
        except Exception:
            break
        jobs = soup.find_all('a', class_='pg-card')
        if not jobs:
            break

        try:
            for job in jobs:
                city_el = job.find('div', class_='pg-card-city')
                if city_el and city_el.find('span'):
                    city, county = parse_location(city_el.find('span').text.strip())
                else:
                    city, county = "", ""
                title_el = job.find('div', class_='pg-card-h')
                job_title = title_el.text.strip() if title_el else ""
                job_link = job.get('href', '')
                job_list.append(Item(
                    job_title=job_title,
                    job_link=job_link,
                    company='GuvernulRomaniei',
                    country='Romania',
                    county=county,
                    city=city,
                    remote='remote' if not city else 'on-site',
                ).to_dict())
        except Exception:
            break

        page += 1
        if page > 200:  # safety limit
            break

    return job_list


def main():

    company_name = "GuvernulRomaniei"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHuEEV_LDvi5RpRoyxZYAX2InVXfC2Kzq1cQ&usqp=CAU"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

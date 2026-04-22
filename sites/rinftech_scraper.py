# Company ---> rinftech
# Link ------> https://jobs.rinf.tech

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from rinftech scraper.

    job_list = []

    city_map = {
        'Bucharest': 'Bucuresti',
        'Cluj-Napoca': 'Cluj-Napoca',
        'Iasi': 'Iasi',
        'Timisoara': 'Timisoara',
        'Sibiu': 'Sibiu',
    }
    county_map = {
        'Bucuresti': 'Bucuresti',
        'Cluj-Napoca': 'Cluj',
        'Iasi': 'Iasi',
        'Timisoara': 'Timis',
        'Sibiu': 'Sibiu',
    }

    page = 1

    while page <= 6:
        url = 'https://jobs.rinf.tech' if page == 1 else f'https://jobs.rinf.tech/?page={page}'
        soup = GetStaticSoup(url)
        jobs = soup.select('main div.flex.flex-col.gap-3.border-b-2.border-border-secondary.py-4.text-left')

        if not jobs:
            break

        for job in jobs:

            title_link = job.find('a', href=True)
            if not title_link:
                continue

            location_items = job.select('div.flex.flex-wrap.gap-6.text-sm p.text-xs.font-semibold.text-ring')
            location_text = location_items[2].get_text(strip=True) if len(location_items) >= 3 else ''

            if location_text == 'Guadalajara':
                continue

            if location_text == 'Remote':
                remote_text = 'remote'
                city = ''
            else:
                remote_text = ''
                location_parts = [part.strip() for part in location_text.replace('|', ',').split(',') if part.strip()]
                romanian_cities = [city_map[part] for part in location_parts if part in city_map]

                if location_text == 'Romania':
                    romanian_cities = ['Bucuresti']
                    remote_text = 'remote'

                if not romanian_cities:
                    continue

                city = romanian_cities[0] if len(romanian_cities) == 1 else romanian_cities

            # get jobs items from response
            job_list.append(Item(
                job_title=title_link.get_text(strip=True),
                job_link=f"https://jobs.rinf.tech{title_link['href']}",
                company='rinf.tech',
                country='Romania',
                county=[county_map.get(single_city, get_county(single_city)) for single_city in city] if isinstance(city, list) else (county_map.get(city, get_county(city)) if city else ''),
                city=city,
                remote=remote_text,
            ).to_dict())

        page += 1

    return job_list


def main():

    company_name = "rinf.tech"
    logo_link = "https://stagiipebune.ro/media/cache/f0/60/f060b0a01bd022e9c28f3073cb5404bb.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

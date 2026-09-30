# Company ---> Partnerd
# Link ------> https://ats.partnerd.ro/c/partnerd

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


BASE_LINK = 'https://ats.partnerd.ro'
JOBS_LINK = f'{BASE_LINK}/c/partnerd'
REMOTE_TYPES = ('hybrid', 'remote', 'on-site')


def split_place_and_remote(meta_text):
    # the card meta line looks like 'Bucuresti, sector 2 · Hybrid' or just 'Hybrid'
    parts = [part.strip() for part in meta_text.split('·') if part.strip()]

    if not parts:
        return '', 'on-site'

    if len(parts) == 1:
        if parts[0].lower() in REMOTE_TYPES:
            return '', parts[0]
        return parts[0], 'on-site'

    return parts[0], parts[-1]


def get_county_and_city(place):
    for chunk in place.split(','):
        county = get_county(chunk.strip())
        if county:
            return county, chunk.strip()

    return get_county('Bucuresti'), 'Bucuresti'


def scraper():

    # scrape data from partnerd scraper.

    soup = GetStaticSoup(JOBS_LINK)
    job_list = []

    for job in soup.select('a[href*="/c/partnerd/jobs/"]'):

        title_tag = job.find('div', class_='line-clamp-2')
        if title_tag is None:
            continue

        meta_tag = title_tag.find_next_sibling()
        place, remote = split_place_and_remote(meta_tag.text if meta_tag else '')
        county, city = get_county_and_city(place)

        # get jobs items from response
        job_list.append(Item(
            job_title = title_tag.text.strip(),
            job_link = BASE_LINK + job['href'],
            company='Partnerd Scraper',
            country = 'Romania',
            county = county,
            city = city,
            remote = get_job_type(remote),
        ).to_dict())

    return job_list


def main():

    company_name = "Partnerd Scraper"
    logo_link = "https://uploads-ssl.webflow.com/61070548cd02cbe9343b5101/61070d5df465e95e28ce7183_Partnerd%20PNG%20Logo-p-500.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

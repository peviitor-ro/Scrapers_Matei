# Company ---> diversey
# Link ------> https://diversey.wd5.myworkdayjobs.com/Diversey?locationCountry=f2e609fe92974a55a05fc1cdc2852122
import requests
from __utils import (
    get_county,
    Item,
    UpdateAPI,
)

def prepare_post_request() -> tuple:

    # prepare post request for Diversey.

    url = 'https://solenis.wd1.myworkdayjobs.com/wday/cxs/solenis/Solenis/jobs'

    headers = {
        'Content-Type': 'application/json',
    }
    data_raw = {
    "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
    "limit": 20,
    "offset": 0,
    "searchText": "Diversey"
    }
    return url, headers, data_raw

def scraper():

    # scrape data from diversey scraper.
    job_list = []

    url, headers, data = prepare_post_request()
    total_jobs = None

    while total_jobs is None or data['offset'] < total_jobs:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        json_response = response.json()
        jobs = json_response.get('jobPostings', [])

        if not jobs:
            break

        total_jobs = json_response.get('total', 0)

        for job in jobs:
            get_location = job.get('locationsText', '')
            location_parts = [part.strip() for part in get_location.split(',') if part.strip()]
            city = location_parts[0] if location_parts else 'Bucuresti'

            if city in ('Bucharest', 'București'):
                city = 'Bucuresti'

            remote_type = str(job.get('remoteType', '')).lower()
            get_remote = 'remote' if 'remote' in remote_type else 'on-site'

            # get jobs items from response
            job_list.append(Item(
                job_title = job['title'],
                job_link = 'https://solenis.wd1.myworkdayjobs.com/en-US/Solenis' + job['externalPath'],
                company = 'Diversey',
                country = 'Romania',
                county = get_county(city),
                city = city,
                remote = get_remote,
            ).to_dict())

        data['offset'] += data['limit']

    return job_list


def main():

    company_name = "Diversey"
    logo_link = "https://findlogovector.com/wp-content/uploads/2019/01/diversey-logo-vector.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()

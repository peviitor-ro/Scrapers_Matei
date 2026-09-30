# Company ---> DowJones
# Link ------> https://dowjones.jobs/jobs/?location=Romania

import re
import unicodedata

from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

# dowjones.jobs is a nuxt single page app, the job listings are not in the html
# anymore. The frontend calls the jobsyn search api and scopes the results with
# the X-Origin header, so that is the endpoint we read the jobs from.
SEARCH_API = "https://prod-search-api.jobsyn.org/api/v1/solr/search"

SEARCH_HEADERS = {
    'Accept': 'application/json',
    'X-Origin': 'dowjones.jobs',
}

# the search api never returns more than 10 jobs per page, so we walk the pages.
NUM_ITEMS = 10


def get_job_link(job: dict) -> str:
    # the site builds the detail page as /<location slug>/<title slug>/<guid>/job/
    location = unicodedata.normalize('NFKD', job['location_exact'])
    location = location.encode('ascii', 'ignore').decode('ascii')
    location = re.sub(r'\W+', '-', location).strip('-').lower()

    return f"https://dowjones.jobs/{location}/{job['title_slug']}/{job['guid']}/job/"


def scraper():

    # scrape data from dowjones scraper.

    job_list = []
    offset = 0

    while True:

        json_data = GetRequestJson(
            f"{SEARCH_API}?location=Romania&num_items={NUM_ITEMS}&page=1&offset={offset}",
            custom_headers = SEARCH_HEADERS,
        )

        if not isinstance(json_data, dict):
            break

        jobs = json_data.get('jobs') or []

        for json_job in jobs:

            hiring_place = json_job.get('location_exact') or ''

            # get jobs items from response
            job_list.append(Item(
                job_title = json_job['title_exact'].strip(),
                job_link = get_job_link(json_job),
                company = 'DowJones',
                country = json_job['country_ac'].strip(),
                county = get_county('Bucuresti'),
                city = 'Bucuresti',
                remote = get_job_type('remote' if 'virtual' in hiring_place.lower() else 'on-site'),
            ).to_dict())

        if not jobs or not json_data.get('pagination', {}).get('has_more_pages'):
            break

        offset += len(jobs)

    return job_list


def main():

    company_name = "DowJones"
    logo_link = "https://dn9tckvz2rpxv.cloudfront.net/dow-jones/img/logo2.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

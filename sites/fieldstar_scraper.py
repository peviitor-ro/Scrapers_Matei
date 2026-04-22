# Company ---> FieldStar
# Link ------> https://fieldstar.mingle.ro/ro/apply

import requests

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from FieldStar scraper.

    job_list = []
    page = 0

    while True:
        response = requests.get(
            'https://mingle.ro/api/boards/careers-page/jobs',
            params={
                'company': 'fieldstar',
                'page': page,
                'pageSize': 100,
            },
            timeout=30,
        )
        json_data = response.json().get('data', {})
        jobs = json_data.get('results', [])

        if not jobs:
            break

        for job in jobs:
            locations = [location.get('label', '').strip() for location in job.get('locations', []) if location.get('label')]
            city_job = [city.replace('Cluj', 'Cluj-Napoca') for city in locations]
            county_job = [get_county(city) for city in city_job]

            # get jobs items from response
            job_list.append(Item(
                job_title = job['title'],
                job_link = f'https://fieldstar.mingle.ro/ro/apply/{job["uid"]}',
                company = 'FieldStar',
                country = 'Romania',
                county = county_job,
                city = city_job,
                remote = 'on-site',
            ).to_dict())

        if not json_data.get('pagination', {}).get('hasNext'):
            break

        page += 1

    return job_list


def main():

    company_name = "FieldStar"
    logo_link = "https://trt.ro/wp-content/uploads/Logouri-website-TRT-2022-Fieldstar-300x300.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

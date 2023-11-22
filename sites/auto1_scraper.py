# Company ---> Auto1 Group
# Link ------> https://www.auto1-group.com/en/jobs/?country=Romania

from __utils import (
    GetRequestJson,
    Item,
    UpdateAPI,
    get_county,
)


def scraper():
    # scrape data from Auto1 Group scraper.

    page = 1
    job_list = []

    while page <= 3:

        json_data = GetRequestJson(f"https://www.auto1-group.com/smart-recruiters/jobs/search/?page={page}&country=Romania")
        jobs = json_data['jobs']['hits']['hits']

        for job in jobs:
            town = job['_source']['locationCity']

            if town == 'Bucharest':
                town = 'Bucuresti'

            # get jobs items from response
            job_list.append(Item(
                job_title = job['_source']['title'],
                job_link = f'https://www.auto1-group.com/en/jobs/{job["_source"]["url"]}',
                company = 'Auto1Group',
                country = 'Romania',
                county = get_county(town),
                city = town,
                remote = 'on-site',
            ).to_dict())

        page = page + 1

    return job_list


def main():

    company_name = "Auto1Group"
    logo_link = "https://www.auto1-group.com/images/logo-auto1-group-v4.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

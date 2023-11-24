# Company ---> Clevertech
# Link ------> https://clevertech.biz/jobs

from __utils import (
    GetRequestJson,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from clevertech scraper.

    json_data = GetRequestJson('https://clevertech.biz/_next/data/AGrh3n8knChzMTSDHJ4Pz/jobs/apply.json?applicationType=default')

    job_list = []

    for job in json_data['pageProps']['activeJobs']:

        # get jobs items from response
        job_list.append(Item(
            job_title = job['name'],
            job_link = 'https://clevertech.biz/remote-jobs/' + job['slug'],
            company = 'Clevertech',
            country = 'Romania',
            county = '',
            city = '',
            remote = 'remote',
        ).to_dict())

    return job_list


def main():

    company_name = "Clevertech"
    logo_link = "https://clevertech.biz/_next/static/media/ct-logo-redgrey.380f31ad.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

# Company ---> Clevertech
# Link ------> https://clevertech.biz/jobs
import requests
from __utils import (
    GetStaticSoup,
    GetRequestJson,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from clevertech scraper.

    job_list = []
    flag = 1
    while flag < 3:
        json_data = GetRequestJson(f'https://lumenalta.com/api/jobs?page={flag}&limit=10&name=')

        for job in json_data['data']:

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
        flag += 1

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

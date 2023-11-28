# Company ---> Clevertech
# Link ------> https://clevertech.biz/jobs

from __utils import (
    GetStaticSoup,
    GetRequestJson,
    Item,
    UpdateAPI,
)


def get_id():

    soup = GetStaticSoup('https://clevertech.biz/jobs')
    script_id = soup.find_all('script', attrs = {'src': '/_next/static/GP71h1Ih1nzvHYndylkaB/_ssgManifest.js'})
    script_key = str(script_id).split('/')[3]

    return script_key

def scraper():

    # scrape data from clevertech scraper.
    key = get_id()
    json_data = GetRequestJson(f'https://clevertech.biz/_next/data/{key}/jobs/apply.json?applicationType=default')
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

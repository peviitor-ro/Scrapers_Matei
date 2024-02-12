# Company ---> diversey
# Link ------> https://diversey.wd5.myworkdayjobs.com/Diversey?locationCountry=f2e609fe92974a55a05fc1cdc2852122
import requests
from __utils import (
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def prepare_post_request() -> tuple:

    # prepare post request for Diversey.

    url = 'https://diversey.wd5.myworkdayjobs.com/wday/cxs/diversey/Diversey/jobs'

    headers = {
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://diversey.wd5.myworkdayjobs.com',
        'Referer': 'https://diversey.wd5.myworkdayjobs.com/Diversey?locationCountry=f2e609fe92974a55a05fc1cdc2852122',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Calypso-Csrf-Token': 'b161c88c-cd97-4f09-aa88-389add456b6d',
    }
    data_raw = {
    "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
    "limit": 20,
    "offset": 0,
    "searchText": ""
    }
    return url, headers, data_raw

def scraper():

    # scrape data from diversey scraper.
    url, headers, data = prepare_post_request()
    response = requests.post(url, headers=headers, json=data)
    json_response = response.json()

    job_list = []
    for job in json_response['jobPostings']:

        get_location = job['locationsText']
        if "-" in get_location:
            orase = "Bucuresti"
            get_remote = "on-site"
        elif 'locations' in get_location.lower():
            orase = "Bucuresti"
            get_remote = "remote"

        # get jobs items from response
        job_list.append(Item(
            job_title = job['title'],
            job_link = 'https://diversey.wd5.myworkdayjobs.com/en-US/Diversey' + job['externalPath'],
            company = 'Diversey',
            country = 'Romania',
            county = '',
            city = orase,
            remote = get_remote,
        ).to_dict())

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

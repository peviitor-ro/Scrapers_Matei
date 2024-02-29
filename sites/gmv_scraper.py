# Company ---> gmv
# Link ------> https://gmv.csod.com/ux/ats/careersite/4/home?c=gmv&lq=Russia&pl=ChIJ-yRniZpWPEURE_YRZvj9CRQ&country=ro&lang=en-US

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)

import requests
from bs4 import BeautifulSoup
import re


def prepare_post_request():

    url = "https://eu-fra.api.csod.com/rec-job-search/external/jobs"
    token = get_token()
    
    headers = {
        "authority": "eu-fra.api.csod.com",
        "accept": "application/json; q=1.0, text/*; q=0.8, */*; q=0.1",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": f"Bearer {token}",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "csod-accept-language": "en-US",
        "origin": "https://gmv.csod.com",
        "referer": "https://gmv.csod.com/",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    data = {
        "careerSiteId": 4,
        "careerSitePageId": 4,
        "pageNumber": 1,
        "pageSize": 25,
        "cultureId": 1,
        "searchText": "",
        "cultureName": "en-US",
        "states": [],
        "countryCodes": ["ro"],
        "cities": [],
        "placeID": "ChIJ-yRniZpWPEURE_YRZvj9CRQ",
        "radius": None,
        "postingsWithinDays": None,
        "customFieldCheckboxKeys": [],
        "customFieldDropdowns": [],
        "customFieldRadios": []
    }

    return url, headers, data


def get_token():
    session = requests.Session()
    response = session.get(url='https://gmv.csod.com/ux/ats/careersite/4/home?c=gmv&lq=Russia&pl=ChIJ-yRniZpWPEURE_YRZvj9CRQ&country=ro&lang=en-US')
    soup = BeautifulSoup(response.text, 'lxml')

    regex = r'"token":"([^"]+)"'
    matches = re.findall(regex, str(soup))
    if matches:
        token = matches[0]

    return token.strip()


def scraper():

    # scrape data from gmv scraper.

    url, headers, data = prepare_post_request()
    response = requests.post(url, headers=headers, json=data)
    json_data = response.json()

    job_list = []

    for job in json_data['data']['requisitions']:
        get_country = job['locations'][0]['country']
        get_city = job['locations'][0]['city']
        if get_city == 'Bucharest':
            get_city = 'Bucuresti'
        if get_country == 'RO':
            get_country = 'Romania'
        links = f"https://gmv.csod.com/ux/ats/careersite/4/home/requisition/{job['requisitionId']}?c=gmv&lang=en-US"

        # get jobs items from response
        job_list.append(Item(
            job_title = job['displayJobTitle'],
            job_link = links,
            company = 'Gmv',
            country = get_country,
            county = get_county(get_city),
            city = get_city,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "Gmv"
    logo_link = "https://www.gmv.com/sites/default/files/content/image/2021/08/17/115/gmv_bckgrgbgrey.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

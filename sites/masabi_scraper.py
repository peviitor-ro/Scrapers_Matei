# Company ---> masabi
# Link ------> https://careers.masabi.com/

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)
import requests


def prepare_post_request():

    url = 'https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams'

    headers = {
        'Authority': 'jobs.ashbyhq.com',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Apollographql-Client-Name': 'frontend_non_user',
        'Apollographql-Client-Version': '0.1.0',
        'Content-Type': 'application/json',
        'Origin': 'https://jobs.ashbyhq.com',
        'Referer': 'https://jobs.ashbyhq.com/masabi?embed=js',
        'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'Sec-Ch-Ua-mobile': '?0',
        'Sec-Ch-Ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    data = {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {
            "organizationHostedJobsPageName": "masabi"
        },
        "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }\n    jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}\n"
        }

    return url, headers, data


def scraper():

    # scrape data from masabi scraper.
    url, headers, data = prepare_post_request()
    response = requests.post(url, headers=headers, json=data)
    json_data = response.json()

    job_list = []
    for job in json_data['data']['jobBoard']['jobPostings']:
        cluj_found = False
        bucharest_found = False
        for secondary_location in job['secondaryLocations']:
            location_name = secondary_location['locationName']

            if location_name == 'Cluj' and not cluj_found:
                location_name = 'Cluj-Napoca'
                job_list.append(Item(
                    job_title = job['title'],
                    job_link = f'https://careers.masabi.com/masabi-jobs/?ashby_jid={job['id']}',
                    company = 'Masabi',
                    country = 'Romania',
                    county = get_county(location_name),
                    city = location_name,
                    remote = 'Remote',
                ).to_dict())
                cluj_found = True

            elif location_name == 'Bucharest' and not bucharest_found:
                location_name = 'Bucuresti'
                job_list.append(Item(
                    job_title = job['title'],
                    job_link = f'https://careers.masabi.com/masabi-jobs/?ashby_jid={job['id']}',
                    company = 'Masabi',
                    country = 'Romania',
                    county = get_county(location_name),
                    city = location_name,
                    remote = 'Remote',
                ).to_dict())
                bucharest_found = True

        if cluj_found and bucharest_found:
            break
    return job_list


def main():

    company_name = "Masabi"
    logo_link = "https://careers.masabi.com/wp-content/uploads/2023/01/06-red-black.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()

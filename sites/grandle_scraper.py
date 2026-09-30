# Company ---> grandle
# Link ------> https://gradle.com/careers/ (redirects to https://develocity.ai/careers/)
# Board -----> https://job-boards.greenhouse.io/gradle (jobs public API)

from __utils import (
    GetRequestJson,
    Item,
    UpdateAPI,
)

JOBS_API_LINK = 'https://boards-api.greenhouse.io/v1/boards/gradle/jobs'


def scraper():

    # scrape data from grandle scraper.

    response = GetRequestJson(JOBS_API_LINK)
    job_list = []

    for job in response.get('jobs', []):

        check = job.get('location', {}).get('name', '').strip()
        if check.startswith('Europe') or check == 'Anywhere':

        # get jobs items from response
            job_list.append(Item(
                job_title = job['title'].strip(),
                job_link = job['absolute_url'],
                company = 'Grandle',
                country = 'Romania',
                county = '',
                city = '',
                remote = 'remote',
            ).to_dict())
        else: continue

    return job_list


def main():

    company_name = "Grandle"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Gradle_logo.png/799px-Gradle_logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

# Company ---> grandle
# Link ------> https://gradle.com/careers/

from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from grandle scraper.

    soup = GetStaticSoup("https://gradle.com/careers/")
    job_list = []
    
    for job in soup.find_all('li', class_ = 'careers__jobs-list'):

        check = job.find('div', class_ = 'careers__job-location').text.strip()
        if check == 'Europe' or check == 'Anywhere':

        # get jobs items from response
            job_list.append(Item(
                job_title = job.find('a').text.strip(),
                job_link = job.find('a')['href'],
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

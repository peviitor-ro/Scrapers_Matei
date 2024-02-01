# Company ---> aylo
# Link ------> https://www.aylo.com/careers/category-details/#department=All%20Departments&location=Bucharest%2C%20Romania

from __utils import (
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from aylo scraper.

    json_data = GetRequestJson('https://boards-api.greenhouse.io/v1/boards/aylo/jobs')
    job_list = []
    
    for job in json_data['jobs']:
        if job['location']['name'] == 'Bucharest, Romania':

            if job['location']['name'].split(',')[0] == "Bucharest":
                get_city = 'Bucuresti'
            # get jobs items from response
            job_list.append(Item(
                job_title = job['title'],
                job_link = job['absolute_url'],
                company = 'Aylo',
                country = 'Romania',
                county = get_county(get_city),
                city = get_city,
                remote='',
            ).to_dict())

    return job_list


def main():

    company_name = "Aylo"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Aylo_logo.svg/2560px-Aylo_logo.svg.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

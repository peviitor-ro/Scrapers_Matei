# Company ---> Bookster
# Link ------> https://cariere.bookster.ro/

from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from Bookster scraper.

    json_data = GetRequestJson("https://cariere.bookster.ro/api/jobs/list")
    job_list = []

    for json_job in json_data:

        # get jobs items from response
        job_list.append(Item(
            job_title = json_job['Title'],
            job_link = 'https://cariere.bookster.ro/view/' + json_job['Slug'],                company = 'Bookster',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = get_job_type('hybrid'),
        ).to_dict())

    return job_list


def main():

    company_name = "Bookster"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGN1kBfgbjJS_jH2S2Fz2l_NhRlwI2HRpfTQKJkmM3&s"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

# Company ---> jti
# Link ------> https://jobs.jti.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from jti scraper.
    url = "https://jobs.jti.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO"
    page_number = 0
    job_list = []
    while page_number <= 25:
        soup = GetStaticSoup(url)

        for job in soup.find_all('div', 'jobdetail-phone visible-phone'):
            span_elements = job.find_all('span')

            if len(span_elements) >= 4:
                get_city = span_elements[3].text
                if get_city == 'Bucharest':
                    get_city = 'Bucuresti'

                # get jobs items from response
            job_list.append(Item(
                job_title = job.find('a').text.strip(),
                job_link = 'https://jobs.jti.com' + str(job.find('a')['href']),
                company = 'jti',
                country = job.find('span', class_ = 'jobShifttype visible-phone').text.strip(),
                county = '',
                city = get_city,
                remote = '',
            ).to_dict())
        page_number += 25
        url = f"{url}&startrow={page_number}"
    return job_list


def main():

    company_name = "jti"
    logo_link = "https://pbs.twimg.com/profile_images/978547423822909440/dp5cg3vJ_400x400.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

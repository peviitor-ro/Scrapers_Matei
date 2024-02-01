# Company ---> mercedes
# Link ------> https://www.mercedes-benz.ro/passengercars/brand/careers/opportunities.html

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import re

def scraper():

    # scrape data from mercedes scraper.

    soup = GetStaticSoup("https://www.mercedes-benz.ro/passengercars/brand/careers/opportunities.html")
    job_list = []
    
    for job in soup.find('div', class_='responsivegrid aem-GridColumn aem-GridColumn--default--12').find_all('script'):

        if job.string:
            if "label" in job.string:
                start_index = job.string.find('"label":"') + len('"label":"')
                end_index = job.string.find('","', start_index)
                text = job.string[start_index:end_index]
                urls = re.findall(r'\"url\":\"(.*?\.pdf)\"', job.string)

                for url in urls:
                    # get jobs items from response
                    job_list.append(Item(
                        job_title = text.strip(),
                        job_link = 'https://www.mercedes-benz.ro' + url,
                        company = 'Mercedes',
                        country = 'Romania',
                        county='',
                        city='',
                        remote='',
                    ).to_dict())

    return job_list


def main():

    company_name = "Mercedes"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Mercedes-Logo.svg/1024px-Mercedes-Logo.svg.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

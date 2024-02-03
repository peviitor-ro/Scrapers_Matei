# Company ---> keyence
# Link ------> https://www.keyencecareer.eu/romania.html

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import re

def scraper():

    # scrape data from keyence scraper.

    soup = GetStaticSoup("https://www.keyencecareer.eu/romania.html")
    job_list = []

    for job in soup.find_all('h3', class_ = 'h2 itemTitle actItemTitle'):
        title = job.find('a').text.strip()
        get_city = re.findall(r'\b(?:Cluj-Napoca|Timisoara|Oradea)\b', title)
        oras = ', '.join(get_city)
        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = job.find('a')['href'],
            company = 'Keyence',
            country = 'Romania',
            county = '',
            city = oras,
            remote='',
        ).to_dict())
    return job_list


def main():

    company_name = "Keyence"
    logo_link = "https://www.keyencecareer.eu/_images/logo_small.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

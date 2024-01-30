# Company ---> GuvernulRomaniei
# Link ------> https://posturi.gov.ro/

from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from guvernulromaniei scraper.

    job_list = []
    base_url = "https://posturi.gov.ro/page/"

    for page_number in range(1, 28):
        url = base_url + str(page_number)
        soup = GetStaticSoup(url)
    
        for job in soup.find_all('article', class_ = 'box'):

            location = job.find('div', class_ = 'locatie').text.strip()

            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('div', class_ = 'title').find('a').text.strip(),
                job_link = job.find('div', class_ = 'title').find('a')['href'],
                company = 'GuvernulRomaniei',
                country = 'Romania',
                county = '',
                city = location,
                remote = 'on-site' if location else 'remote',
            ).to_dict())

    return job_list


def main():

    company_name = "GuvernulRomaniei"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHuEEV_LDvi5RpRoyxZYAX2InVXfC2Kzq1cQ&usqp=CAU"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

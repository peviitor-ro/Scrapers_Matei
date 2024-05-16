from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from guvernulromaniei scraper.

    job_list = []
    url = "https://posturi.gov.ro/page/1"
    index = 0

    while index < 48:
        soup = GetStaticSoup(url)
        for job in soup.find_all('article', class_='box'):

            location = job.find('div', class_='locatie').text.strip()

            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('div', class_='title').find('a').text.strip(),
                job_link = job.find('div', class_='title').find('a')['href'],
                company = 'GuvernulRomaniei',
                country = 'Romania',
                county = location,
                city = '',
                remote = 'on-site' if location else 'remote',
            ).to_dict())

        index += 1
        url = f"https://posturi.gov.ro/page/{index + 1}"

    return job_list


def main():

    company_name = "GuvernulRomaniei"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHuEEV_LDvi5RpRoyxZYAX2InVXfC2Kzq1cQ&usqp=CAU"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

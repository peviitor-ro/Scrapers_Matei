# Company ---> DowJones
# Link ------> https://dowjones.jobs/jobs/?location=Romania

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from dowjones scraper.

    soup = GetStaticSoup("https://dowjones.jobs/jobs/?location=Romania")

    job_list = []

    for job in soup.find_all('li', attrs = {'class': 'direct_joblisting with_description'}):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').find('a').text.strip(),
            job_link = 'https://dowjones.jobs' + job.find('h4').find('a')['href'],
            company = 'DowJones',
            country = job.find('span', attrs = {'class': 'hiringPlace'}).text.strip(),
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "DowJones"
    logo_link = "https://dn9tckvz2rpxv.cloudfront.net/dow-jones/img/logo2.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

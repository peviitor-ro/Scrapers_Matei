# Company ---> saintgobain
# Link ------> https://joinus.saint-gobain.com/ro?f%5B0%5D=tara%3Aro

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from saintgobain scraper.

    soup = GetStaticSoup("https://joinus.saint-gobain.com/ro?f%5B0%5D=tara%3Aro")
    job_list = []

    for job in soup.find_all('div', class_ = 'offer-card-body'):
        oras = job.find('div', class_='field__item').text.split()[-1]
        if oras == 'Cluj':
            oras = 'Cluj-Napoca'
        elif oras == 'Prahova':
            oras = 'Ploiesti'
        elif oras == 'Ilfov':
            oras = 'Branesti'
        elif oras == '':
            oras = 'Ploiesti'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('span').text.strip(),
            job_link = 'https://joinus.saint-gobain.com' + job.find('a')['href'],
            company = 'SaintGobain',
            country = 'Romania',
            county = '',
            city = oras,
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "SaintGobain"
    logo_link = "https://joinus.saint-gobain.com/sites/joinus.saint-gobain.com/files/logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

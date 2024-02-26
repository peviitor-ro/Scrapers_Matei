#
# Company ---> maxbet
# Link ------> https://maxbetgroup.ro/joburi

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from maxbet scraper.

    soup = GetStaticSoup("https://maxbetgroup.ro/joburi")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'col-xl-6 col-lg-6 col-md-6 mb-3'):

        oras = str(job.find('div', class_ = 'location').text.strip())
        if oras == 'Piatra Neamț':
            oras = 'Piatra-Neamt'
        if oras == 'Târgu Mureș':
            oras = 'Targu-Mures'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', class_ = 'job-name').text.strip(),
            job_link = job.find('a')['href'],
            company = 'MaxBet',
            country = 'Romania',
            county = '',
            city = oras,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "MaxBet"
    logo_link = "https://maxbetgroup.ro/assets/app/images/maxbet-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

# Company ---> FieldStar
# Link ------> https://www.fieldstar.ro/jobs/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from FieldStar scraper.

    soup = GetStaticSoup("https://www.fieldstar.ro/jobs/")
    job_list = []

    for job in soup.find_all('div', attrs = {'class': 'awsm-job-listing-item awsm-grid-item'}):

        locatie_oras = job.find('div', attrs={'class': 'awsm-job-specification-item awsm-job-specification-locatie'})
        if locatie_oras:
            cities = locatie_oras.find_all('span', attrs={'class': 'awsm-job-specification-term'})
            city_list = [city.text for city in cities]
            city_job = ', '.join(city_list)                       # MANIPULEZ MAI MULTE ORASE INTR-UN SINGUR STRING

        if city_job == 'Remote':
            city_job = ''
            remote = 'remote'                                     # ADD REMOTE MANUAL, PT CA PE SITE
        else:                                                          # LA CITY E SCRIS REMOTE
            remote = 'on-site'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', attrs = {'class': 'awsm-grid-left-col'}).text.strip(),
            job_link = job.find('a')['href'],
            company = 'FieldStar',
            country = 'Romania',
            county = '',
            city = city_job,
            remote = get_job_type(remote),
        ).to_dict())
    print(job_list)
    return job_list


def main():

    company_name = "FieldStar"
    logo_link = "https://trt.ro/wp-content/uploads/Logouri-website-TRT-2022-Fieldstar-300x300.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

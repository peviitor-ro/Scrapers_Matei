# Company ---> autocobalcescu
# Link ------> https://www.autocobalcescu.ro/hr

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from AutoCobalcescu scraper.

    soup = GetStaticSoup("https://www.autocobalcescu.ro/hr")
    job_list = []
    
    for job in soup.find_all('div', class_= 'col-12'):

        job_location = job.find('h6', class_='card-title').text.strip()
        if 'Bucuresti' in job_location:
            get_city = 'București'
        elif 'Pitești' in job_location:
            get_city = 'Pitesti'
        else:
            get_city = 'Bucuresti'
        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h6', class_= 'card-title').text.strip(),
            job_link = job.find('div', class_= 'card-body').find('a')['href'],
            company = 'AutoCobalcescu',
            country = 'Romania',
            county = get_county(get_city),
            city = get_city,
            remote= '',
        ).to_dict())
    print(job_list)
    return job_list


def main():

    company_name = "AutoCobalcescu"
    logo_link = "https://www.autocobalcescu.ro/images/logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

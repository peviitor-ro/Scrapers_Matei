# Company ---> gts
# Link ------> https://www.gts.ro/ro/roluri-disponibile

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from gts scraper.

    soup = GetStaticSoup("https://www.gts.ro/ro/roluri-disponibile")
    job_list = []

    for job in soup.find_all('tr')[1:]:
        get_city = job.find('td', class_='views-field-field-city').text.strip()
        if get_city == 'Bucure\u00c8\u0099ti':
            get_city = 'Bucuresti'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('td', class_='views-field-title').text.strip(),
            job_link = f'https://www.gts.ro/ro{job.find('a')['href']}',
            company = 'gts',
            country= 'Romania',
            county = '',
            city = get_city,
            remote='',
        ).to_dict())

    return job_list


def main():

    company_name = "gts"
    logo_link = "data:image/png;base64,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"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

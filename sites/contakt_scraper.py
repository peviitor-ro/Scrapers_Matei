# Company ---> contakt
# Link ------> https://www.contakt.ro/cariere

from urllib.parse import quote, urlparse, parse_qs
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from contakt scraper.

    soup = GetStaticSoup("https://www.contakt.ro/cariere")
    job_list = []

    for job in soup.find_all('div', class_ = 'c-jobs-list__item-wrapper'):

        location = job.find('div', class_='c-jobs-list__location').text.split(',', 1)[1].strip()
        if 'sector' in location.lower():
            location = 'Bucuresti'
        # AU CA SI "APLICA" LINK DE MAIL. INCERC SA IAU LINK-UL DE LA MAIL CU TOT CU SUBIECT
        link = job.find('div', class_ = 'c-jobs-list collapse').find('a')['href']

        email = link.split(':')[1].split('?')[0]
        query_params = parse_qs(urlparse(link).query)
        subject = query_params['subject'][0] if 'subject' in query_params else None
        escaped_email = quote(email)
        escaped_subject = quote(subject)
        new_link = f'mailto:{escaped_email}?subject={escaped_subject}'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', class_ = 'c-jobs-list__title').text.strip(),
            job_link = new_link,
            company = 'contakt',
            country = 'Romania',
            county = get_county(location),
            city = location,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "contakt"
    logo_link = "https://www.contakt.ro/media/settings/2023/02/27/logo-9450.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

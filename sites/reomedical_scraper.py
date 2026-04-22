# Company ---> reomedical
# Link ------> https://reo-medical.ro/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from reomedical scraper.

    soup = GetStaticSoup("https://reo-medical.ro/cariere/")
    job_list = []

    for title_link in soup.find_all('a', href=True):
        href = title_link['href']

        if '/cariere/' not in href or href.rstrip('/') == 'https://reo-medical.ro/cariere':
            continue

        title_tag = title_link.find_parent('h3', class_='elementor-heading-title')
        if not title_tag:
            continue

        job_card = title_tag
        while job_card and not job_card.find('span', class_='elementor-icon-list-text'):
            job_card = job_card.parent

        location = 'Bucuresti'
        if job_card:
            location_tag = job_card.find('span', class_='elementor-icon-list-text')
            if location_tag:
                location = location_tag.get_text(strip=True).replace('București', 'Bucuresti')

        # get jobs items from response
        job_list.append(Item(
            job_title = title_link.get_text(strip=True),
            job_link = href,
            company = 'ReoMedical',
            country = 'Romania',
            county = get_county(location),
            city = location,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "ReoMedical"
    logo_link = "https://reo-medical.ro/wp-content/uploads/2021/08/REO-Medical-aparatura-medicala-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

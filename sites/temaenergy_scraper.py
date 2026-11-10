# Company ---> TemaEnergy
# Link ------> https://tema-energy.ro/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from temaenergy scraper.

    soup = GetStaticSoup("https://tema-energy.ro/despre-noi/cariere/")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'col-md-6 col-sm-6 col-xs-12'):

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', class_ = 'col-md-12 col-sm-12 col-xs-12 post_title_page').find('a').text.strip(),
            job_link = job.find('a')['href'],
            company = 'TemaEnergy',
            country = 'Romania',
            county = get_county('Bucuresti'),
            city = 'Bucuresti',
            remote = 'on-site',
        ).to_dict())

    if not job_list:
        bestjobs = GetStaticSoup("https://www.bestjobs.eu/company-profile/tema-energy", timeout=30)
        seen_links = set()

        for link in bestjobs.find_all('a', href=True):
            href = link['href']
            if not href.startswith('/loc-de-munca/'):
                continue

            job_link = f"https://www.bestjobs.eu{href}"
            if job_link in seen_links:
                continue

            card = link.find_parent(
                'div', class_=lambda classes: classes and 'group' in classes and 'relative' in classes
            )
            if card is None or 'Tema Energy' not in card.get_text(' ', strip=True):
                continue

            title_tag = card.find('h2')
            title = title_tag.get_text(' ', strip=True) if title_tag else link.get_text(' ', strip=True)
            city = 'Bucuresti'

            location = card.find('a', href=lambda value: value and 'locuri-de-munca-in-' in value)
            if location is not None:
                location_text = location.get('title') or location.get_text(' ', strip=True)
                city = location_text.split(',')[0].strip() or city
                if 'Bucure' in city:
                    city = 'Bucuresti'

            seen_links.add(job_link)
            job_list.append(Item(
                job_title = title,
                job_link = job_link,
                company = 'TemaEnergy',
                country = 'Romania',
                county = get_county(city),
                city = city,
                remote = 'on-site',
            ).to_dict())

    return job_list


def main():

    company_name = "TemaEnergy"
    logo_link = "https://tema-energy.ro/wp-content/plugins/website-logo/images/logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

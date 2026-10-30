# Company ---> Altimate
# Link ------> https://www.altimate.ro/category/cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from Altimate scraper.

    job_list = []
    first_page = GetStaticSoup(f"https://www.altimate.ro/category/cariere")

    for page_num in range(2):
        if page_num == 0:
            current_page = first_page
        else:
            current_page = GetStaticSoup(f"https://www.altimate.ro/category/cariere/page/{page_num + 1}/")


        for job in current_page.find_all('div', attrs={'class': 'elementor-post__text'}):

            title = job.find('h2', attrs={'class': 'elementor-post__title'}).text.strip()
            if 'R\u00e2mnicu V\u00e2lcea' in title:
                city = 'Ramnicu Valcea'
            else:
                city = 'Bucuresti'

            job_list.append(Item(
                job_title= title ,
                job_link=job.find('h2', attrs={'class': 'elementor-post__title'}).find('a')['href'],
                company='Altimate',
                country='Romania',
                county = get_county(city),
                city = city,
                remote='on-site',
            ).to_dict())

    # The careers page currently has no posts, so fall back to the company's
    # active listings on BestJobs.
    if not job_list:
        bestjobs = GetStaticSoup("https://www.bestjobs.eu/company-profile/altimate", timeout=30)
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
            if card is None:
                continue

            title_tag = card.find('h2')
            if title_tag is None or 'Altimate' not in card.get_text(' ', strip=True):
                continue

            title = title_tag.get_text(' ', strip=True)
            city = 'Ramnicu Valcea' if ('R\u00e2mnicu V\u00e2lcea' in title or 'Ramnicu Valcea' in title) else 'Bucuresti'

            location = card.find('a', href=lambda value: value and 'locuri-de-munca-in-' in value)
            if location is not None:
                location_text = location.get('title') or location.get_text(' ', strip=True)
                city = location_text.split(',')[0].strip() or city
                if 'Bucure' in city:
                    city = 'Bucuresti'
                elif 'V\u00e2lcea' in city or 'Valcea' in city:
                    city = 'Ramnicu Valcea'

            seen_links.add(job_link)
            job_list.append(Item(
                job_title=title,
                job_link=job_link,
                company='Altimate',
                country='Romania',
                county=get_county(city),
                city=city,
                remote='on-site',
            ).to_dict())

    return job_list


def main():

    company_name = "Altimate"
    logo_link = "https://www.altimate.ro/wp-content/uploads/2023/03/Logo-Altimate-Final-Small-Size-Pozitiv.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

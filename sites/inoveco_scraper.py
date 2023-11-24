# Company ---> inoveco
# Link ------> https://inovecoexpert.ro/posturi-disponibile/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from Inoveco scraper.

    soup = GetStaticSoup("https://inovecoexpert.ro/posturi-disponibile/")
    job_list = []

    joburi = soup.find_all('div', attrs ='elementor-widget-wrap elementor-element-populated')

    for job in joburi:
                            # IA TOATE LINK URILE DE PE BUTOANE
        title_elem = job.find('div', attrs = 'elementor-button-wrapper')
        link = title_elem.find('a')['href'] if title_elem else None

        if link:            # INTRA PE FIECARE LINK CA SA IA TITLUL
            title_pag2_soup = GetStaticSoup(link)
            if title_pag2_soup:
                final_title = title_pag2_soup.find('header', attrs = 'page-header').find('h1').text.strip() if title_pag2_soup.find('header', attrs = 'page-header') else None
                            # A LUAT TITLUL

                # Adăugarea jobului în listă
                job_list.append(Item(
                    job_title = final_title,
                    job_link = link,
                    company = 'Inoveco',
                    country = 'Romania',
                    county = get_county('Ilfov'),
                    city = 'Ilfov',
                    remote = 'on-site',
                ).to_dict())

    return job_list


def main():

    company_name = "Inoveco"
    logo_link = "https://s.cdnmpro.com/438595266/logo.jpg?rv=1625477870"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

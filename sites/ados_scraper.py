# Company ---> ados
# Link ------> https://www.adosfresh.ro/cariera/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from ados scraper.

    soup = GetStaticSoup("https://www.adosfresh.ro/cariera/")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'vc_row wpb_row vc_inner vc_row-fluid'):
        title = job.find('h3').text.strip()
        if title == 'Agent achiziții și contractări cereale':
            city = ['Giurgiu', 'Alexandria', 'Voluntari', 'Calarasi', 'Slobozia', 'Braila', 'Iasi',
                    'Bacau', 'Suceava', 'Vaslui', 'Botosani']
        elif title == 'Manager depozit legume-fructe' or title == 'Mecanic întreținere și reparații utilaje':
            city = 'Crevedia'
        else:
            city = 'Pogoanele'

        # get jobs items from response
        job_list.append(Item(
            job_title = title,
            job_link = job.find('a')['href'],
            company= 'Ados',
            country = 'Romania',
            county = '',
            city = city,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "Ados"
    logo_link = "https://www.adosfresh.ro/wp-content/uploads/2023/10/logo-ados-footer-230.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

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

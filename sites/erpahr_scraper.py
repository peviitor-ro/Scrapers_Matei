# Company ---> erpahr
# Link ------> https://erpahr.ro/cariere

from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from erpahr scraper.

    soup = GetStaticSoup("https://erpahr.ro/cariere")
    job_list = []
    
    for job in soup.find_all('div', class_ = 'col-xs-12 col-md-6 col-lg-4 col-xl-3 mv-20'):
        city = []
        location_span = job.find('span', class_='pretitle')
        if location_span == "ROMANIA":
            next_sibling = location_span.find_next_sibling('span', class_='pretitle_separator')
            if next_sibling:
                locations_text = next_sibling.find_next_sibling('span', class_='pretitle').get_text(strip=True)
                locations = locations_text.split(', ')
                city = locations if locations else []

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('div', class_ = 'career_name').find('h4').text,
            job_link = 'https://erpahr.ro' + job.find('div', class_ = 'career_name').find('a')['href'],
            company = 'ErpaHR',
            country = 'Romania',
            county = '',
            city = city,
            remote = '',
        ).to_dict())

    return job_list


def main():

    company_name = "ErpaHR"
    logo_link = "https://erpahr.ro/assets/images/erpahr-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

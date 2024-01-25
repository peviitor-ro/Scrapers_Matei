# Company ---> boostuphr
# Link ------> https://www.boostuphr.com/jobs

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
from urllib.parse import quote


def scraper():

    # scrape data from boostuphr scraper.

    soup = GetStaticSoup("https://www.boostuphr.com/jobs")
    job_list = []
    
    for job in soup.find_all('div', attrs = {'role': 'listitem'}):

        get_link = job.find('a')['href']
        url = quote(get_link, safe = ':/')
        link_soup = GetStaticSoup(get_link)
        job_type = link_soup.find('div', attrs = {'id': 'comp-lo4aysd24'}).text.strip()
        get_city = job.find('p', class_ = 'font_8 wixui-rich-text__text').text.split(',')[0].strip()

        if get_city == "Romania":
            get_city = ''
        elif get_city == "Bucharest":
            get_city = 'Bucuresti'
        else: pass

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h2').text.strip(),
            job_link = url,
            company= 'Boost-upHr',
            country = 'Romania',
            county = get_county(get_city),
            city = get_city,
            remote = job_type,
        ).to_dict())

    return job_list


def main():

    company_name = "Boost-upHr"
    logo_link = "https://media.licdn.com/dms/image/D4D0BAQFyiT2xYTzMhQ/company-logo_200_200/0/1681885595294?e=1714003200&v=beta&t=6h4QKDND5EUv9LSL6n8F_1Rj_-gMNc21Ez0bG-YDpYE"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

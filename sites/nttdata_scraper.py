# Company ---> nttdata
# Link ------> https://careers.nttdata.ro/search/

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    job_list = []
    url_base = "https://careers.nttdata.ro/search/"
    url_extend = '&startrow={}&q=&sortColumn=referencedate&sortDirection=desc'

    soup = GetStaticSoup(url_base)

    pagination = soup.find('ul', class_='pagination')
    if pagination:
        num_pages = len(pagination.find_all('li')) - 2
    else:
        num_pages = 1

    for page_num in range(num_pages):
        url = url_base + url_extend.format(page_num * 25)
        soup = GetStaticSoup(url)

        for job in soup.find_all('tr', class_='data-row'):

            link = 'https://careers.nttdata.ro' + job.find('div', class_='jobdetail-phone visible-phone').find('a')['href']
            location_page = GetStaticSoup(link)
            location_list = []
            for cities in location_page.find_all('span', class_='jobGeoLocation'):
                location = cities.text.split(',')[0].strip()
                location_list.append(location)

            job_list.append(Item(
                job_title = job.find('div', class_='jobdetail-phone visible-phone').find('a').text.strip(),
                job_link = link,
                company = 'NTTData',
                country = 'Romania',
                county = '',
                city = location_list,
                remote = '',
            ).to_dict())

    return job_list


def main():

    company_name = "NTTData"
    logo_link = "https://www.top-employers.com/contentassets/e7e0f0e615164b519ee4078cea2304fe/oid00d200000000wi7ids0683y00000zgq1dda3y000003ckbet59nz1kmc6hv5aspvjjgbjvsi5rotn6y3n0qgvoogscaspdffalse5?quality=75&height=75&bgcolor=white"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()

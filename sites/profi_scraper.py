# Company ---> profi
# Link ------> https://www.profi.ro/rezultate-cautare-cariere/

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)
import requests


def prepare_post_request():

    url = "https://www.profi.ro/wp-admin/admin-ajax.php"

    headers = {
        'authority': 'www.profi.ro',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.profi.ro',
        'Referer': 'https://www.profi.ro/rezultate-cautare-cariere/',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    return url, headers

def scraper():

    # scrape data from profi scraper.

    # # # # # # # # # # # # # START PARTE STATIC GET # # # # # # # # # # # # #
    soup = GetStaticSoup("https://www.profi.ro/rezultate-cautare-cariere/")
    job_list = []

    rows = soup.find_all('tr')

    for job in rows[1:]:
        cells = job.find_all('td')
        get_title = cells[0].text.strip()
        get_city = cells[2].text.strip()

        last_cell = cells[-1]
        link = None
        if last_cell.find('a'):
            link = last_cell.find('a').get('href')

        # Adaugă locul de muncă la listă
        job_list.append(Item(
            job_title = get_title,
            job_link = link,
            company = 'Profi',
            country = 'Romania',
            county = get_county(get_city),
            city = get_city,
            remote = '',
        ).to_dict())

    # # # # # # # # # # # # # END PARTE STATIC GET # # # # # # # # # # # # #

    # # # # # # # # # # # # # START PARTE POST JSON # # # # # # # # # # # # #
    url, headers = prepare_post_request()
    session = requests.Session()
    offset = 1
    flag = True

    while flag:
        response = session.post(url=url, headers=headers, data={
            'data': '{"job_name":"","county_name":"","store_name":"","store_type":""}',
            'action': 'load_more_jobs',
            'nonce': '761c7d7e78',
            'page': offset,
            'posts_per_page': '10'
        })

        json_data = response.json()
        if offset < 20:
            offset += 1
            for job in json_data:
                job_list.append(Item(
                    job_title = job['job_title'],
                    job_link = job['job_url'],
                    company = 'Profi',
                    country = 'Romania',
                    county = get_county(job['job_city']),
                    city = job['job_city'],
                    remote = '',
                ).to_dict())
        else:
            flag = False
    # # # # # # # # # # # # # END PARTE POST JSON # # # # # # # # # # # # #

    return job_list


def main():

    company_name = "Profi"
    logo_link = "https://imgcdn.bestjobs.eu/cdn/el/plain/employer_logo/632020db719a5.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

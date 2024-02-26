# Company ---> GiGroup
# Link ------> https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca
import requests
from bs4 import BeautifulSoup
from __utils import (
    get_county,
    Item,
    UpdateAPI,
)


def prepare_post_request() -> tuple:

    # prepare post request for GiGroup.

    url = 'https://ro.gigroup.com/wp-content/themes/gi-group-child/job-search-infinite-scroll_ALL.php?fbclid=IwAR3Av5LpQV66NPEgVKJA7lVOO2JcW9ibjrRCvSa2UT5AX0rhBldAwOiptFE'

    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ro.gigroup.com',
        'Referer': 'https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    return url, headers


def scraper():

    # scrape data from GiGroup scraper.
    url, headers = prepare_post_request()
    session = requests.Session()

    # list with data
    job_list = []
    offset = 0
    flag = True

    while flag:
        response = session.post(url=url, headers=headers, data={
                "X_GUMM_REQUESTED_WITH": "XMLHttpRequest",
                "action": "scrollpagination",
                "numberLimit": "30",
                "offset": offset
            })

        # get data and add to offset
        json_data = BeautifulSoup(response.text, 'html.parser')
        data = len(json_data.find_all('article'))
        if data > 0:
            offset += 30
        else:
            flag = False
        # end

        for job in json_data.find_all('article', attrs={'class': 'workRow job-item-s'}):

            title = job.find('div', attrs={'class': 'titleBlock'}).find('h2').text
            location_divs = job.find('div', attrs={'class': 'span8'}).find_all('div', attrs={'class': 'workCol2'})[1].find('h3').text.split(',')[0].strip()
            if '-' in location_divs:
                location_clear = location_divs.split('-')[0].strip()
            else:
                location_clear = location_divs

            if location_clear == 'Cluj':
                location_clear = 'Cluj-Napoca'
            else: pass
            if title == 'Director Sucursala':
                location_clear = 'Mures'
            if title == 'Tehnician de calitate':
                location_clear = 'Pitesti'
            if title == 'Operator turnatorie':
                location_clear = 'Pitesti'

            # get jobs items from response
            job_list.append(Item(
                job_title = title,
                job_link = job.find('div', attrs={'class': 'titleBlock'}).find('a').get('href'),
                company = 'GiGroup',
                country = 'Romania',
                county = get_county(location_clear),
                city = location_clear,
                remote = 'on-site',
            ).to_dict())


    return job_list


def main():

    company_name = "GiGroup"
    logo_link = "https://w5b2c9z3.rocketcdn.me/wp-content/themes/gi-group/images/gi-group-child-logo@2x.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
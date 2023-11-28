# Company ---> GiGroup
# Link ------> https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca

from __utils import (
    PostRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def prepare_post_request() -> tuple:

    # prepare post request for GiGroup.

    url = 'https://ro.gigroup.com/wp-content/themes/gi-group-child/job-search-infinite-scroll_ALL.php?'

    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ro.gigroup.com',
        'Referer': 'https://ro.gigroup.com/oferta-noastra-de-locuri-de-munca',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    return url, headers


def scraper():

    # scrape data from GiGroup scraper.


    url, headers = prepare_post_request()

    # list with data
    job_list = []

    offset = 0
    flag = True

    while flag:
        json_data = PostRequestJson(url=url, custom_headers=headers, data_raw={
                "X_GUMM_REQUESTED_WITH": "XMLHttpRequest",
                "action": "scrollpagination",
                "numberLimit": 30,
                "offset": offset
            })

        # get data and add to offset
        data = len(json_data.find_all('article'))
        if data > 0:
            offset += 30
        else:
            flag = False
        # end

        for job in json_data.find_all('article', attrs={'class': 'workRow job-item-s'}):

            location_divs = job.find('div', attrs={'class': 'span8'}).find_all('div', attrs={'class': 'workCol2'})[1].find('h3').text.split(',')[0].strip()
            if '-' in location_divs:
                location_clear = location_divs.split('-')[0].strip()
            else:
                location_clear = location_divs

            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('div', attrs={'class': 'titleBlock'}).find('h2').text,
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

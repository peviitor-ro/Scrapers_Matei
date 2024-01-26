# Company ---> hnservices
# Link ------> https://www.hn-services.com/en/we-recruit/

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)
import requests
from bs4 import BeautifulSoup


def prepare_post_request():
    url = "https://www.hn-services.com/wp-admin/admin-ajax.php"
    headers = {
        "authority": "www.hn-services.com",
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "wp-wpml_current_language=en; cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-analytics=yes; _pk_ref.1.4904=^%^5B^%^22^%^22^%^2C^%^22^%^22^%^2C1706223895^%^2C^%^22https^%^3A^%^2F^%^2Fwww.google.com^%^2F^%^22^%^5D; _pk_id.1.4904=1be4e91a57ca4340.1706223895.; _pk_ses.1.4904=1",
        "origin": "https://www.hn-services.com",
        "referer": "https://www.hn-services.com/en/we-recruit/",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    return url, headers



def scraper():

    # scrape data from hnservices scraper.

    url, headers = prepare_post_request()
    job_list = []

    for offset in range(1, 3):
        data = {
            "action": "get_offres",
            "data[villes][]": "1472",
            "data[actualPage]": offset,
            "data[textSearch]": "",
            "data[postPerPage]": "12"
        }

        response = requests.post(url, headers=headers, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')

        for job in soup.find_all('div', class_ = 'card h-100 p-3'):
            get_city = job.find('ul', class_='list-inline ville').text.strip()
            if get_city:
                cities = [city.strip() for city in get_city.split(',')]
                bucharest = next((city for city in cities if city == "Bucharest"))
                if bucharest:
                    bucharest = "Bucuresti"

            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('h3').text.strip(),
                job_link = job.find('a')['href'],
                company='HNServices',
                country = 'Romania',
                county = get_county(bucharest),
                city = bucharest,
                remote='',
            ).to_dict())
        offset += 1

    return job_list


def main():

    company_name = "HNServices"
    logo_link = "https://www.hn-services.com/wp-content/themes/bootscore-5-child/img/logo/Hn-logo-40ans.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()

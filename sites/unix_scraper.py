# Company ---> unix
# Link ------> https://www.unixauto.ro/cariera/cautator

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import re


def get_raw_headers():
    url = "https://www.unixauto.ro/cariera/cautator"

    raw_headers = {
        "Authority": "www.unixauto.ro",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": "\"Not A(Brand)\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    return url, raw_headers

def get_token(url, headers):
    token_url = url
    token_headers = headers
    token_soup = GetStaticSoup(token_url, token_headers)
    token_input = token_soup.find('input', {'name': '__RequestVerificationToken'})
    token = token_input['value']

    return token

def get_headers(token):
    headers = {
        "authority": "www.unixauto.ro",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "cookie": f"_ga=GA1.1.2075285043.1703213117; LCookieConsentDismissed=True; CGuestToken=59f18500bdf94bb6afad9e5e5e7568d5; .AspNetCore.Antiforgery._JXGetjxs4c={token}; CUxClientResolution=1920x1080; CUxClientWindowSize=1920x953; CBrowserInfo=Chrome^%^20ver:^%^20121; LDriver=false; _ga_8TPXNB2JDY=GS1.1.1707309333.3.0.1707309333.60.0.0; _clck=100x120^%^7C2^%^7Cfj2^%^7C0^%^7C1498; _clsk=kwec8n^%^7C1707309334221^%^7C1^%^7C1^%^7Cd.clarity.ms^%^2Fcollect; _ga_45KFT6BZ94=GS1.1.1707309333.1.1.1707309344.0.0.0",
        "sec-ch-ua": "\"Not A(Brand)\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    return headers


def extract_addresses(text):
    matches = re.findall(r'\d{6}\s(.+?)\s(?:Sos|Str|Strada|Bd|1|Crangasi|Calea)', text)

    return matches

def scraper():
    url, raw_headers = get_raw_headers()
    token = get_token(url, raw_headers)
    headers = get_headers(token)

    soup = GetStaticSoup(url, custom_headers=headers)
    job_list = []

    for job in soup.find_all('a', class_='karrierjob'):
        orase = job.find('p', class_='karrierjob__p').text.strip()
        addresses = extract_addresses(orase)
        city_name = addresses_str = ', '.join(addresses)
        
        if city_name == 'Cluj Napoca':
            city_name = 'Cluj-Napoca'
        elif city_name == 'T\u00e2rgu Mures':
            city_name = 'Targu-Mures'

        job_list.append(Item(
            job_title=job.find('h3').text.strip(),
            job_link = 'https://www.unixauto.ro' + str(job.get('href')),
            company = 'Unix',
            country = 'Romania',
            county = '',
            city = city_name,
            remote = 'on-site',
        ).to_dict())

    return job_list


def main():

    company_name = "Unix"
    logo_link = "https://www.unixauto.ro/assets/images/UNIX_RO.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

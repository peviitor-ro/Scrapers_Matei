#  You can create your own scraper:
#  ... static
#  ... dynamic_json_get
#  ... dynamic_json_post
#  ... dynamic_render
#  ... custom
#
import sys
import os


#  ---------------------> STATIC SCRAPER <---------------------
def create_static_scraper_config(nume_scraper, link):
    config_content = f"""
# Company ---> {nume_scraper}
# Link ------> {link}

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from {nume_scraper} scraper.

    soup = GetStaticSoup("{link}")
    job_list = []
    
    for job in soup.find_all(...):

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Static scraper {nume_scraper.lower()}_scraper.py was succesfully created!')


#  ---------------------> DYNAMIC JSON GET <---------------------
def create_dynamic_json_get_scraper_config(nume_scraper, link):
    config_content = f"""
# Company ---> {nume_scraper}
# Link ------> {link}

from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from {nume_scraper} scraper.

    json_data = GetRequestJson("{link}")
    job_list = []
    
    for job in json_data['key']:

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Scraper type: dynamic_json_get {nume_scraper.lower()}_scraper.py was successfully created!')


#  ---------------------> DYNAMIC JSON POST <---------------------
def create_dynamic_json_post_scraper_config(nume_scraper, link):
    config_content = f"""
# Company ---> {nume_scraper}
# Link ------> {link}

from __utils import (
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from {nume_scraper} scraper.

    json_data = PostRequestJson("{link}", custom_headers=headers, data=data_row)

    job_list = []
    for job in json_data['key']:
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Scraper type: dynamic_json_post {nume_scraper.lower()}_scraper.py was successfully created!')


#  ---------------------> DYNAMIC RENDER <---------------------
def create_dynamic_render_scraper_config(nume_scraper, link):
    config_content = f"""
# Company ---> {nume_scraper}
# Link ------> {link}

from __utils import (
    GetDynamicSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from {nume_scraper} scraper.

    soup = GetDynamicSoup("{link}")

    job_list = []
    for job in soup.find_all(...):
        pass

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Scraper type: dynamic_render {nume_scraper.lower()}_scraper.py was successfully created!')


#  ---------------------> CUSTOM SCRAPER <---------------------
def create_custom_scraper_config(nume_scraper, link):
    config_content = f"""
# Company ---> {nume_scraper}
# Link ------> {link}

from __utils import Item
import requests
from bs4 import BeautifulSoup
# from requests_html import HTMLSession


def scraper():

    # scrape data from {nume_scraper} scraper.

    job_list = []
    
    for job in []:
    
        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='{nume_scraper}',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())


def main():

    company_name = "{nume_scraper}"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
"""

    with open(f'{nume_scraper.lower()}_scraper.py', 'w') as f:
        f.write(config_content)
    print(f'Custom scraper {nume_scraper.lower()}_scraper.py was successfully created!')


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 create_scraper.py \"nume_scraper\" \"link\" \"static/dynamic_json_get/dynamic_json_post/dynamic_render/custom\"")
    else:
        nume_scraper = sys.argv[1]
        link = sys.argv[2]
        scraper_type = sys.argv[3]

        # Verificați dacă fișierul scraper există deja sau nu
        if os.path.exists(f'{nume_scraper.lower()}_scraper.py'):
            print(f"File {nume_scraper.lower()}_scraper.py already exists!")
        else:
            if scraper_type == 'static':
                create_static_scraper_config(nume_scraper, link)
            elif scraper_type == 'dynamic_json_get':
                create_dynamic_json_get_scraper_config(nume_scraper, link)
            elif scraper_type == 'dynamic_json_post':
                create_dynamic_json_post_scraper_config(nume_scraper, link)
            elif scraper_type == 'dynamic_render':
                create_dynamic_render_scraper_config(nume_scraper, link)
            elif scraper_type == 'custom':
                create_custom_scraper_config(nume_scraper, link)
            else:
                print("Type of scraper needs to be 'static', 'dynamic_json_get', 'dynamic_json_post', 'dynamic_render' or 'custom'.")

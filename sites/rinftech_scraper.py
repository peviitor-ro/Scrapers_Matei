# Company ---> rinftech
# Link ------> https://jobs.rinf.tech/jobs/Careers

from __utils import (
    GetDynamicSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from rinftech scraper.

    soup = GetDynamicSoup("https://jobs.rinf.tech/jobs/careers")
    job_list = []

    for job in soup.find_all('div', class_='cw-filter-joblist'):

        city = job.find('p', class_='filter-subhead cw-bw').text.split(',')[0].strip()
        if city == 'Guadalajara':
            continue
        elif city == 'Remote':
            remote_text = 'remote'
            city = ''
        else:
            remote_text = ''

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('h3').text.strip(),
            job_link=job.find('a')['href'],
            company='rinf.tech',
            country='Romania',
            county='',
            city=city,
            remote=remote_text,
        ).to_dict())

    return job_list


def main():

    company_name = "rinf.tech"
    logo_link = "https://stagiipebune.ro/media/cache/f0/60/f060b0a01bd022e9c28f3073cb5404bb.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

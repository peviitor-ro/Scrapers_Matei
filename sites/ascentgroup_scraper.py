from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    #  scrape data from ascentgroup scraper.

    soup = GetStaticSoup("https://www.ascentjobs.ro/lista-joburi/")
    job_list = []

    for job in soup.find_all('div', attrs = {'class': 'job-list'}):

        city = job.find('span', attrs = {'class': 'office-location'}).text
        if city == 'Chișineu Criș':
            city = 'Chisineu Cris'
        if city == 'Timișoara':
            city = 'Timisoara'

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').text,
            job_link = job.find('h4').find('a')['href'],
            company = 'AscentGroup',
            country = 'Romania',
            county = get_county(city),
            city = city,
            remote = get_job_type(job.find_all('span', attrs = {'class': 'job-type part-time'})[-1].text),
        ).to_dict())

    return job_list


def main():

    company_name = "AscentGroup"
    logo_link = "https://assets2.ghidul.ro/media/foto_video/11/268/27585/foto/crop/4382711.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

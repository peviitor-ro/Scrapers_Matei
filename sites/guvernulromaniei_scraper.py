# Company ---> GuvernulRomaniei
# Link ------> https://posturi.gov.ro/

from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)

from __utils.found_county import find_cities_from_county_in_string, remove_diacritics, find_best_city_match


def scraper():

    # scrape data from guvernulromaniei scraper.

    job_list = []
    base_url = "https://posturi.gov.ro/page/"

    #determine last page number to fetch
    soup = GetStaticSoup(base_url)
    span_tag = soup.find('span', class_='page-numbers dots')
    a_tag = span_tag.find_next_sibling('a', class_='page-numbers')
    max_page = int(a_tag.text)

    for page_number in range(max_page, 1, -1):
        url = base_url + str(page_number)
        soup = GetStaticSoup(url)

        for job in soup.find_all('article', class_ = 'box'):
            county = remove_diacritics(job.find('div', class_ = 'locatie').text.strip())
            angajator_text = job.find('div', class_='angajator').text.strip()

            # get jobs items from response
            job_list.append(Item(
                job_title = job.find('div', class_ = 'title').find('a').text.strip(),
                job_link = job.find('div', class_ = 'title').find('a')['href'],
                company = 'GuvernulRomaniei',
                country = 'Romania',
                county = county,
                city = find_best_city_match(county, find_cities_from_county_in_string(county, remove_diacritics(angajator_text).lower())), #WARNING, not perfect, depends on city name being present in short job description, which most are, but not all, eg: https://posturi.gov.ro/anunt/ingrijitor-1486/ Alternative would be to open job page itself and try to find city from there.. too complicated for me
                remote = 'on-site' if county else 'remote',
            ).to_dict())

    return job_list


def main():

    company_name = "GuvernulRomaniei"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHuEEV_LDvi5RpRoyxZYAX2InVXfC2Kzq1cQ&usqp=CAU"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

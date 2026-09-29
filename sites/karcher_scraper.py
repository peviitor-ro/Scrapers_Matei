# Company ---> karcher
# Link ------> https://careers.kaercher.com/search/?searchby=location&locationsearch=Romania

import re

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)

SEARCH_URL = (
    "https://careers.kaercher.com/search/"
    "?searchby=location&locationsearch=Romania"
    "&sortColumn=referencedate&sortDirection=desc"
)
BASE_URL = "https://careers.kaercher.com"
PAGE_SIZE = 50
MAX_PAGES = 50


def parse_location(location):
    # location looks like: "Voluntari, RO, 077191"
    city = location.split(",")[0].strip()
    if not city or city.upper() in {"RO", "ROMANIA"}:
        return None, None
    return city, get_county(city)


def parse_total(soup):
    # pagination label looks like: "Results 1 – 50 of 290"
    label = soup.find("span", class_="paginationLabel")
    if not label:
        return None

    match = re.search(
        r"Results\s*(\d+)\s*[–-]\s*(\d+)\s*of\s*(\d+)",
        label.get_text(" ", strip=True),
    )
    if not match:
        return None

    _, end, total = (int(group) for group in match.groups())
    return total, end


def scraper():

    # scrape data from karcher scraper.

    job_list = []
    startrow = 0

    for _ in range(MAX_PAGES):
        url = f"{SEARCH_URL}&startrow={startrow}" if startrow else SEARCH_URL
        soup = GetStaticSoup(url)
        rows = soup.find_all("tr", class_="data-row")
        if not rows:
            break

        for row in rows:
            link = row.find("td", class_="colTitle")
            link = link.find("a", class_="jobTitle-link") if link else None
            if not link:
                continue

            location_tag = row.find("td", class_="colLocation")
            location_tag = location_tag.find("span", class_="jobLocation") if location_tag else None
            if not location_tag:
                location_tag = row.find("span", class_="jobLocation")

            location = location_tag.text.strip() if location_tag else ""
            city, county = parse_location(location)

            job_link = link["href"]
            if job_link.startswith("/"):
                job_link = BASE_URL + job_link

            # get jobs items from response
            job_list.append(Item(
                job_title=link.text.strip(),
                job_link=job_link,
                company="Karcher",
                country="Romania",
                county=county,
                city=city,
                remote="on-site",
            ).to_dict())

        pagination = parse_total(soup)
        if not pagination:
            break

        total, last_row = pagination
        startrow += max(last_row - startrow, len(rows))
        if startrow >= total:
            break

    return job_list


def main():

    company_name = "Karcher"
    logo_link = "https://s1.kaercher-media.com/versions/2023.22.1/static/img/kaercher_logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

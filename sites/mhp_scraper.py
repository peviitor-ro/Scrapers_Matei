#
# Company ---> mhp
# Link ------> https://jobs.mhp.com/index.php?ac=search_result&search_criterion_country%5B%5D=176&search_criterion_physical_location%5B%5D=141

from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():

    # scrape data from mhp scraper.

    json_data = GetRequestJson(
"https://porsche-beesite-production-gjb-mhp.app.beesite.de/search/?data=%7B%22LanguageCode%22%3A%22EN%22%2C%22SearchParameters%22%3A%7B%22FirstItem%22%3A1%2C%22CountItem%22%3A250%2C%22Sort%22%3A%5B%7B%22Criterion%22%3A%22PublicationStartDate%22%2C%22Direction%22%3A%22DESC%22%7D%5D%2C%22MatchedObjectDescriptor%22%3A%5B%22ID%22%2C%22PositionTitle%22%2C%22PositionURI%22%2C%22PositionShortURI%22%2C%22PositionLocation.CountryName%22%2C%22PositionLocation.CityName%22%2C%22PositionLocation.Longitude%22%2C%22PositionLocation.Latitude%22%2C%22PositionLocation.PostalCode%22%2C%22PositionLocation.StreetName%22%2C%22PositionLocation.BuildingNumber%22%2C%22PositionLocation.Distance%22%2C%22JobCategory.Name%22%2C%22PublicationStartDate%22%2C%22ParentOrganizationName%22%2C%22ParentOrganization%22%2C%22OrganizationShortName%22%2C%22CareerLevel.Name%22%2C%22JobSector.Name%22%2C%22PositionIndustry.Name%22%2C%22PublicationCode%22%2C%22PublicationChannel.Id%22%5D%7D%2C%22SearchCriteria%22%3A%5B%7B%22CriterionName%22%3A%22PositionLocation.Country%22%2C%22CriterionValue%22%3A%5B%22176%22%5D%7D%2C%7B%22CriterionName%22%3A%22PositionLocation.City%22%2C%22CriterionValue%22%3A%5B%22141%22%5D%7D%2C%7B%22CriterionName%22%3A%22PublicationChannel.Code%22%2C%22CriterionValue%22%3A%5B%2288%22%5D%7D%5D%7D")
    job_list = []

    for job in json_data['SearchResult']['SearchResultItems']:
        position = job['MatchedObjectDescriptor']

        if 'PositionLocation' in position:
            locations = position['PositionLocation']

            for location in locations:

                loc = location['CityName']
                if loc == 'Cluj':
                    loc = 'Cluj-Napoca'

                job_list.append(Item(
                    job_title = position['PositionTitle'],
                    job_link = position['PositionURI'],
                    company = 'MHP',
                    country = location['CountryName'],
                    county = get_county(loc),
                    city = loc,
                    remote = 'on-site',
                ).to_dict())

    return job_list


def main():

    company_name = "MHP"
    logo_link = "https://media.licdn.com/dms/image/D4E0BAQGkhY-B-x106w/company-logo_200_200/0/1688371955964/mhp_a_porsche_company_logo?e=2147483647&v=beta&t=olxJjJ7V96H7qa5aiSdt7kWzinxAGGG7gEXfcP2aX9k"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()

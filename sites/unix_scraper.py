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


def extract_city_name(text):
    coduri_postale = re.findall(r'\b\d{6}\b', text)

    if coduri_postale:
        for cod in coduri_postale:
            index_cod = text.find(cod)                              # COD POSTAL
            rest_text = text[index_cod + len(cod):] if index_cod != -1 else None

            if rest_text:
                cuvinte_dupa_cod = rest_text.split()
                if len(cuvinte_dupa_cod) >= 2:
                    primele_doua_cuvinte = " ".join(
                        cuvinte_dupa_cod[:2])                       # PRIMELE 2 CUV DUPA COD

                if get_county(primele_doua_cuvinte) is None:
                    index_ultimul_spatiu = primele_doua_cuvinte.rfind(" ")  # VERIFIC DACA E OK ORASUL

                    if index_ultimul_spatiu != -1:
                        ultimul_cuvant_pana_la_spatiu = primele_doua_cuvinte[
                                                        :index_ultimul_spatiu]
                        return ultimul_cuvant_pana_la_spatiu


def scraper():
    soup = GetStaticSoup("https://www.unixauto.ro/cariera/cautator")
    job_list = []

    for job in soup.find_all('a', class_='karrierjob'):
        orase = job.find('p', class_='karrierjob__p').text.strip()

        # Use extract_city_name function to get the city name
        nume_oras = extract_city_name(orase)

        job_list.append(Item(
            job_title=job.find('h3').text.strip(),
            job_link = 'https://www.unixauto.ro' + str(job.get('href')),
            company = 'Unix',
            country = 'Romania',
            county = '',
            city = nume_oras,
            remote='',
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

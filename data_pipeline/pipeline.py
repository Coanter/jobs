import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

def main():
    # 1. Собрать данные
    soup_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://bishkek.headhunter.kg/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&enable_snippets=false&L_save_area=true&page=0'

    for i in range(40):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        soup_list.append(soup)

    vacancies = []
    for item in soup_list:
        vacancies += item.find_all('div', class_='vacancy-info--ieHKDTkezpEj0Gsx')

    # 2. Обработать данные
    vacancy_titles = []
    salaries = []
    experience_list = []
    company_names = []
    cities = []

    for item in vacancies:
        # Название вакансии
        title_span = item.find('span', {'data-qa': 'serp-item__title-text'})
        if title_span:
            vacancy_titles.append(title_span.get_text(strip=True()))
        
        # Зарплата
        salary_span = item.find('span', class_='magritte-text___pbpft_3-0-20 magritte-text_style-primary___AQ7MW_3-0-20 magritte-text_typography-label-1-regular___pi3R-_3-0-20')
        if salary_span:
            salary_text = salary_span.get_text(strip=True).replace('\u202f', '')
            formatted_salary = (
                salary_text
                .replace('₽', ' ₽')
                .replace('₸', ' ₸')
                .replace('до', ' до ')
                .replace('от', 'от ')
                .replace('на руки', ' на руки')
                .replace('до вычета налогов', ' до вычета налогов')
            )
            salaries.append(formatted_salary)
        else:
            salaries.append('Не указана')
        
        # Опыт
        experience_div = item.find('div', class_='magritte-tag__label___YHV-o_3-0-23')
        if experience_div:
            experience_span = experience_div.find('span')
            if experience_span:
                experience_text = experience_span.get_text(strip=True)
                experience_list.append(experience_text)

        # Название компании
        company_span = item.find('span', {'data-qa': 'vacancy-serp__vacancy-employer-text'})
        if company_span:
            company_names.append(company_span.get_text(strip=True))
        
        # Город
        city_span = item.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
        if city_span:
            city_text = city_span.get_text(strip=True)
            cities.append(city_text)

    # 3. Сохранить данные в CSV
    df = pd.DataFrame(
        {
        'title': vacancy_titles,
        'salary': salaries,
        'experience': experience_list,
        'company': company_names,
        'city': cities
        }
    )
    df.to_csv('head_hunter.csv', index=False)

    # 4. Сохранить данные в SQLite
    conn = sqlite3.connect('vacancies.db')
    df.to_sql('vacancies', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    main()





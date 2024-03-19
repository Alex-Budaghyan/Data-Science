import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup


def write_in_file(soup, writer):
    job_items = soup.find_all(class_="web_item_card hs_job_list_item")

    rows = []
    for job_item in job_items:
        title = job_item.find(class_="font_bold").text.replace('\n', '').strip()
        company = job_item.find(class_='job_list_company_title').text.replace('\n', '').strip()
        deadline = job_item.find(class_='formatted_date').text.replace('\n', '').strip()
        location = job_item.find(class_='job_location').text.replace('\n', '').strip()
        rows.append([title, company, deadline, location])

    writer.writerows(rows)


def scrap_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_doc = response.text
        return BeautifulSoup(html_doc, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(e)
        return


def scrape_with_selenium(url, header):
    driver = webdriver.Edge()
    try:
        driver.get(url)
        categories = driver.find_elements(By.CLASS_NAME, 'hs_nav_link')
        if categories:
            categories[0].click()
            time.sleep(1)

            with open('staff_data.csv', 'w', encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)

                while True:
                    soup = scrap_data(driver.current_url)
                    if soup:
                        write_in_file(soup, writer)
                    else:
                        break

                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, '.pagination .next a')
                        next_button.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        print("Next button not found. Exiting loop.")
                        break
        else:
            print("No categories found.")
    finally:
        driver.quit()


if __name__ == '__main__':
    base_url = 'https://staff.am/en/'
    header = ['Job name', 'Company', 'Deadline', 'Location']

    scrape_with_selenium(base_url, header)

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def send_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(e)


def scrape_page(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    important_info = soup.find_all("div", class_='card-body')

    data = []
    for info in important_info:
        title = info.find("a", class_="title").text
        description = info.find('p', class_="description card-text").text
        price = info.find('h4', class_='float-end price card-title pull-right').text
        num_of_review = info.find('p', class_='float-end review-count').text[0]
        rating_div = info.find('div', class_='ratings')
        p_in_div = rating_div.find_all("p")
        rating = len(p_in_div[1].find_all('span'))
        data.append([title, description, price, num_of_review, rating])

    return data


def create_dataframe(data, gadget, category):
    df = pd.DataFrame(data, columns=['Title', 'Description', 'Price', 'Review_Count', 'Rating'])
    df['Gadget'] = gadget
    df['Type'] = category
    return df


driver = webdriver.Chrome()

try:
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    page_source = send_request(url)
    main_page_data = scrape_page(page_source)
    main_page_df = create_dataframe(main_page_data, "Main Page", "All Items")
    all_data_df = pd.DataFrame()
    driver.get(url)
    time.sleep(30)

    sidebar_items = driver.find_elements(By.CSS_SELECTOR, '#side-menu > li.nav-item')[1:]

    for sidebar_item in sidebar_items:
        gadget = sidebar_item.text.strip()
        sidebar_item.click()
        time.sleep(2)


        categories = driver.find_elements(By.CSS_SELECTOR, '.sidebar .active .nav-item')

        for category in categories:
            category_name = category.text.strip()
            category.click()
            time.sleep(2)
            category_page_data = scrape_page(driver.page_source)
            category_df = create_dataframe(category_page_data, gadget, category_name)
            all_data_df = pd.concat([all_data_df, category_df], ignore_index=True)
            driver.back()
        driver.back()

    final_df = pd.concat([main_page_df, all_data_df], ignore_index=True)
    final_df.to_csv("Scraped_Data.txt", index=False)

finally:
    driver.quit()


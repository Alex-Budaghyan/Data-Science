import requests
from bs4 import BeautifulSoup


def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_='thumbnail')
        scraped_data = []
        for item in items:
            name = item.find('a', class_='title').text.strip()
            price = item.find('h4', class_='price').text.strip()
            description = item.find('p', class_='description').text.strip()
            reviews = item.find('div', class_='ratings').find('p').text.strip()
            scraped_data.append({'Name': name, 'Price': price, 'Description': description, 'Reviews': reviews})

        return scraped_data

    except requests.exceptions.RequestException as e:
        print("Error fetching webpage:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def save_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            for item in data:
                f.write(f"Name: {item['Name']}\n")
                f.write(f"Price: {item['Price']}\n")
                f.write(f"Description: {item['Description']}\n")
                f.write(f"Reviews: {item['Reviews']}\n\n")
    except Exception as e:
        print("Error saving data to file:", e)


if __name__ == "__main__":
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    filename = "data.txt"

    scraped_data = scrape_data(url)

    if scraped_data:
        save_to_file(scraped_data, filename)

import requests


def fetch_wikipedia_page(title):
    try:
        url = f"https://en.wikipedia.org/wiki/{title}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as r:
        return f"Error fetching Wikipedia page {title}"


title = input("Enter the title of Wikipedia page: ")
content = fetch_wikipedia_page(title)
print(content)


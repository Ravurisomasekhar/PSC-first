import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(str)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            text = soup.get_text()
            self.index[url] = text

            base_url = base_url or url
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(base_url, link['href'])
                self.crawl(absolute_url, base_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        return [url for url, content in self.index.items() if keyword.lower() in content.lower()]

    def print_results(self, results):
        if not results:
            print("No results found.")
        else:
            print("Search results:")
            for url in results:
                print(f"- {url}")  # ✅ Use f-string for a single string


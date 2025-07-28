import unittest
from unittest.mock import patch, MagicMock
from main import WebCrawler  # ✅ This is now correct
import requests

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.index)
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")
        crawler = WebCrawler()
        crawler.crawl("https://bad-url.com")

        self.assertIn("https://bad-url.com", crawler.visited)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "Nothing here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    @patch('builtins.print')
    def test_print_results(self, mock_print):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])
        mock_print.assert_any_call("Search results:")
        mock_print.assert_any_call("- https://test.com/result")

    @patch('builtins.print')
    def test_print_no_results(self, mock_print):
        crawler = WebCrawler()
        crawler.print_results([])
        mock_print.assert_called_with("No results found.")

if __name__ == "__main__":
    unittest.main()

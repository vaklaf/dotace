import unittest
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.library.downloader.downloader import rewrite_url


class TestRewriteUrl(unittest.TestCase):
    def test_rewrite_url_with_new_query(self):
        url = "http://example.com/path?param1=value1&param2=value2"
        new_query = {"param3": "value3", "param4": "value4"}
        expected_url = "http://example.com/path?param1=value1&param2=value2&param3=value3&param4=value4"
        result = rewrite_url(url,new_query= new_query)
        self.assertEqual(result, expected_url)

    def test_rewrite_url_without_new_query(self):
        url = "http://example.com/path?param1=value1&param2=value2"
        expected_url = "http://example.com/path?param1=value1&param2=value2"
        result = rewrite_url(url)
        self.assertEqual(result, expected_url)
        
    def test_rewrite_url_in_cls_zlk_region_context(self):
        url = "https://zlinskykraj.cz/archiv-dotaci?f-year=2021"
        new_query = {'f-year':2023,'page':10}
        expected_url = "https://zlinskykraj.cz/archiv-dotaci?f-year=2023&page=10"
        result = rewrite_url(url, new_query= new_query)
        self.assertEqual(result, expected_url)
        
    def test_rewrite_url_new_scheme(self):
        url = "http://example.com/path?param1=value1&param2=value2"
        expected_url = "https://example.com/path?param1=value1&param2=value2"
        result = rewrite_url(url, new_scheme="https")
        self.assertEqual(result, expected_url)
        
    def test_rewrite_url_new_netloc(self):
        url = "http://example.com/path?param1=value1&param2=value2"
        expected_url = "http://newdomain.com/path?param1=value1&param2=value2"
        result = rewrite_url(url, new_netloc="newdomain.com")
        self.assertEqual(result, expected_url)
        
    def test_rewrite_url_new_path(self):
        url = "http://example.com/path?param1=value1&param2=value2"
        expected_url = "http://example.com/newpath?param1=value1&param2=value2"
        result = rewrite_url(url, new_path="/newpath")
        self.assertEqual(result, expected_url)
        
    def test_rewrite_url_new_fragment(self):
        url = "http://example.com/path?param1=value1&param2=value2#oldfragment"
        expected_url = "http://example.com/path?param1=value1&param2=value2#newfragment"
        result = rewrite_url(url, new_fragment="newfragment")
        self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
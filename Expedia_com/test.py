import unittest
from .main import Spider
from dragline.http import Request


class SpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = Spider()

    # def test_parse(self):
    #     response = Request("http://www.example.org").send()
    #     data = list(self.spider.parse(response))
    #     self.assertDictEqual({'name': 'Example Domain', 'url': 'http://www.example.org'}, dict(data[0]))


if __name__ == '__main__':
    unittest.main()
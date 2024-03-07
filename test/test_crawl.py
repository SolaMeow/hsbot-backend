import unittest
import asynctest
from unittest.mock import patch
import sys
import os
import aiohttp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crawl.crawl import total_page, fetch_page

class TestCrawl(asynctest.TestCase):
    @patch('aiohttp.ClientSession.get', new_callable=asynctest.CoroutineMock)
    async def test_total_page(self, mock_get):
        async def get_text():
            return '{"leaderboard":{"pagination":{"totalPages":10}}}'  # 修改这里

        mock_response = asynctest.CoroutineMock()
        mock_response.text = get_text
        mock_get.return_value.__aenter__.return_value = mock_response
        headers = {'User-Agent': 'my-app/0.0.1'}
        async with aiohttp.ClientSession() as session:
            result = await total_page(session, 'http://example.com', headers)
        self.assertEqual(result, 10)

    @patch('aiohttp.ClientSession.get', new_callable=asynctest.CoroutineMock)
    async def test_fetch_page(self, mock_get):
        async def get_text():
            return '{"leaderboard":{"rows":[{"rank":1,"accountid":"test"}]}}'  # 修改这里

        mock_response = asynctest.CoroutineMock()
        mock_response.text = get_text
        mock_get.return_value.__aenter__.return_value = mock_response
        headers = {'User-Agent': 'my-app/0.0.1'}
        async with aiohttp.ClientSession() as session:
            result = await fetch_page(session, 'http://example.com', headers)
        self.assertEqual(result, [(1, 'test')])

if __name__ == '__main__':
    unittest.main()
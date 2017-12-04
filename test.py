import unittest
import requests

BASE_URL = 'http://localhost:8000/'

class TestPrestoServer(unittest.TestCase):

    def test_root_posting_not_allowed(self):
        post = requests.post(BASE_URL, data='some data')
        self.assertEqual(post.status_code, 400, 'Posting to a directory is not allowed')

    def test_relative_posting_not_allowed(self):
        post = requests.post(BASE_URL + '../file', data='some data')
        self.assertEqual(post.status_code, 400, 'Posting to a relative directory is not allowed')        

    def test_relative_getting_not_allowed(self):
        post = requests.post(BASE_URL + '../file', data='some data')
        self.assertEqual(post.status_code, 400, 'Getting a relative directory is not allowed')        

    def test_nested_path(self):
        post = requests.post(BASE_URL + 'b/c/d', data='data in nested file')
        self.assertEqual(post.status_code, 201, 'Creating a file results in 201')

    def test_get_posted_data_gets_it_back(self):
        post = requests.post(BASE_URL + 'file1', data='data in file1')
        self.assertEqual(post.status_code, 201, 'Creating a file results in 201')

        post = requests.post(BASE_URL + 'file2', data='data in file2')
        self.assertEqual(post.status_code, 201, 'Creating a file results in 201')

        get = requests.get(BASE_URL + 'file1')
        self.assertEqual(get.status_code, 200, 'Getting a file is OK')
        self.assertEqual(get.text, 'data in file1', 'Getting file1 should return file1')

if __name__ == '__main__':
    unittest.main()

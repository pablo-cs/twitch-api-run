import unittest
import sys

sys.path.append('../')  # imports from the parent directory (twitch-api-run)
from app.routes import app  # imports flask app object

class RoutesTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_search_page(self):
        response = self.app.post('/search', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_page(self):
        response = self.app.post('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_fav_page(self):
        response = self.app.get('/view_fav', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_pop_page(self):
        response = self.app.get('/view_pop', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_remove_page(self):
        response = self.app.post('/remove', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

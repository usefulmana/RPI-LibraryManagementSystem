import unittest
from search_service import Search


class TestSum(unittest.TestCase):
    def test_book_search(self):
        search = Search.get_instance()
        result = search.search_books("gone")
        self.assertEqual(result, [
            {
                "ISBN": "1",
                "author": "Scarlet",
                "id": 1,
                "published_date": "2017-05-05",
                "title": "Gone with the Wind"
            }
        ])

    def test_check_book_exist(self):
        search = Search.get_instance()
        result = search.check_book_exist(1)
        self.assertEqual(result, {
            "ISBN": "1",
            "author": "Scarlet",
            "id": 1,
            "published_date": "2017-05-05",
            "title": "Gone with the Wind"
        })


if __name__ == '__main__':
    unittest.main()

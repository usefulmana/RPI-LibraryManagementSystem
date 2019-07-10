import unittest
from return_service import ReturnService


class TestReturnService(unittest.TestCase):
    def test_get_list_of_undue_books(self):
        return_service = ReturnService.get_instance()
        result = return_service.get_list_of_undue_books('nlbasni2010@gmail.com', "Alex")
        self.assertEqual(result, [
            {
                "book_id": 5,
                "borrow_date": "2019-07-10",
                "borrow_status": "borrowed",
                "due_date": "2019-07-17",
                "id": 18,
                "return_date": None,
                "return_status": None,
                "user_id": 1
            }
        ])

    def test_check_if_book_exist_in_borrow_history(self):
        return_service = ReturnService.get_instance()
        result = return_service.check_if_book_exist_in_borrow_history(18, return_service.get_list_of_undue_books(
            'nlbasni2010@gmail.com', "Alex"))
        self.assertTrue(result, msg="Should be True")


if __name__ == '__main__':
    unittest.main()

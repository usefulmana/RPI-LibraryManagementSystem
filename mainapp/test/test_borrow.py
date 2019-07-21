import unittest
from borrow_service import BorrowService


class TestBorrow(unittest.TestCase):
    def test_get_user_id_from_email(self):
        borrow = BorrowService()
        result = borrow.get_user_id_from_email("nlbasni2010@gmail.com", "Alex")
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
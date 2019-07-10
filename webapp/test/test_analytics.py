from analytics import Analytics
import mysql.connector
import unittest


class Test(unittest.TestCase):

    def test_get_statistics_for_a_day(self, filename):
        try:
            my_database = mysql.connector.connect(
                host=self._host,
                database=self._database,
                user=self._user,
                passwd=self._password
            )
            if my_database.is_connected():
                cursor = my_database.cursor()
                sql1 = "SELECT COUNT(id) from borrowed_books where borrow_status = 'borrowed' and borrow_date = current_date"
                cursor.execute(sql1)
                result1 = cursor.fetchone()
                sql2 = "SELECT COUNT(id) from borrowed_books where return_status = 'returned' and borrow_date = current_date"
                cursor.execute(sql2)
                result2 = cursor.fetchone()
                sql3 = "SELECT current_date from borrowed_books"
                cursor.execute(sql3)
                result3 = cursor.fetchone()
                final_result = {"date": result3[0], "borrow": result1[0], "return": result2[0]}
                with open(filename, 'w+', newline='') as daily_report:
                    writer = csv.writer(daily_report)
                    writer.writerow(["date", "borrows", "returns"])
                    writer.writerow([final_result['date'], final_result["borrow"], final_result["return"]])
                    daily_report.close()
        except Exception as e:
            print(e)
        finally:
            my_database.close()


if __name__ == '__main__':
    unittest.TestCase()
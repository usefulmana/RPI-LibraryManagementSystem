import mysql.connector
from config_parser import Parser
import csv


class Analytics:
    _instance = None

    @staticmethod
    def get_instance():
        if Analytics._instance is None:
            Analytics()
        return Analytics._instance

    def __init__(self):
        if Analytics._instance is not None:
            raise Exception("This is a singleton class")
        else:
            """Enter your own info here"""
            Analytics._instance = self
            self.parser = Parser.get_instance()
            self._host = self.parser.host
            self._user = self.parser.user
            self._password = self.parser.password
            self._database = self.parser.database

    def get_statistics_for_a_day(self):
        try:
            my_database = mysql.connector.connect(
                host=self._host,
                database=self._database,
                user=self._user,
                passwd=self._password
            )
            if my_database.is_connected():
                cursor = my_database.cursor()
                sql1 = "SELECT COUNT(id) from borrowed_books where status = 'borrowed' and borrow_date = current_date"
                cursor.execute(sql1)
                result1 = cursor.fetchone()
                sql2 = "SELECT COUNT(id) from borrowed_books where status = 'returned' and borrow_date = current_date"
                cursor.execute(sql2)
                result2 = cursor.fetchone()
                sql3 = "SELECT current_date from borrowed_books"
                cursor.execute(sql3)
                result3 = cursor.fetchone()
                final_result = {"date": result3[0], "borrow": result1[0], "return": result2[0]}
                with open('daily.csv', 'w+', newline='') as daily_report:
                    writer = csv.writer(daily_report)
                    writer.writerow(["date", "borrows", "returns"])
                    writer.writerow([final_result['date'], final_result["borrow"], final_result["return"]])
                    daily_report.close()
        except Exception as e:
            print(e)
        finally:
            my_database.close()

    def get_statistics_for_a_week(self):
        try:
            my_database = mysql.connector.connect(
                host=self._host,
                database=self._database,
                user=self._user,
                passwd=self._password
            )
            if my_database.is_connected():
                cursor = my_database.cursor()
                sql1 = "select borrow_date as date, count(`id`) as count from borrowed_books where status = 'borrowed' group by borrow_date order by borrow_date desc limit 7"
                cursor.execute(sql1)
                result1 = cursor.fetchall()
                print(result1)
                sql2 = "select count(`id`) as count from borrowed_books where status = 'returned' group by borrow_date order by borrow_date desc limit 7"
                cursor.execute(sql2)
                result2 = cursor.fetchall()
                print(result2)
                # final_result = {"borrow": result1[0], "return": result2[0]}
                # with open('weekly.csv', 'w+', newline='') as weekly_report:
                #     writer = csv.writer(weekly_report)
                #     writer.writerow(["borrows", "returns"])
                #     writer.writerow([final_result["borrow"], final_result["return"]])
                #     weekly_report.close()
        except Exception as e:
            print(e)
        finally:
            my_database.close()


if __name__ == '__main__':
    anal = Analytics.get_instance()
    # anal.get_statistics_for_a_day()
    anal.get_statistics_for_a_week()

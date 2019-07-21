import mysql.connector
from config_parser import Parser
import csv
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class Analytics:
    _instance = None

    @staticmethod
    def get_instance():
        """
         This method will return an instance of Analytics class
        :return:  An instance of Analytics class
        """
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

    def get_statistics_for_a_day(self, filename):
        """
        Extracting borrow_a_book and return history for a day and write it to a csv file
        :param filename: name of the target csv file
        :return: none
        """
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
                final_result = {"date": result3[0], "borrow_a_book": result1[0], "return": result2[0]}
                with open(filename, 'w+', newline='') as daily_report:
                    writer = csv.writer(daily_report)
                    writer.writerow(["date", "borrows", "returns"])
                    writer.writerow([final_result['date'], final_result["borrow_a_book"], final_result["return"]])
                    daily_report.close()
        except Exception as e:
            print(e)
        finally:
            my_database.close()

    def get_statistics_for_a_week(self, filename):
        """
        Return borrow_a_book & return history of the last 7 days
        :param filename: name of the target csv file
        :return:
        """
        try:
            my_database = mysql.connector.connect(
                host=self._host,
                database=self._database,
                user=self._user,
                passwd=self._password
            )
            if my_database.is_connected():
                cursor = my_database.cursor()
                sql1 = "select borrow_date as date, count(`id`) as count from borrowed_books where borrow_status = 'borrowed' group by borrow_date order by borrow_date asc limit 7"
                cursor.execute(sql1)
                result1 = cursor.fetchall()
                sql2 = "select count(`id`) as count from borrowed_books where return_status = 'returned' group by borrow_date order by borrow_date asc limit 7"
                cursor.execute(sql2)
                result2 = cursor.fetchall()
                final_result = []
                for r in range(len(result1)):
                    final_result.append([result1[r][0], result1[r][1], result2[r][0]])
                with open(filename, 'w+', newline='') as weekly_report:
                    writer = csv.writer(weekly_report)
                    writer.writerow(["date", "borrows", "returns"])
                    for result in final_result:
                        writer.writerow([result[0], result[1], result[2]])
                    weekly_report.close()
        except Exception as e:
            print(e)
        finally:
            my_database.close()

    @staticmethod
    def weekly_plot():
        """
        Draw weekly plot
        :return: none
        """
        ana = Analytics.get_instance()
        ana.get_statistics_for_a_week('weekly.csv')
        Analytics.get_instance().plot_barplot('weekly.csv', 'weekly.png')

    @staticmethod
    def daily_plot():
        """
        Draw daily plot
        :return: none
        """
        ana = Analytics.get_instance()
        ana.get_statistics_for_a_day('daily.csv')
        Analytics.get_instance().plot_barplot('daily.csv', 'daily.png')

    @staticmethod
    def plot_barplot(file, output_file):
        """
            Generate bar plot, can be used for both daily and weekly
            if the table has the same columns ['date', 'borrows', 'returns']
        :param file: path to CSV file
        :return: pop up figure
        """
        sns.set()
        daily_df = pd.read_csv(file)
        daily_df = pd.melt(daily_df, id_vars='date', var_name='type', value_name='count')

        with sns.color_palette('husl'):
            fig, ax = plt.subplots(1)
            sns.barplot(x='date', y='count', hue='type', data=daily_df, ax=ax)
        plt.savefig('images/' + output_file)
        plt.clf()


if __name__ == '__main__':
    anal = Analytics.get_instance()
    anal.daily_plot()
    anal.weekly_plot()


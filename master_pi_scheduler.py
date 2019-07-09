from crontab import CronTab


class Scheduler:
    """ This class is responsible for adding the below scripts into RPi's crontab"""

    @staticmethod
    def run_script():
        pi_cron = CronTab(user='pi')
        # Clear all previous cronjobs if any exists
        pi_cron.remove_all()

        # Schedule the flask application to run at start up
        schedule_flask = pi_cron.new(
            command="cd /home/pi/Desktop/piot-a2/webapp && /home/pi/miniconda3/envs/piot-a2/bin/python3.5 app.py")
        schedule_flask.setall('@reboot')

        # Schedule the web server to run at start up
        schedule_node = pi_cron.new(
            command="cd /home/pi/Desktop/piot-a2/webapp/front-end && node serve.js")
        schedule_node.setall('@reboot')

        pi_cron.write()


if __name__ == '__main__':
    Scheduler.run_script()
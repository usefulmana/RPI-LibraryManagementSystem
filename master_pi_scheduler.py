from crontab import CronTab


class Scheduler:
    """ This class is responsible for adding the below scripts into RPi's crontab"""

    @staticmethod
    def run_script():
        pi_cron = CronTab(user='pi')
        # Clear all previous cronjobs if any exists
        pi_cron.remove_all()

        # Schedule the monitor app to run every minute
        schedule_flask = pi_cron.new(
            command="cd /home/pi/Desktop/piot-a2/webapp && /home/pi/miniconda3/envs/piot-a2/bin/python3.5 app.py")
        schedule_flask.setall('@reboot')

        # Schedule bluetooth app to run every 5 minute
        schedule_node = pi_cron.new(
            command="cd /home/pi/Desktop/piot-a2/webapp/front-end && node serve.js")
        schedule_node.setall('@reboot')

        pi_cron.write()


if __name__ == '__main__':
    Scheduler.run_script()
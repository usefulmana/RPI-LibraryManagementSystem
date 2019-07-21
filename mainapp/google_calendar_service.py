# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.

from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from config_parser import Parser
import re
import base64
import requests

# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/calendar.events"
store = file.Storage("token.json")
creds = store.get()
if (not creds or creds.invalid):
    flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
    creds = tools.run_flow(flow, store)
service = build("calendar", "v3", http=creds.authorize(Http()))


def event_insert(user_email, book_id, name):
    """
    This function is responsible for adding an event to users' Google Calendar to remind them of the due date
    :param user_email: user's email
    :param book_id: book's id
    :param name: user's name
    :return: none
    """
    if g_mail_check(user_email) is None:
        return None
    else:
        date = datetime.now()
        time = date.time().strftime('%H:%M:%S')
        end = '{:%H:%M:%S}'.format(datetime.now() + timedelta(hours=1))
        due_date = (date + timedelta(days=Parser.get_instance().calendar_reminder)).strftime("%Y-%m-%d")
        time_start = "{}T{}+07:00".format(due_date, time)
        time_end = "{}T{}+07:00".format(due_date, end)
        readable_time_end = '{} {} GMT+07:00'.format(due_date, end)
        req = requests.get(url='http://127.0.0.1:5000/books/{}'.format(book_id))
        data = req.json()
        event = {
            "summary": "Reminder for {} to return {}".format(name, data['title']),
            "location": "RMIT University Vietnam Library",
            "description": "Please return {} to the University Library before {}".format(data['title'], readable_time_end),
            "start": {
                "dateTime": time_start,
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "attendees": [
                {"email": user_email},
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 120},
                    {"method": "popup", "minutes": 60},
                ],
            }
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    print("Event created! Please check your Google Calendar")
    # Extracting Google Calendar event ID
    string = event.get("htmlLink").split('=')[1]
    lens = len(string)
    lenx = lens - (lens % 4 if lens % 4 else 4)
    decoded_string = base64.b64decode(string[:lenx])
    event_id = str(decoded_string).split(' ')[0][2:].strip()
    return event_id


def g_mail_check(user_email):
    regex = '^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$'
    return re.search(regex, user_email)


def delete_event(event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print('[INFO] Google Calendar Event deleted')


if __name__ == "__main__":
    pass
    # delete_event('j35bsiacl4qt326arofaa8o7ks')
    # string = 'https://www.google.com/calendar/event?eid=NzFkdDFhNnEwNTFvb3Fza3B0a2xycjY0bDQgYWxleC5uZ3V5ZW4uMzE0MUBt'
    # split_string = string.split('=')
    # decoded_string = base64.b64decode(split_string[1])
    # event_id = str(decoded_string).split(' ')[0][2:].strip()
    # print(event_id)


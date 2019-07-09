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

# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/calendar"
store = file.Storage("token.json")
creds = store.get()
if(not creds or creds.invalid):
    flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
    creds = tools.run_flow(flow, store)
service = build("calendar", "v3", http=creds.authorize(Http()))


def event_insert(user_email):
    """
    This function is responsible for adding an event to users' Google Calendar to remind them of the due date
    :param user_email: user's email
    :return: none
    """
    date = datetime.now()
    time = date.time().strftime('%H:%M:%S')
    end = '{:%H:%M:%S}'.format(datetime.now() + timedelta(hours=1))
    tomorrow = (date + timedelta(days=7)).strftime("%Y-%m-%d")
    time_start = "{}T{}+07:00".format(tomorrow, time)
    time_end = "{}T{}+07:00".format(tomorrow, end)
    event = {
        "summary": "Return Borrowed Book",
        "location": "RMIT University Vietnam Library",
        "description": "Adding reminder to return borrowed book(s)",
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
    event = service.events().insert(calendarId = "primary", body = event).execute()
    print("Event created: {}".format(event.get("htmlLink")))


if __name__ == "__main__":
    pass

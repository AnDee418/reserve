from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']




def get_event():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    # 取得工程
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        timefrom = '2023/01/01'
        timeto = '2023/12/31'
        timefrom = datetime.datetime.strptime(timefrom, '%Y/%m/%d').isoformat()+'Z'
        timeto = datetime.datetime.strptime(timeto, '%Y/%m/%d').isoformat()+'Z'
        events_result = service.events().list(calendarId='420df69919379dc86afb012072f827f7bb2fa0a4d22e97e00be65eba1bc85b42@group.calendar.google.com', 
                                                timeMin=timefrom,
                                                timeMax=timeto,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])
        # f5eb0ca5ccc324aa0bf14f9e5dd1949a0b26deeaa300e8bea0d8807ba81cf94c@group.calendar.google.com
        

        if not events:
            print('No upcoming events found.')
            event_data = []
            return

        # Prints the start and name of the next 10 events

        # 日付とタイトルを変数に代入
        event_data = []
        for event in events:
            event_id = event['id']
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            start_datetime = datetime.datetime.fromisoformat(start_time)
            end_datetime = datetime.datetime.fromisoformat(end_time)
            start_date = start_datetime.date().strftime('%Y/%m/%d')
            start_time = start_datetime.time().strftime('%H:%M')
            end_date = end_datetime.date().strftime('%Y/%m/%d')
            end_time = end_datetime.time().strftime('%H:%M')
            summary = event['summary']
            event_data.append({'id':event_id,'start_date': start_date, 'start_time': start_time, 'end_date': end_date, 'end_time':end_time, 'summary': summary})


    except HttpError as error:
        print('An error occurred: %s' % error)

    return event_data


if __name__ == '__main__':
    get_event()
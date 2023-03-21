from __future__ import print_function
import datetime
import pytz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def delete(event_id):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # 削除処理
    service = build('calendar', 'v3', credentials=creds)

    service.events().delete(calendarId='420df69919379dc86afb012072f827f7bb2fa0a4d22e97e00be65eba1bc85b42@group.calendar.google.com',
                            eventId=event_id).execute()
    print('Event deleted')

if __name__ == '__main__':
    # 削除するイベントのIDを入力してください
    # event_id = 'xxxxx'
    delete()

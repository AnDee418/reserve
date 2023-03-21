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

def insert(name, menu, start_time_obj, end_time_obj):
    JST = pytz.timezone('Asia/Tokyo')

    # タイムゾーン情報を含めたdatetimeオブジェクトを生成
    start_time_obj = JST.localize(start_time_obj)
    end_time_obj = JST.localize(end_time_obj)

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

    # 追加工程
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'{name} {menu}',
        'location': '',
        'description': '',
        'start': {
            'dateTime': start_time_obj.isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end_time_obj.isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
    }

    event = service.events().insert(calendarId='420df69919379dc86afb012072f827f7bb2fa0a4d22e97e00be65eba1bc85b42@group.calendar.google.com',
                                    body=event).execute()
    print (event['id'])

        # トレーニングの場合、30分後に同じ予定を入れる
    if menu == 'トレーニング':
        next_start_time_obj = start_time_obj + datetime.timedelta(minutes=30)
        next_end_time_obj = end_time_obj + datetime.timedelta(minutes=30)
        event2 = {
            'summary': f'{name} {menu}',
            'location': '',
            'description': '',
            'start': {
                'dateTime': next_start_time_obj.isoformat(),
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'dateTime': next_end_time_obj.isoformat(),
                'timeZone': 'Asia/Tokyo',
            },
        }
        event2 = service.events().insert(calendarId='420df69919379dc86afb012072f827f7bb2fa0a4d22e97e00be65eba1bc85b42@group.calendar.google.com',
                                        body=event2).execute()
        print (event2['id'])

if __name__ == '__main__':
    insert()
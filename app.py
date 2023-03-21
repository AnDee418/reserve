from flask import Flask, render_template, request, make_response
import datetime 
from datetime import datetime, timedelta
import get_event as ge
import insert_event as ie
import delete as dele

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'gkhSDgih2gih5bjd7'

TIME_SLOTS = [  
                {'time': '09:00 ~ 09:30'},
                {'time': '09:30 ~ 10:00'},    
                {'time': '10:00 ~ 10:30'},    
                {'time': '10:30 ~ 11:00'},    
                {'time': '11:00 ~ 11:30'},    
                {'time': '11:30 ~ 12:00'},   
                {'time': '12:00 ~ 12:30'},    
                {'time': '12:30 ~ 13:00'},    
                {'time': '13:00 ~ 13:30'},    
                {'time': '13:30 ~ 14:00'},    
                {'time': '14:00 ~ 14:30'},    
                {'time': '14:30 ~ 15:00'},    
                {'time': '15:00 ~ 15:30'},    
                {'time': '15:30 ~ 16:00'},    
                {'time': '16:00 ~ 16:30'},    
                {'time': '16:30 ~ 17:00'},    
                {'time': '17:00 ~ 17:30'},    
                {'time': '17:30 ~ 18:00'},    
                {'time': '18:00 ~ 18:30'},    
                {'time': '18:30 ~ 19:00'}
            ]

SPECIAL_SLOTS = [
    '2023/04/05'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y/%m/%d').date()
        name = request.form.get('name')
        menu = request.form.get('menu')
        suturdays = suturday(date)
        reserve_list = event_list(date)
        time_slots = TIME_SLOTS
        add_events = add_event(time_slots,reserve_list)
        add_events_sut = add_event_sut(time_slots,reserve_list)
        print(add_events)
        if date.strftime('%Y/%m/%d') in SPECIAL_SLOTS:
            return render_template('holiday.html', menu=menu, name=name)

        if holiday(date):
            print(holiday(date))
            return render_template('holiday.html',menu = menu, name=name)
        
        response = make_response(render_template('index.html',add_events = add_events, menu = menu, name=name, date=date, suturdays=suturdays, add_events_sut=add_events_sut))
        expires = datetime.now() + timedelta(minutes=1)
        response.set_cookie('date', str(date), expires=expires)
        response.set_cookie('name', name, expires=expires)
        response.set_cookie('menu', menu, expires=expires)
        return response
        
        # return render_template('index.html',add_events = add_events, menu = menu, name=name, date=date, suturdays=suturdays, add_events_sut=add_events_sut)
    else:
        # cookieから情報を取得する
        date_str = request.cookies.get('date')
        name = request.cookies.get('name')
        menu = request.cookies.get('menu')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return render_template('index.html', menu = menu, name=name, date=date)
        else:
            return render_template('index.html')
        
        # return render_template('index.html')
    


@app.route('/remind', methods=['POST'])
def remind():
    name = request.form.get('name')
    date = request.form.get('date')
    menu = request.form.get('menu')
    time = request.form.get('time')
    print(time)

    return render_template('remind.html', name=name, date=date, menu=menu, time=time)

@app.route('/try_insert', methods=['POST'])
def try_insert():
    name = request.form.get('name')
    date = request.form.get('date')
    menu = request.form.get('menu')
    time = request.form.get('time')

    start_time_str, end_time_str = time.split(' ~ ')

    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    start_time_obj = datetime.combine(date_obj, datetime.strptime(start_time_str, '%H:%M').time())
    end_time_obj = datetime.combine(date_obj, datetime.strptime(end_time_str, '%H:%M').time())

    ie.insert(name, menu, start_time_obj, end_time_obj)

    return render_template('result.html')

@app.route('/check')
def check():
    return render_template('check.html')

@app.route('/check/get', methods=['POST'])
def check_get():
    name = request.form.get('name')
    event_checks = event_check(name)
    print(event_checks)
    return render_template('check_get.html', event_checks=event_checks)

@app.route('/delete/remind', methods=['POST'])
def delete_remind():
    id = request.form.get('id')
    name = request.form.get('name')
    menu = request.form.get('menu')
    date = request.form.get('date')
    time = request.form.get('time')
    return render_template('delete_remind.html', id=id, name=name, menu=menu, date=date, time=time)

@app.route('/delete', methods=['POST'])
def delete():
    event_id = request.form.get('id')

    dele.delete(event_id)

    return render_template('delete_msg.html')





def holiday(date):
    if date.weekday() == 6 or (date.weekday() == 5 and date.day // 7 in [0, 2, 4]):
        return True
    else:
        return False
    
def suturday(date):
    if date.weekday() == 5 and date.day // 7 in [1, 3]:
        return True
    else:
        return False

def event_list(date):
    events = ge.get_event()
    reserve_list = []
    for event in events:
        start_datetime = datetime.strptime(f"{event['start_date']} {event['start_time']}", '%Y/%m/%d %H:%M')
        end_datetime = datetime.strptime(f"{event['end_date']} {event['end_time']}", '%Y/%m/%d %H:%M')
        time_range = f"{start_datetime.strftime('%H:%M')} ~ {end_datetime.strftime('%H:%M')}"
        if start_datetime.date() == date:
            reserve_list.append({
                'event_date': start_datetime.strftime('%Y/%m/%d'),
                'time': time_range,
                'start_time': start_datetime.strftime('%Y/%m/%d %H:%M'),
                'end_time': end_datetime.strftime('%Y/%m/%d %H:%M'),
                'summary': event['summary']
            })
    return reserve_list

def event_check(name):
    events = ge.get_event()
    print(events)
    reserve_list = []
    for event in events:
        start_datetime = datetime.strptime(f"{event['start_date']} {event['start_time']}", '%Y/%m/%d %H:%M')
        end_datetime = datetime.strptime(f"{event['end_date']} {event['end_time']}", '%Y/%m/%d %H:%M')
        time_range = f"{start_datetime.strftime('%H:%M')} ~ {end_datetime.strftime('%H:%M')}"
        if  name in event['summary']:
            reserve_list.append({
                'id':event['id'],
                'event_date': start_datetime.strftime('%Y/%m/%d'),
                'time': time_range,
                'start_time': start_datetime.strftime('%Y/%m/%d %H:%M'),
                'end_time': end_datetime.strftime('%Y/%m/%d %H:%M'),
                'summary': event['summary']
            })
    return reserve_list

def add_event(time_slots, reserve_list):
    TODAY_LIST = []
    for time_slot in time_slots:
        matching_reserves = [reserve for reserve in reserve_list if reserve['time'] == time_slot['time']]
        if matching_reserves:
            summary = '/'.join([reserve['summary'] for reserve in matching_reserves])
            med_count = summary.count('治療')
            jim_count = summary.count('トレーニング')
            TODAY_LIST.append({
                'time': time_slot['time'],
                'summary': summary,
                'med_count': med_count,
                'jim_count': jim_count,
            })
        else:
            TODAY_LIST.append({
                'time': time_slot['time'],
                'summary': '',
                'med_count': 0,
                'jim_count': 0
            })

        for i in range(len(TODAY_LIST)-1):
            if TODAY_LIST[i+1]['med_count'] == 2:
                TODAY_LIST[i]['jim_count'] = 1
            elif 'トレーニング' in TODAY_LIST[i+1]['summary']:
                TODAY_LIST[i]['jim_count'] = 1

    return TODAY_LIST

def add_event_sut(time_slots, reserve_list):
    SUTURDAY_LIST = []
    for time_slot in time_slots:
        matching_reserves = [reserve for reserve in reserve_list if reserve['time'] == time_slot['time']]
        if matching_reserves:
            summary = '/'.join([reserve['summary'] for reserve in matching_reserves])
            med_count = summary.count('治療')
            jim_count = summary.count('トレーニング')
            SUTURDAY_LIST.append({
                'time': time_slot['time'],
                'summary': summary,
                'med_count': med_count,
                'jim_count': jim_count,
            })
        else:
            SUTURDAY_LIST.append({
                'time': time_slot['time'],
                'summary': '',
                'med_count': 0,
                'jim_count': 0
            })
        if time_slot['time'] == '14:30 ~ 15:00':
            break

        for i in range(len(SUTURDAY_LIST)-1):
            if SUTURDAY_LIST[i+1]['med_count'] == 2:
                SUTURDAY_LIST[i]['jim_count'] = 1
            elif 'トレーニング' in SUTURDAY_LIST[i+1]['summary']:
                SUTURDAY_LIST[i]['jim_count'] = 1
    return SUTURDAY_LIST

if __name__ == '__main__':
    app.run(debug=True)

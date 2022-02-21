from django import template
import json
from datetime import datetime, timedelta
import datetime as date
import array
import os
import textwrap
from django.db import connection
from django.http.response import JsonResponse
import requests

register = template.Library()

from ..models import EmployeeAvailability, User, EmployeeOverAvailability
from ..models import UserPrice, BasicInfo, BookableAmenity
from ..models import UserMediaRecord
from ..models import Availability
from ..models import OverAvailability
from ..models import Event

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@register.simple_tag
def change_date(dateVal=''):
    # print(dateVal)
    dd = str(dateVal)
    new_date = datetime.strptime(dd, "%Y-%m-%d").strftime("%d %b %Y")
    # print(new_date)
    return new_date

@register.simple_tag
def change_dat(dateVal=''):
    dd = str(dateVal)
    new_date = datetime.strptime(dd, "%Y-%m-%d").strftime("%d/%m/%Y")
    return new_date

@register.simple_tag
def change_type_int(val=''):
    dd = int(val)
    return dd

@register.simple_tag
def change_type_str(val=''):
    dd = str(val)
    return dd

@register.simple_tag
def check_type(val=''):
    dd = type(val)
    # print(dd)
    return dd

@register.simple_tag
def truncate_str(val=''):
    truncated_text = textwrap.shorten(val, width=50, placeholder="...")
    return truncated_text

@register.simple_tag
def check_ext(val=''):
    filename, fileExtension = os.path.splitext(str(val))
    # print(fileExtension)
    return fileExtension

@register.simple_tag
def change_date1(dateVal=''):
    # print(dateVal)
    dd = str(dateVal)
    new_date = datetime.strptime(dd, "%Y-%m-%d").strftime("%d %b")
    return new_date

@register.simple_tag
def fetch_user(user_id=''):
    user = User.objects
    auth = user.filter(id=user_id).values('first_name','last_name')[0]
    
    return auth

@register.simple_tag
def fetch_user_image(user_id=''):
    user = UserMediaRecord.objects
    if user.filter(user_id=user_id,type='ProfilePhoto'):
        auth = user.filter(user_id=user_id,type='ProfilePhoto').values()[0]
        return auth
    else:
        return 1

@register.simple_tag
def check_avail(user_id='',day = ''):
    availability = Availability.objects
    availData = availability.all().filter(user_id=user_id,day_name=day).values()
    # availData = availability.filter(user_id=user_id,day_name=day)
    return availData

@register.simple_tag
def check_all_avail(user_id='', schedule_id = ''):
    availability = EmployeeAvailability.objects
    availData = availability.all().filter(user_id=user_id,schedule_id = schedule_id).values()
    return availData

@register.simple_tag
def over_avail(user_id='', schedule_id = ''):
    availability = EmployeeOverAvailability.objects
    availData = availability.all().filter(user_id=user_id,schedule_id = schedule_id).values()
    return availData

@register.simple_tag
def get_over_avail(user_id='', start = '', end = ''):
    user_id = str(user_id)
    start = str(start)
    end = str(end)
    
    cursor = connection.cursor()        

    cursor.execute("SELECT *, MIN(date) as mindate, MAX(date) as maxdate FROM `overwrite_availabilities` where user_id = "+user_id+" AND date >= '"+start+"' AND date <= '"+end+"' GROUP By start_time, end_time ORDER BY date")
    availData = dictfetchall(cursor)
    # availData = cursor.fetchall()
    # print(availData)

    # for availD in availData:
    #     if availD[]

    return availData


@register.simple_tag
def check_over_avail(user_id=''):
    today = datetime.today()
    availability = OverAvailability.objects
    availData = availability.all().filter(user_id=user_id).order_by('date').values()
    # availData = availability.all().filter(user_id=user_id,date__gte = today).order_by('date').values()

    data = []
    cursor = connection.cursor()
    
    if availData:
        ai = 0
        for avail in availData: 
            # print('test new ',avail)
            start = avail['date']
            start_last = avail['date'] - timedelta(days=1)
            end = avail['date']

            data.append(ai)
            data[ai] =[]
            data[ai].append(avail['date'])
            data[ai].append(end)
            # data[ai].append(avail['start_time'])
            # data[ai].append(avail['end_time'])
            # data[ai].append(avail['id'])

            if ai > 0 and data[ai - 1][1] == start_last:   
                ss = str(start_last)
                cursor.execute("SELECT start_time FROM `overwrite_availabilities` where user_id = '"+str(user_id)+"' AND date = '"+ss+"'")
                lastData = dictfetchall(cursor)

                # print(lastData[0]['start_time'])
                cursor.execute("SELECT start_time FROM `overwrite_availabilities` where user_id = '"+str(user_id)+"' AND date = '"+str(start)+"'")
                currData = dictfetchall(cursor)

                if lastData[0]['start_time'] == currData[0]['start_time']:
                    data.pop(ai)
                    data[ai - 1][1] = end
                else:
                    ai = ai + 1                
            else:
                ai = ai + 1
    # print(data)
    return data

@register.simple_tag
def convert_json(jsonStr=''):
    aList = json.loads(jsonStr)
    return aList

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)

@register.simple_tag
def get_service(value = ''):
    
    data = json.loads(value)

    arr = []
    for end_val in data:
        for key, cat in end_val.items():
            # print(cat)
            for vall in cat:
                # print(vall)
                # for vv in vall:
                    # print(vv)
                valCheck = UserPrice.objects.filter(id=vall)

                if bool(valCheck):
                    session_record = UserPrice.objects.get(id=vall)
                    arr.append(session_record.session_name)

    if arr == []:
        arr = ''
    else:
        return arr

@register.simple_tag
def get_service_data(value = ''):
    
    data = json.loads(value)

    arr = []
    for end_val in data:
        for key, cat in end_val.items():
            # print(key)
            # print(cat)
            for vall in cat:
                # print(type(vall))
                # for vv in vall:
                    # print(vv)
                # session_record = UserPrice.objects.get(id=vall)
                arr.append(int(vall))


    return arr

#schedule 
@register.simple_tag
def check_emp_avail(user_id='', schedule_id='',day = ''):
    # print(user_id)
    # print(schedule_id)
    availability = EmployeeAvailability.objects
    availData = availability.all().filter(user_id=user_id,schedule_id = schedule_id,day_name=day).values()
    # availData = availability.filter(user_id=user_id,day_name=day)
    # print(availData)
    return availData

@register.simple_tag
def get_emp_over_avail(user_id='', schedule_id='', start = '', end = ''):
    user_id = str(user_id)
    schedule_id = str(schedule_id)
    start = str(start)
    end = str(end)
    
    cursor = connection.cursor()        

    cursor.execute("SELECT *, MIN(date) as mindate, MAX(date) as maxdate FROM `employee_overwrite_availabilities` where user_id = "+user_id+" AND schedule_id = "+schedule_id+" AND date >= '"+start+"' AND date <= '"+end+"' GROUP By start_time, end_time ORDER BY date")
    availData = dictfetchall(cursor)
    # availData = cursor.fetchall()
    # print(availData)

    # for availD in availData:
    #     if availD[]

    return availData


@register.simple_tag
def check_emp_over_avail(user_id='', schedule_id=''):
    today = datetime.today()
    availability = EmployeeOverAvailability.objects
    availData = availability.all().filter(user_id=user_id,schedule_id=schedule_id,date__gte = today).order_by('date').values()
    # availData = availability.all().filter(user_id=user_id,date__gte = today).order_by('date').values()
    # print(availData)
    data = []
    cursor = connection.cursor()
    
    if availData:
        ai = 0
        for avail in availData: 
            # print('test new ',avail)
            start = avail['date']
            start_last = avail['date'] - timedelta(days=1)
            end = avail['date']

            data.append(ai)
            data[ai] =[]
            data[ai].append(avail['date'])
            data[ai].append(end)
            # data[ai].append(avail['start_time'])
            # data[ai].append(avail['end_time'])
            # data[ai].append(avail['id'])
            # print(data[ai - 1][1])
            # print(start_last)

            if ai > 0 and data[ai - 1][1] == start_last:   
                ss = str(start_last)
                cursor.execute("SELECT start_time FROM `employee_overwrite_availabilities` where user_id = '"+str(user_id)+"' AND schedule_id = '"+str(schedule_id)+"' AND date = '"+ss+"'")
                lastData = dictfetchall(cursor)

                # print(lastData[0]['start_time'])
                cursor.execute("SELECT start_time FROM `employee_overwrite_availabilities` where user_id = '"+str(user_id)+"' AND schedule_id = '"+str(schedule_id)+"' AND date = '"+str(start)+"'")
                currData = dictfetchall(cursor)

                # print(lastData[0]['start_time'])
                # print(currData[0]['start_time'])
                if lastData[0]['start_time'] == currData[0]['start_time']:
                    data.pop(ai)
                    data[ai - 1][1] = end
                else:
                    ai = ai + 1                
            else:
                ai = ai + 1
    # print(data)
    return data

@register.simple_tag
def get_data_service(id='', type = ''):
    record = UserPrice.objects.all().filter(id=id).values('id','session_name').order_by('session_name').first()
    
    return record['session_name']

@register.simple_tag
def get_pt(id=''):
    record = User.objects.all().filter(id=id).values('id','first_name','last_name').order_by('first_name').first()
    
    return record['first_name'] + ' ' + record['last_name']

@register.simple_tag
def get_book_id(user_id = '',date = '',con1 = '',con2 = '',con3 = '',con4 = '',con5 = ''):
    records = Event.objects.all().filter(user_id=user_id,date_of_booking=date).filter(con1 & con2 & con3 & con4 & con5).values()

    dataI = []
    # print(records)
    for record in records: 
        dataI.append(record['id'])

    return dataI

@register.simple_tag
def get_book_time(id):
    records = Event.objects.all().filter(id=id).values()
    
    # print(records)
    data = []
    dataST = []
    dataS = []
    dataP = []
    dataC = []
    dataI = []
    ai = 0
    for record in records:        
        time = record['time_of_booking']        
        dd = datetime.strptime(str(time), '%H:%M %p')
        dat = dd + timedelta(hours=1)
        dd = datetime.strptime(str(dat), "%Y-%m-%d %H:%M:%S").strftime("%H:%M %p")
        
        data.append(str(time + ' - ' + dd))
        
        type_of_service = {            
            1 : 'Session',
            2 : 'Services',
            3 : 'Amenities Booking',
            4 : 'Classes',
            5 : 'Live Classes',
        }
        type_of_services = int(record['type_of_services'])
        dataST.append(type_of_service[type_of_services])

        if type_of_services == 3:
            recordd = UserPrice.objects.all().filter(id=record['service']).values('id','type_of_amenity').order_by('type_of_amenity').first()   

            if recordd != None:
                user = BookableAmenity.objects
                if user.filter(id=recordd['type_of_amenity']):
                    auth = user.filter(id=recordd['type_of_amenity']).values('name').first()
                    dataS.append(auth['name']) 
                
            
        else:
            recordd = UserPrice.objects.all().filter(id=record['service']).values('id','session_name').order_by('session_name').first()   
            
            if recordd:
                dataS.append(recordd['session_name']) 
            

        recordd = User.objects.all().filter(id=record['pt_name']).values('id','first_name','last_name').order_by('first_name').first()
        dataP.append(recordd['first_name'] + ' ' + recordd['last_name'])

        dataC.append(record['client_name'])
        dataI.append(record['id'])

        ai = ai + 1

    print(dataS)
    dataArr = []
    dataArr.append(data)
    dataArr.append(dataST)
    dataArr.append(dataS)
    dataArr.append(dataP)
    dataArr.append(dataC)
    dataArr.append(dataI)

    # print(dataArr)
    return dataArr

@register.simple_tag
def get_location(user_id=''):
    user = BasicInfo.objects
    if user.filter(user_id=user_id):
        auth = user.filter(user_id=user_id).values('location').first()
        return auth['location']
    else:
        return ''

@register.simple_tag
def get_amenity(id = ''):
    user = BookableAmenity.objects
    if user.get(id=id):
        auth = user.filter(id=id).values('name').first()
        return auth['name']
    else:
        return ''

@register.simple_tag
def splitArray(value):
    if value != '':
        key = ','
        a_list = value.split(key)
        map_object = map(int, a_list)
        list_of_integers = list(map_object)
        return list_of_integers

@register.simple_tag
def convert_date(value):
    dd = str(value)
    new_date = datetime.strptime(dd, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
    return new_date
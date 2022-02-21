from django.shortcuts import render
from .. models import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django import template
from django.core.mail import *
import math
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.hashers import *
from django.core.signing import Signer
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import random
from django.utils.text import slugify
import string
import json
from django.contrib import messages
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from smtplib import SMTP 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from django.template.loader import get_template
from . send_email import *
import requests
import datetime as date
from flask import render_template, make_response, redirect
from django.shortcuts import render  
from django import forms
from django.db import connection
from django.db.models import Q

from django.core.files.storage import FileSystemStorage

import os
# Create your views here.


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))

def setAvailability(request):
    user_id = request.session['user_id']

    title = 'Set Availability'

    employees = User.objects.all().filter(user_type="Employee").values_list('id','first_name', 'last_name').order_by('first_name')
    # mediaSocialMedia=UserMediaRecord.objects.all().filter(user_id=user_id,type="myMedia[]").values()

    #print(employees)
    context = {
        'pageTitle': title,
        'employees': employees,
    }

    return render(request, 'schedules/setAvailability.html', context)

def saveSchedule(request):
    user_id = request.session['user_id']
    data = request.POST

    # print(data)

    employee_id = data.get("employee_id")
    schedule_name = data.get("schedule_name")
    # print(user_id)
    # print(employee_id)

    avail_values = UserSchedule.objects.filter(user_id=user_id,employee_id=employee_id,is_default=1)
    # print(avail_values)
    is_default = 1
    if avail_values:
        is_default = 0

    schedules = UserSchedule(
        user_id=user_id,
        employee_id=employee_id,
        schedule_name=schedule_name,
        is_default=is_default,
        
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    schedules.save()

    s_id = schedules.id

    context = {
        'id':s_id,'name':schedule_name,'emp_id':employee_id
        }


    return JsonResponse(context)

def getEmployee(request):
    user_id = request.session['user_id']
    data = request.POST

    empId = data.get("empId")

    scheduleList = UserSchedule.objects.all().filter(user_id=user_id,employee_id=empId).values().order_by('-is_default','id')
    firstData = UserSchedule.objects.all().filter(user_id=user_id,employee_id=empId).values().order_by('-is_default','id').first()
    
    if firstData:
        context = {
            'scheduleList': scheduleList,
            'emp_id': empId,
            'first_id': firstData['id'],
        }

        return render(request, 'elements/schedule/getEmployee.html', context)
    else:
        return HttpResponse(1)

def deleteSchedule(request):
    user_id = request.session['user_id']
    data = request.POST

    schedule_id = data.get("id")
    
    scheduleinfo = UserSchedule.objects.get(id=schedule_id)    

    if scheduleinfo.is_default == 1:
        nextData = UserSchedule.objects.filter(id__gt=schedule_id,user_id=user_id).first()
        if nextData:
            UserSchedule.objects.filter(id=nextData.id).update(is_default=1)

    UserSchedule.objects.filter(id=schedule_id).delete()
    return HttpResponse(1)

def showCalender(request):
    user_id = request.session['user_id']
    data = request.POST

    s_id = data.get("s_id")
    emp_id = data.get("emp_id")
    # print(s_id)
    # print(emp_id)
    userData = User.objects.filter(id=emp_id).first()
    scheduleData = UserSchedule.objects.filter(id=s_id).first()
    # print(userData)
    # print(scheduleData)

    context = {
        'userId': emp_id,
        'schedule_id': s_id,
        'scheduleData':scheduleData,
    }

    return render(request, 'schedules/available_list_data.html', context)

def saveAvailabilityEmp(request):
    if request.method == 'POST':
        data = request.POST       
        # print(data)
        user_id = request.session['user_id']

        dayArr = data.getlist("serializedData[day_name][]")
        schedule_id = data.getlist("serializedData[schedule_id]")
        user_id = data.getlist("serializedData[emp_id]")

        # EmployeeAvailability.objects.filter(user_id=user_id).delete()
        if not dayArr:
            day_array = {'SUN','MON','TUE','WED','THU','FRI','SAT'}
            day = data.get("serializedData[day_name]")

            if day != None:
                start_arr = data.getlist("serializedData[start_time['"+day+"'][]][]")
                end_arr = data.getlist("serializedData[end_time['"+day+"'][]][]")
                if not start_arr:
                    start_arr_json = '["'+data.get("serializedData[start_time['"+day+"'][]]")+'"]'
                    end_arr_json = '["'+data.get("serializedData[end_time['"+day+"'][]]")+'"]'                
                else:
                    start_arr_json = json.dumps(start_arr)
                    end_arr_json = json.dumps(end_arr)

                if EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day):
                    EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).update(start_time=start_arr_json,end_time=end_arr_json)
                else:
                    record = EmployeeAvailability(
                        user_id=user_id,
                        schedule_id=schedule_id,
                        day_name=day,
                        start_time=start_arr_json,
                        end_time=end_arr_json,

                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )

                    record.save()

                day_array.remove(day)
            else:
                EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id).delete()

            for day in day_array:
                EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).delete()

        else:
            day_array = {'SUN','MON','TUE','WED','THU','FRI','SAT'}
            for day in dayArr:
                # print(dayArr)
                start_arr = data.getlist("serializedData[start_time['"+day+"'][]][]")
                end_arr = data.getlist("serializedData[end_time['"+day+"'][]][]")
                if not start_arr:
                    start_arr_json = '["'+data.get("serializedData[start_time['"+day+"'][]]")+'"]'
                    end_arr_json = '["'+data.get("serializedData[end_time['"+day+"'][]]")+'"]'                
                else:
                    start_arr_json = json.dumps(start_arr)
                    end_arr_json = json.dumps(end_arr)

                if EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day):
                    EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).update(start_time=start_arr_json,end_time=end_arr_json)
                else:
                    record = EmployeeAvailability(
                        user_id=user_id,
                        schedule_id=schedule_id,
                        day_name=day,
                        start_time=start_arr_json,
                        end_time=end_arr_json,

                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )

                    record.save()
                
                day_array.remove(day)
            
            # print(day_array)
            for day in day_array:
                EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).delete()


    return HttpResponse(1)

def saveAvailEmp(request):
    if request.method == 'POST':
        data = request.POST       

        schedule_id = data.getlist("serializedData[schedule_id]")
        user_id = data.getlist("serializedData[emp_id]")
        uncheck = data.get("uncheck")
        day = data.get("day")

        if EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day):
            EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).update(status=uncheck)

    return HttpResponse(1)


def empCalenderPost(request):
    user_id = request.session['user_id']
    data = request.POST
    

    date_Arr = data.get("serializedData[selected_values]")
    schedule_id = data.get("serializedData[schedule_id]")
    user_id = data.get("serializedData[emp_id]")


    aList = json.loads(date_Arr)
    for x in aList:
        status = 0
        chk_date = date.datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")
        # print(chk_date)
        start_arr = data.getlist("serializedData[over_start_time[]][]")
        end_arr = data.getlist("serializedData[over_end_time[]][]")
        if not start_arr:
            start_arr = data.get("serializedData[over_start_time[]]")
            end_arr = data.get("serializedData[over_end_time[]]")
            if not start_arr:
                start_arr_json = '["''"]'
                end_arr_json = '["''"]'
                status = 1
            else:
                start_arr_json = '["'+data.get("serializedData[over_start_time[]]")+'"]'
                end_arr_json = '["'+data.get("serializedData[over_end_time[]]")+'"]'                
        else:
            start_arr_json = json.dumps(start_arr)
            end_arr_json = json.dumps(end_arr)

        if EmployeeOverAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,date=chk_date):
            EmployeeOverAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,date=chk_date).update(start_time=start_arr_json,end_time=end_arr_json)
        else:
            record = EmployeeOverAvailability(
                user_id=user_id,
                schedule_id=schedule_id,
                date=chk_date,
                start_time=start_arr_json,
                end_time=end_arr_json,
                status=status,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            record.save()

    context = {
        'userId' : user_id,
        'schedule_id' : schedule_id,
    } 

    return render(request, 'elements/schedule/overwrite_section.html', context)

def empCalenderPostEdit(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    schedule_id = data.get("schedule_id")
    user_id = data.get("emp_id")

    day_array = {'SUN','MON','TUE','WED','THU','FRI','SAT'}
    day = data.get("day")[0:3].upper()
    # print(day)

    status = 0
    if day != None:
        start_arr = data.getlist("serializedData[over_start_time_edit[]][]")
        end_arr = data.getlist("serializedData[over_end_time_edit[]][]")
        if not start_arr:
            start_arr = data.get("serializedData[over_start_time[]]")
            end_arr = data.get("serializedData[over_end_time[]]")
            if not start_arr:
                start_arr_json = '["''"]'
                end_arr_json = '["''"]'
                status = 1
            else:
                start_arr_json = '["'+data.get("serializedData[over_start_time[]]")+'"]'
                end_arr_json = '["'+data.get("serializedData[over_end_time[]]")+'"]'                
        else:
            start_arr_json = json.dumps(start_arr)
            end_arr_json = json.dumps(end_arr)
        # print(start_arr_json)
        # print(end_arr_json)
        # print(schedule_id)
        # print(user_id)
        if EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day):
            EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).update(start_time=start_arr_json,end_time=end_arr_json)
        else:
            # print(schedule_id)
            record = EmployeeAvailability(
                user_id=user_id,
                schedule_id=schedule_id,
                day_name=day,
                start_time=start_arr_json,
                end_time=end_arr_json,
                status=status,


                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            # print(record)
            record.save()
    else:
        EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day).delete()



    return HttpResponse(1)


def checkEmpCalVal(request):
    data = request.POST
    user_id = request.session['user_id']
    schedule_id = data.get("schedule_id")
    user_id = data.get("emp_id")
    # print(user_id)
    # print(schedule_id)

    today_date = data.get("date[]")
    new_today_date = date.datetime.strptime(today_date, "%m/%d/%Y").strftime("%Y-%m-%d")

    # basicinfo = EmployeeOverAvailability.objects.get(user_id=user_id)
    avail_values = EmployeeOverAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,date=new_today_date)

    if not avail_values:
        day = date.datetime.strptime(today_date, "%m/%d/%Y").strftime("%a")
        avail_values = EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day,status=0)        
        queries = avail_values
            
        if not avail_values:
            queries = 0
    else:
        queries = avail_values
        
    context = {
        'queries' : queries
    } 

    return render(request, 'elements/schedule/calender_section.html', context)

def checkEmpCalValEdit(request):
    data = request.POST
    user_id = request.session['user_id']
    schedule_id = data.get("schedule_id")
    user_id = data.get("emp_id")
    # print(user_id)
    # print(schedule_id)

    today_date = data.get("date[]")
    new_today_date = date.datetime.strptime(today_date, "%m/%d/%Y").strftime("%Y-%m-%d")

    # basicinfo = EmployeeOverAvailability.objects.get(user_id=user_id)
    avail_values = EmployeeOverAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,date=new_today_date)

    if not avail_values:
        day = date.datetime.strptime(today_date, "%m/%d/%Y").strftime("%a")
        avail_values = EmployeeAvailability.objects.filter(user_id=user_id,schedule_id=schedule_id,day_name=day,status=0)        
        queries = avail_values
            
        if not avail_values:
            queries = 0
    else:
        queries = avail_values
        
    context = {
        'queries' : queries
    } 

    return render(request, 'elements/schedule/edit_calender_section.html', context)


def deleteEmpOver(request):
    data = request.POST
    user_id = request.session['user_id']

    user_id = data.get("emp_id")
    schedule_id = data.get("schedule_id")
    dates = data.get("dates")
    aList = json.loads(dates)
    for x in aList:
        
        dateVal = date.datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")
        EmployeeOverAvailability.objects.filter(user_id=user_id, schedule_id=schedule_id, date = dateVal).delete()

    context = {
        'userId' : user_id,
        'schedule_id' : schedule_id,
    } 
    return render(request, 'elements/schedule/overwrite_section.html', context)

def empOverwritesection(request):
    return render(request, 'elements/schedule/overwrite_section.html')

def makeDefault(request):
    data = request.POST

    emp_id = data.get("emp_id")
    schedule_id = data.get("schedule_id")   

    UserSchedule.objects.filter(employee_id=emp_id).update(is_default=0)
    UserSchedule.objects.filter(id=schedule_id).update(is_default=1)

    return HttpResponse(1)

def editSchedule(request):
    user_id = request.session['user_id']
    data = request.POST

    # print(data)
    schedule_id = data.get("schedule_id")
    schedule_name = data.get("schedule_name")

    UserSchedule.objects.filter(id=schedule_id).update(schedule_name=schedule_name)

    context = {
        'id':schedule_id,'name':schedule_name
        }


    return JsonResponse(context)

def cloneSchedule(request):
    user_id = request.session['user_id']
    data = request.POST

    # print(data)
    schedule_id = data.get("schedule_id")
    schedule_name = data.get("schedule_name")

    scheduleinfo = UserSchedule.objects.get(id=schedule_id)

    if scheduleinfo:
        schedules = UserSchedule(
            user_id=scheduleinfo.user_id,
            employee_id=scheduleinfo.employee_id,
            schedule_name=schedule_name,
            is_default=0,
            
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        schedules.save()

        s_id = schedules.id
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO `employee_availabilities` (user_id, schedule_id, day_name, start_time, end_time, status, created_at, updated_at) SELECT user_id, '"+str(s_id)+"', day_name, start_time, end_time, status, '"+str(datetime.utcnow())+"', '"+str(datetime.utcnow())+"' FROM `employee_availabilities` where schedule_id = "+schedule_id+"")
        cursor.execute("INSERT INTO `employee_overwrite_availabilities` (user_id, schedule_id, date, start_time, end_time, created_at, updated_at) SELECT user_id, '"+str(s_id)+"', date, start_time, end_time, '"+str(datetime.utcnow())+"', '"+str(datetime.utcnow())+"' FROM `employee_overwrite_availabilities` where schedule_id = "+schedule_id+"")

        

    context = {
        'id':schedule_id,'name':schedule_name
        }


    return JsonResponse(context)

def showCalenderView(request):
    user_id = request.session['user_id']
    data = request.POST

    s_id = data.get("s_id")
    emp_id = data.get("emp_id")

    userData = User.objects.filter(id=emp_id).first()
    scheduleData = UserSchedule.objects.filter(id=s_id).first()

    context = {
        'userId': emp_id,
        'schedule_id': s_id,
        'scheduleData':scheduleData,
    }

    return render(request, 'schedules/available_calender_data.html', context)

def getEventData(request):
    # print('eventdat new')
    data = request.POST
    # print(data)

    s_id = data.get("schedule_id")
    emp_id = data.get("emp_id")
    start = data.get("start")
    end = data.get("end")
    # print(s_id)
    # print(emp_id)
    # print('rtyrtyrt')

    availability = EmployeeOverAvailability.objects
    
    
    eAvailability = EmployeeAvailability.objects
    availAllDays = eAvailability.all().filter(user_id=emp_id,schedule_id = s_id).values().order_by('day_name')

    dataResults = []
    count = 0
    dayss = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT','SUN']
    for num in range(7):
        dstart = date.datetime.strptime(start, "%Y-%m-%d")
        dend = date.datetime.strptime(end, "%Y-%m-%d")
        # print(dstart)
        # print(dend)
        
        days = [dstart + timedelta(days=x) for x in range((dend-dstart).days + 1) if (dstart + timedelta(days=x)).weekday() == num]
        for datee in days:
            # print(dayss[num])  
            datee, vll = str(datee).split(' ')                                                                                                    
            # print(datee)                                                                                                        
            # datee = date.datetime.strptime(str(datee), "%Y-%m-%d")
            # print(emp_id)
            # print(s_id)
            # print(datee)
            availData = availability.all().filter(user_id=emp_id,schedule_id = s_id,date=datee).values().first()
            # print('new test ',datee,availData)
            # print('test 0000')
            # print(availData)
            countSlot = 1
            if availData != None:
                # print('test 1111')
                aList = json.loads(availData['start_time'])
                bList = json.loads(availData['end_time'])
                for tm, tm1 in zip(aList, bList):           
                    dataResults.append(count)
                    dataResults[count] =[]

                    date_str=tm
                    date_obj = date.datetime.strptime(date_str, '%I:%M %p')
                    ddStart = str(availData['date'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')

                    date_str=tm1
                    date_obj = date.datetime.strptime(date_str, '%I:%M %p')
                    ddEnd = str(availData['date'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')

                    dataResults[count].append(str(ddStart))
                    dataResults[count].append(str(ddEnd))
                    dataResults[count].append(str(tm + ' - ' + tm1))
                    dataResults[count].append(str(availData['date']))
                    count += 1
                    countSlot += 1

            else:
                # print('test 22222')
                # print(datee)
                # print(dayss[num])
                availData = eAvailability.all().filter(user_id=emp_id,schedule_id = s_id,day_name=dayss[num]).values().order_by('day_name').first()
                # print(availData)
                countSlot = 1
                if availData:
                    aList = json.loads(availData['start_time'])
                    bList = json.loads(availData['end_time'])
                    for tm, tm1 in zip(aList, bList):           
                        dataResults.append(count)
                        dataResults[count] =[]

                        date_str=tm
                        date_obj = date.datetime.strptime(date_str, '%I:%M %p')
                        ddStart = str(datee)+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')
                        # print(ddStart)

                        date_str=tm1
                        date_obj = date.datetime.strptime(date_str, '%I:%M %p')
                        ddEnd = str(datee)+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')
                        # print(ddEnd)

                        dataResults[count].append(str(ddStart))
                        dataResults[count].append(str(ddEnd))
                        dataResults[count].append(str(tm + ' - ' + tm1))
                        dataResults[count].append(str(datee))
                        count += 1
                        countSlot += 1

    # print(dataResults)

    # dataResults = []
    # print(availDatas)
    # count = 0
    # for availData in availDatas:
    #     # print(availData)        
    #     aList = json.loads(availData['start_time'])
    #     bList = json.loads(availData['end_time'])
    #     for tm, tm1 in zip(aList, bList):           
    #         dataResults.append(count)
    #         dataResults[count] =[]

    #         date_str=tm
    #         date_obj = date.datetime.strptime(date_str, '%I:%M %p')
    #         ddStart = str(availData['date'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')
    #         # print(ddStart)

    #         date_str=tm1
    #         date_obj = date.datetime.strptime(date_str, '%I:%M %p')
    #         ddEnd = str(availData['date'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')
    #         # print(ddEnd)

    #         dataResults[count].append(str(ddStart))
    #         dataResults[count].append(str(ddEnd))
    #         dataResults[count].append(str(tm + ' - ' + tm1))
    #         count += 1

    
    # if not availDatas:
    #     print(5)
    # else:
    #     count = 0
    #     aList = json.loads(availData['start_time'])
    #     bList = json.loads(availData['end_time'])
    #     for tm, tm1 in zip(aList, bList):           
    #         dataResults.append(count)
    #         dataResults[count] =[]
    #         dataResults[count].append(str(availData['date']))
    #         dataResults[count].append(str(tm))
    #         dataResults[count].append(str(tm1))
    #         count += 1

    # print(dataResults)
    json_format = json.dumps(dataResults)

    return HttpResponse(json_format)

def calendar(request):
    user_id = request.session['user_id']

    start = date.datetime.now()
    end = date.datetime.now() + timedelta(days=60)

    title = 'Set Availability'
    serviceRecords = UserPrice.objects.filter(user_id=user_id).values_list('id','session_name').order_by('session_name')

    ptusers = User.objects.all().filter(user_type="Personal Trainer").values_list('id','first_name', 'last_name').order_by('first_name')

    records = Event.objects.all().filter(user_id=user_id,date_of_booking__gte=start,date_of_booking__lte=end).values().order_by('date_of_booking')

    lastDate = ''
    dataRecords = []
    ai = 0
    ak = 0
    
    for record in records:
        
        if lastDate == record['date_of_booking']:
            dataRecords[ak].append(aj)
            dataRecords[ak][aj] =[]
            dataRecords[ak][aj].append(record)
            ai = ai
        else:
            datVal = record['date_of_booking']

            aj = 0
            dataRecords.append(ai)
            dataRecords[ai] =[]
            dataRecords[ai].append(aj)
            dataRecords[ai][aj] =[]
            dataRecords[ai][aj].append(record)
            ak = ai
            ai = ai + 1

        lastDate = record['date_of_booking']
        
        
        aj = aj + 1

    # print(dataRecords)


    basicinfo = ''
    if BasicInfo.objects.filter(user_id=user_id):
        basicinfo = BasicInfo.objects.get(user_id=user_id)

    context = {
        'pageTitle': title,
        'serviceRecords': serviceRecords,
        'ptusers': ptusers,
        'basicinfo':basicinfo,
        'eventList':dataRecords,
        'start': start,
        'end':end
    }

    return render(request, 'schedules/calendar.html', context)

def getServiceData(request):
    category = request.POST.get("category")

    if category == 3:
        category = 5

    records = UserPrice.objects.filter(session_category=category).values_list('id','session_name').order_by('session_name')
    context = {
        'records': records,
    }
    
    return render(request, 'elements/schedule/getServiceData.html', context)

def addEvent(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    date_of_booking = data.get("date_of_booking")
    time_of_booking = data.get("time_of_booking")
    location = data.get("location")
    client_name = data.get("client_name")
    pt_name = data.get("pt_name")
    type_of_services = data.get("type_of_services")
    service = data.get("service")

    events = Event(
        user_id=user_id,
        date_of_booking=date.datetime.strptime(date_of_booking, "%d/%m/%Y").strftime("%Y-%m-%d"),
        time_of_booking=time_of_booking,
        location=location,
        client_name=client_name,
        pt_name=pt_name,
        type_of_services=type_of_services,
        service=service,
        status=1,
        slug=slugify(client_name + "-" + rand_slug()),
        
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    events.save()

    records = Event.objects.all().filter(user_id=user_id).values().order_by('date_of_booking')
    context = {
        'eventList': records,
    }

    print(records)

    return render(request, 'elements/schedule/event_table.html', context)

def viewEvent(request):
    data = request.POST

    id = data.get("id")
    eventData = Event.objects.get(id=id)

    ptusers = User.objects.all().filter(user_type="Personal Trainer").values_list('id','first_name', 'last_name').order_by('first_name')
    records = UserPrice.objects.filter(session_category=eventData.type_of_services).values_list('id','session_name').order_by('session_name')

    context = {
        'eventData': eventData,
        'ptusers': ptusers,
        'records': records,
    }
    
    return render(request, 'elements/schedule/event_popup.html', context)

def deleteEvent(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    Event.objects.filter(id=id).delete()

    return HttpResponse(1)

def editEvent(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    # return HttpResponse(1)

    date_of_booking = data.get("date_of_booking")
    time_of_booking = data.get("time_of_booking")
    # location = data.get("location")
    # client_name = data.get("client_name")
    pt_name = data.get("pt_name")
    # type_of_services = data.get("type_of_services")
    # service = data.get("service")
    event_id = data.get("event_id")


    Event.objects.filter(id=event_id).update(
        date_of_booking=date.datetime.strptime(date_of_booking, "%d/%m/%Y").strftime("%Y-%m-%d"),
        time_of_booking=time_of_booking,
        pt_name=pt_name,
        updated_at=datetime.utcnow(),
    )

    records = Event.objects.all().filter(user_id=user_id).values().order_by('date_of_booking')
    context = {
        'eventList': records,
    }

    return render(request, 'elements/schedule/event_table.html', context)

def searchEvent(request):
    user_id = request.session['user_id']
    data = request.POST
    print(data)

    search_service = data.get("search_service")
    search_pt = data.get("search_pt")
    search_client = data.get("search_client")
    search_start_date = data.get("search_start_date")
    search_end_date = data.get("search_end_date")

    # return HttpResponse(1)   
    con1 =con2 = con3 = con4 = con5 = Q()
    events = Event.objects
    if search_service != '':
        con1 = Q(type_of_services=search_service) #any query you want
    if search_pt != '':
        con2 = Q(type_of_services=search_service) #any query you want
    if search_client != '':
        con3 = Q(client_name__contains = search_client) #any query you want
    if search_start_date != '' and search_end_date != '':
        con4 = Q(date_of_booking__gte = search_start_date) #any query you want
        con5 = Q(date_of_booking__lte = search_end_date) #any query you want

    records = events.all().filter(user_id=user_id).filter(con1 & con2 & con3 & con4 & con5).values().order_by('date_of_booking')
    
    context = {
        'eventList':records
    }

    return render(request, 'elements/schedule/event_table.html', context)

def getSEventData(request):
    user_id = request.session['user_id']
    data = request.POST

    # start = data.get("start")
    # end = data.get("end")
    print(user_id)

    availability = Event.objects    
    availAllDays = availability.all().filter(user_id=user_id,date_of_booking__gte=date.datetime.now()).values().order_by('date_of_booking')

    dataResults = []
    count = 0

    countSlot = 1
    if availAllDays != None:
        for avail in availAllDays:
            dataResults.append(count)
            dataResults[count] =[]

            date_str=avail['time_of_booking']
            date_obj = date.datetime.strptime(date_str, '%I:%M %p')
            ddStart = str(avail['date_of_booking'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')

            dd = date.datetime.strptime(date_str, '%H:%M %p')
            data = date_obj + timedelta(hours=1)
            dd = datetime.strptime(str(data), "%Y-%m-%d %H:%M:%S").strftime("%H:%M %p")
            date_obj = date.datetime.strptime(date_str, '%I:%M %p')
            ddEnd = str(avail['date_of_booking'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')

            # date_str=tm1
            # date_obj = date.datetime.strptime(date_str, '%I:%M %p')
            # ddEnd = str(availData['date'])+'T'+date.datetime.strftime(date_obj, '%H:%M:%S')

            dataResults[count].append(str(ddStart))
            dataResults[count].append(str(ddEnd))
            dataResults[count].append(str(avail['client_name']))
            dataResults[count].append(str(avail['date_of_booking']))
            dataResults[count].append(str(avail['id']))
            count += 1
            countSlot += 1

    # print(dataResults)
    json_format = json.dumps(dataResults)

    return HttpResponse(json_format)
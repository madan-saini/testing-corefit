from django.shortcuts import render
from .. models import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
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
from datetime import datetime
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from smtplib import SMTP 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from django.template.loader import get_template
from . send_email import *
import datetime as date
from datetime import datetime, timedelta
import requests
import time
from flask import render_template, make_response, redirect
from django.shortcuts import render  
import json
from django.db.models import Q

import os
# Create your views here.

# def __init__(self):
#     Flask.redirect('/profile', 301)


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

# def setcookie(request):  
#     # return 5 * x
#     response = HttpResponse("Cookie Set")  
#     response.set_cookie('user_remember', '1')
#     return response

# def getcookie(request):  
#     tutorial  = request.COOKIES['java-tutoriall']  
#     return HttpResponse("java tutorials @: "+  tutorial); 

def userType(id,type):
    user = User.objects.get(id=id)
    user_type1 = user.user_type
    context ={
        'user_type1':user_type1,
        'type':type
    }
    return context


def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))

def logout(request):
    
        
    del request.session['user_id']
    messages.success(
                    request, f"Your account logout successfully.")
    return HttpResponseRedirect("login")


def login(request):
    title = 'Login'

    user = User.objects
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        emailCheck = user.filter(email_address=email,freelance_id=0)

        if bool(emailCheck):
            auth = user.get(email_address=email,freelance_id=0)
            datas = check_password(password, auth.password)
            if datas:
                request.session['user_id'] = auth.id
                request.session['user_type'] = auth.user_type
                user_id = request.session['user_id']
                usertype = auth.user_type
                if usertype == "Personal Trainer":
                    return HttpResponse(2)
                if usertype == "Gym&Studio":
                    return HttpResponse(1)
                if usertype == "FreelanceTrainer":
                    return HttpResponse(3)
                if usertype == "Personal Training Company":
                    return HttpResponse(4)
                if usertype == "Sports Facility":
                    return HttpResponse(5)
                return HttpResponse(1)
            else:
                messages.error(
                    request, f"Invalid email or password")
                return HttpResponse(0)
        else:
            messages.error(
                    request, f"Invalid email or password")
            return HttpResponse(0)

        # print(datas)
        # return HttpResponse(json_string)
    # user = User.objects.get()
  
    # print the response dictionary
    try: 
        user_email_address = request.COOKIES['user_email_address']
    except:
        user_email_address = ''

    # print(r.text)
    context = {
        # 'users': user,
        'pageTitle': title,
        'user_email_address':user_email_address
    }
    return render(request, 'users/login.html', context)

def forgotPassword(request):
    title = 'Forgot Password'
    user = User.objects
    
    if request.method == 'POST':
        email = request.POST['email']
        emailCheck = user.filter(email_address=email,freelance_id=0)

        if bool(emailCheck):
            auth = user.get(email_address=email,freelance_id=0)
            user_name = auth.first_name+' '+auth.last_name
            # user_id = request.session['user_id']
            # return HttpResponse(1)

            otp = generateOTP()
            request.session['otp'] = ''
            signer = Signer()
            encrypthOTP = make_password(otp)
            request.session['otp'] = encrypthOTP
            sessionOtp = request.session['otp']

            emailtemplate = Emailtemplate.objects
            emailTemplateData = emailtemplate.get(id=3)

            email_subject = emailTemplateData.subject
            email_template = emailTemplateData.template

            edits = [('[!username!]', user_name), ('[!SITE_TITLE!]', settings.SITE_TITLE),('[!OTP!]',otp),('[!REPLY_EMAIL!]',settings.REPLY_EMAIL),('[!REPLY_PHONE!]',settings.REPLY_PHONE),('[!MAIL_SIGNATURE!]',settings.MAIL_SIGNATURE)]
            for search, replace in edits:
                email_template = email_template.replace(search, replace)

            data = []
            data.append(
                {
                    'template': email_template,
                    "logo": settings.HTTP_PATH + '/' +settings.LOGO_INNER,
                    'HTTP_PATH': settings.HTTP_PATH,
                    'SITE_TITLE': settings.SITE_TITLE
                    
                })
            jsonData = data
            template = env.get_template('email_template.html')
            output = template.render(data=jsonData[0])

            send_mail(email, email_subject, output)  
            return HttpResponse(0)
        else:
            messages.error(
                    request, f"Invalid email address")
            return HttpResponse(1)

        # print(datas)
        # return HttpResponse(json_string)
    # user = User.objects.get()

    
    context = {
        # 'users': user,
        'pageTitle': title
    }
    return render(request, 'users/forgot-password.html', context)

def resetPassword(request, slug):
    title = 'Reset Password'
    user = User.objects

    emailCheck = user.filter(uniqueKey=slug)

    if bool(emailCheck):
        if request.method == 'POST':
            password = request.POST['password']

            auth = user.get(uniqueKey=slug)
            datas = check_password(password, auth.password)
            
            if datas:
                # messages.error(
                #     request, f"You cannot put your old password as new password, please use another password.")
                return HttpResponse(0)
            else:
                password=make_password(password)

                uniqueKey = ''
                User.objects.filter(uniqueKey=slug).update(uniqueKey=uniqueKey,password=password)  

                messages.success(
                        request, f"Password updated successfully.")
                return HttpResponse(1)
            
        context = {
            # 'users': user,
            'pageTitle': title,
            'slug':slug
        }
        return render(request, 'users/reset-password.html', context)
    else:
        print(45654)
        return HttpResponseRedirect('/login')

def checkValid(request):
    emailId = request.POST.get("serializedData[email]")    
    emailCheck = User.objects.filter(email_address=emailId,freelance_id=0)
    phone = request.POST.get("serializedData[phone]")    
    # terms = request.POST.get("serializedData[terms]")    
    # print(emailId)
    # print(terms)
    # return HttpResponse(request.POST.get("serializedData[phone]"))
    phoneCheck = User.objects.filter(contact=phone)
    if bool(emailCheck) == False:
        if bool(phoneCheck) == False:
            return HttpResponse('0')
        else:
            return HttpResponse('Phone number already exist')
    else:
        return HttpResponse('Email address already exist')

def register(request):
    title = 'Registration'

    if request.method == 'POST':
        data = request.POST

        if data.get("serializedData[user_type]") == "Personal Trainer":
            users = User(
                freelance_id=0,
                email_address=data.get("serializedData[email]"),
                contact=data.get("serializedData[phone]"),
                first_name=data.get("serializedData[first_name]"),
                last_name=data.get("serializedData[last_name]"),
                user_type="FreelanceTrainer",
                password=make_password(data.get("serializedData[password]")),
                slug=slugify(data.get("serializedData[first_name]") + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            users.save()

            # users2 = User(
            #     freelance_id=users.id,
            #     email_address=data.get("serializedData[email]"),
            #     contact=data.get("serializedData[phone]"),
            #     first_name=data.get("serializedData[first_name]"),
            #     last_name=data.get("serializedData[last_name]"),
            #     user_type=data.get("serializedData[user_type]"),
            #     password=make_password(data.get("serializedData[password]")),
            #     slug=slugify(data.get("serializedData[first_name]") + "-" + rand_slug()),
            #     created_at=datetime.utcnow(),
            #     updated_at=datetime.utcnow(),
            # )
            #
            # users2.save()
        else:
            users = User(
                freelance_id=0,
                email_address=data.get("serializedData[email]"),
                contact=data.get("serializedData[phone]"),
                first_name=data.get("serializedData[first_name]"),
                last_name=data.get("serializedData[last_name]"),
                user_type=data.get("serializedData[user_type]"),
                password=make_password(data.get("serializedData[password]")),
                slug=slugify(data.get("serializedData[first_name]") + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            users.save()

        messages.success(
                    request, f"Your account has been registered successfully. You can login now.")
        return HttpResponse(users)

    context = {
        'pageTitle': title
    }
    return render(request, 'users/register.html', context)

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def otp_send(request):

    emailId = request.POST.get("email")
    emailCheck = User.objects.filter(email_address=emailId,freelance_id=0)

    if bool(emailCheck):
        auth = User.objects.get(email_address=emailId,freelance_id=0)
        first_name = auth.first_name
        last_name = auth.last_name
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
    
    
    otp = generateOTP()
    request.session['otp'] = ''
    otp_sen = otp
    otp = otp+emailId
    encrypthOTP = make_password(otp)
    request.session['otp'] = encrypthOTP

    # user = User.objects
    # auth = user.get(email_address=emailId)
    user_name = first_name + ' ' + last_name
    emailtemplate = Emailtemplate.objects
    emailTemplateData = emailtemplate.get(id=3)

    email_subject = emailTemplateData.subject
    email_template = emailTemplateData.template

    edits = [('[!username!]', user_name), ('[!SITE_TITLE!]', settings.SITE_TITLE),('[!OTP!]',otp_sen),('[!REPLY_EMAIL!]',settings.REPLY_EMAIL),('[!REPLY_PHONE!]',settings.REPLY_PHONE),('[!MAIL_SIGNATURE!]',settings.MAIL_SIGNATURE)]
    for search, replace in edits:
        email_template = email_template.replace(search, replace)

    data = []
    data.append(
        {
            'template': email_template,
            "logo": settings.HTTP_PATH + '/' +settings.LOGO_INNER,
            'HTTP_PATH': settings.HTTP_PATH,
            'SITE_TITLE': settings.SITE_TITLE
            
        })
    jsonData = data
    template = env.get_template('email_template.html')
    output = template.render(data=jsonData[0])

    send_mail(emailId, email_subject, output) 
    return HttpResponse(1)

def otp_verify(request):
    otp1 = request.POST.get("serializedData[otp_code]")
    otp2 = request.POST.get("serializedData[otp_code1]")
    otp3 = request.POST.get("serializedData[otp_code2]")
    otp4 = request.POST.get("serializedData[otp_code3]")
    otp5 = request.POST.get("serializedData[otp_code4]")
    otp6 = request.POST.get("serializedData[otp_code5]")
    emailId = request.POST.get("serializedData[email]")

    
    checkOtp=otp1+otp2+otp3+otp4+otp5+otp6+emailId
    
    sessionOtp = request.session['otp']
    if check_password(checkOtp, sessionOtp):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def forgot_otp_verify(request):
    otp1 = request.POST.get("serializedData[otp_code]")
    otp2 = request.POST.get("serializedData[otp_code1]")
    otp3 = request.POST.get("serializedData[otp_code2]")
    otp4 = request.POST.get("serializedData[otp_code3]")
    otp5 = request.POST.get("serializedData[otp_code4]")
    otp6 = request.POST.get("serializedData[otp_code5]")

    email = request.POST.get("serializedData[email]")
    uniqueKey = rand_slug()
    
    checkOtp=otp1+otp2+otp3+otp4+otp5+otp6
    
    sessionOtp = request.session['otp']
    if check_password(checkOtp, sessionOtp):     

        User.objects.filter(email_address=email,freelance_id=0).update(uniqueKey=uniqueKey)
        return HttpResponse(uniqueKey)
    else:
        return HttpResponse(0)

def index(request):
    title = 'Index'
    
    context = {
        # 'users': user,
        'pageTitle': title
    }
    return render(request, 'users/index.html', context)

def profile(request):
    title = settings.SITE_TITLE + ' | ' + 'Profile'

    user_id = request.session['user_id']
    request.session['user_type'] = "Gym or Studio"
    userTypes =userType(user_id,request.session['user_type'])
    if userTypes['user_type1'] != request.session['user_type']:
        request.session['user_type'] = userTypes['type']
        messages.error(
                    request, f"Your are not allowed for this url .")
        return HttpResponseRedirect('login')

        # return HttpResponse('Hello')

    # print(user_id)
    user = User.objects
    auth = user.get(id=user_id)
    
    amenities = Amenity.objects.all().values_list('id','name').order_by('name')
    equipments = Equipment.objects.all().values_list('id','name').order_by('name')
    services = Service.objects.all().values_list('id','name').order_by('name')
    countries = Country.objects.all().values_list('id','name').order_by('name')
    languages = Language.objects.all().values_list('id','name').order_by('name')
    branchRecords = Branch.objects.all().values_list('id','branch_name').order_by('branch_name')
    brandRecords = Brand.objects.all().values_list('id','brand_name').order_by('brand_name')

    basicinfo = ''
    awardInfo = ameniinfo = amenityinfo = ''
    equipinfo = equipmentinfo = ''
    if BasicInfo.objects.filter(user_id=user_id):
        basicinfo = BasicInfo.objects.get(user_id=user_id)
        amenityinfo = UserAmenity.objects.all().filter(user_id=user_id).values()
        ameniinfo = UserAmenity.objects.filter(user_id=user_id)
        equipinfo = UserEquipment.objects.filter(user_id=user_id)
        equipmentinfo = UserEquipment.objects.all().filter(user_id=user_id).values()
        
    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    # *******
    mediaSocialMedia=UserMediaRecord.objects.all().filter(user_id=user_id,type="myMedia[]").values()

    mediavirtual_tour=UserMediaRecord.objects.all().filter(user_id=user_id,type="virtual_tour").values()
    mediatile_image=UserMediaRecord.objects.all().filter(user_id=user_id,type="tile_image").values()

    mediamyMedia=UserMediaRecord.objects.all().filter(user_id=user_id,type="myMedia[]").values().order_by('-created_at')
    mediaprofile_photo=UserMediaRecord.objects.filter(user_id=user_id,type='ProfilePhoto').values()
    # print('mediaprofile_photo',mediaprofile_photo)

    userClientTransformationData = UserClientTransformation.objects.all().filter(user_id=user_id).values()

    if mediamyMedia:
        mediamyMedia = mediamyMedia[0]

    
    # print('mediatile_image',mediatile_image[0])
    
    # print('mediaprofile_photo',mediaprofile_photo[0]['data'])
# **********

    sesstionTypes = Session.objects.all().values_list('id','name').order_by('name')
    serviceAmenityTypes = ServiceAmenity.objects.all().values_list('id','name').order_by('name')
    amenityTypes = BookableAmenity.objects.all().values_list('id','name').order_by('name')
    sports = Sport.objects.all().values_list('id','name').order_by('name')
    priceList = UserPrice.objects.filter(user_id=user_id).values()

    # print(ameniinfo)
    # print(amenityinfo)
    amen_arr = []
    if amenityinfo:
        for amm in amenityinfo:
            amen_arr.append(amm['amenity_id'])

    equi_arr = []
    if equipmentinfo:
        for eqmm in equipmentinfo:
            equi_arr.append(eqmm['equipment_id'])

    cities = []
    # if basicinfo:
    #     cities = City.objects.all().values_list('id','name').order_by('name')
    if basicinfo:
        cities = City.objects.filter(country_id=basicinfo.country).values_list('id','name').order_by('name')
        

    existingFaq = ExistingFaq.objects.all().filter().values()
    faq_tabless = UserFaq.objects.all().filter(user_id=user_id).values()

    # print(cities)
    context = {
        # 'users': user,
        'pageTitle': title,
        'user': auth,
        'facility_types': settings.FACILITY_TYPE,
        'branchRecords': branchRecords,
        'brandRecords': brandRecords,
        'basicinfo': basicinfo,
        'languages': languages,
        'countries': countries,
        'cities': cities,
        'services': services,
        'amenities': amenities,
        'equipments': equipments,
        'amenityinfo': amenityinfo,
        'ameniinfo': ameniinfo,
        'equipinfo': equipinfo,
        'equipmentinfo': equipmentinfo,
        'amenityList': amen_arr,
        'equipList': equi_arr,
        'awardList': awardInfo,
        'sesstionTypes': sesstionTypes,
        'serviceAmenityTypes': serviceAmenityTypes,
        'amenityTypes': amenityTypes,
        'sports': sports,
        'priceList': priceList,

        # *********
        'mediaSocialMedia':mediaSocialMedia,
        'mediavirtual_tour':mediavirtual_tour,
        'mediatile_image':mediatile_image,
        'mediaprofile_photo':mediaprofile_photo,
        'mediamyMedia':mediamyMedia,
        "userClientTransformationData":userClientTransformationData,
        "existingFaq":existingFaq,
        "faq_tabless":faq_tabless
        # **********
    }
   
    return render(request, 'users/profile.html', context)

def thankyou(request):
    
    title = 'Thank You'
    
    context = {
        # 'users': user,
        'pageTitle': title
    }
    return render(request, 'users/thankyou.html', context)

def overwritesection(request):
    return render(request, 'users/overwrite_section.html')

def newOffer(request):
    title = settings.SITE_TITLE + ' | ' + 'New Offer'

    user_id = request.session['user_id']
    offerRecords = UserOffer.objects.filter(user_id=user_id).values()
    serviceRecords = UserPrice.objects.filter(user_id=user_id).values()

    session_records = UserPrice.objects.filter(session_category=1,user_id=user_id).values_list('id','session_name').order_by('session_name')
    service_records = UserPrice.objects.filter(session_category=2,user_id=user_id).values_list('id','session_name').order_by('session_name')
    day_records = UserPrice.objects.filter(session_category=3,user_id=user_id).values_list('id','session_name').order_by('session_name')
    membership_records = UserPrice.objects.filter(session_category=4,user_id=user_id).values_list('id','session_name').order_by('session_name')

    context = {
        'pageTitle': title,
        'offerRecords': offerRecords,
        'serviceRecords': serviceRecords,
        'session_records': session_records,
        'service_records': service_records,
        'day_records': day_records,
        'membership_records': membership_records,
    }

    return render(request, 'users/new_offer.html', context)
    
def employee(request):
    title = settings.SITE_TITLE + ' | ' + 'Employees'
    user_id = request.session['user_id']

    # employees = User.objects.all().filter(user_type="Personal Trainer").exclude(freelance_id=0).select_related('freelance').values().order_by('id')
    employees = User.objects.all().filter(Q(user_type ="Personal Trainer")).exclude(freelance_id=0)

    # print(employees)
    start = date.datetime.now()
    end = date.datetime.now() + timedelta(days=60)
    context = {
        'pageTitle': title,
        'employees': employees,
        'start': start.strftime("%m/%d/%Y"),
        'end':end.strftime("%m/%d/%Y")
    }

    return render(request, 'users/employee.html', context)

def searchEmployee(request):
    user_id = request.session['user_id']
    data = request.POST
    print(data)

    empSearch = data.get("name")
    employees = User.objects.all().filter(Q(user_type ="Personal Trainer") and Q(first_name__contains = empSearch)).exclude(freelance_id=0)
    context = {
        'employees': employees,
    }

    return render(request, 'elements/users/emp_table.html', context)
    
def deleteEmployee(request):
    data = request.POST
    data = request.POST

    id = data.get("id")
    User.objects.filter(id=id).delete()

    return HttpResponse(1)





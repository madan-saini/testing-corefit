from locale import currency
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
from django.db.models import Q, Avg, Count

from requests import get


from django.core.files.storage import FileSystemStorage

import os
# Create your views here.


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))

def bankcards(request):
    user_id = request.session['user_id']

    title = 'Bank and Card Information'

    bankInfo = cardInfo = ''
    if UserBank.objects.filter(user_id=user_id):
        bankInfo = UserBank.objects.get(user_id=user_id)
    if UserCard.objects.filter(user_id=user_id):
        cardInfo = UserCard.objects.get(user_id=user_id)

    context = {
        'pageTitle': title,
        'user_id': user_id,
        'bankInfo': bankInfo,
        'cardInfo': cardInfo,
    }

    return render(request, 'wallets/bankcards.html', context)

def bankSubmit(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    account_name = data['account_name']
    bank_name = data['bank_name']
    routing_number = data['routing_number']
    account_number = data['account_number']
    account_type = data['account_type']
    sort_code = data['sort_code']
    iban_number = data['iban_number']

    bankInfo = UserBank.objects.filter(user_id=user_id)

    # print(bankInfo['id'])
    if not bankInfo:
        record = UserBank(
            user_id=user_id,
            account_name=account_name,
            bank_name=bank_name,
            routing_number=routing_number,
            account_number=account_number,
            account_type=account_type,
            sort_code=sort_code,
            iban_number=iban_number,
            status=1,
            
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()
    else:
        bankInfo = UserBank.objects.get(user_id=user_id)

        UserBank.objects.filter(id=bankInfo.id).update(
            account_name=account_name,
            bank_name=bank_name,
            routing_number=routing_number,
            account_number=account_number,
            account_type=account_type,
            sort_code=sort_code,
            iban_number=iban_number,

            updated_at=datetime.utcnow(),
        )

    return HttpResponse(1)

def cardSubmit(request):
    user_id = request.session['user_id']
    data = request.POST
    print(data)

    card_holder_name = data['card_holder_name']
    card_number = data['card_number']
    card_type = data['card_type']
    card_cvv = data['card_cvv']
    expiry_date = data['expiry_date']

    cardInfo = UserCard.objects.filter(user_id=user_id)

    # # print(bankInfo['id'])
    if not cardInfo:
        # print(2)
        record = UserCard(
            user_id=user_id,
            card_holder_name=card_holder_name,
            card_number=card_number,
            card_type=card_type,
            card_cvv=card_cvv,
            expiry_date=expiry_date,
            
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()
    else:
        cardInfo = UserCard.objects.get(user_id=user_id)

        UserCard.objects.filter(id=cardInfo.id).update(
            card_holder_name=card_holder_name,
            card_number=card_number,
            card_type=card_type,
            card_cvv=card_cvv,
            expiry_date=expiry_date,

            updated_at=datetime.utcnow(),
        )

    return HttpResponse(1)


def boltlist(request):
    user_id = request.session['user_id']

    title = 'Bolt-Ons List'

    boltons = Bolton.objects.all().filter(status=1).values()

    context = {
        'pageTitle': title,
        'user_id': user_id,
        'boltons': boltons,
    }

    return render(request, 'wallets/bolton-list.html', context)

def mybolt(request):
    user_id = request.session['user_id']

    title = 'My Bolt-Ons'

    boltons = UserBolton.objects.all().filter(user_id=user_id).select_related('bolton')

    context = {
        'pageTitle': title,
        'user_id': user_id,
        'boltons': boltons,
    }

    return render(request, 'wallets/mybolt.html', context)

def updateBoltStatus(request):
    user_id = request.session['user_id']
    data = request.POST

    id = data['id']
    checkbox = data.get("checkbox")

    if checkbox == "true":
        status = 1
    else:
        status = 0
        
    UserBolton.objects.filter(id=id).update(status=status, updated_at=datetime.utcnow())

    return HttpResponse(1)

def enquireSubmit(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    subject = data['subject']
    message = data['message']

    record = Enquiry(
        user_id=user_id,
        type='Bolton',
        subject=subject,
        message=message,
        slug=slugify(subject + "-" + rand_slug()),
        
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    record.save()

    signer = Signer()
    email = 'madan.saini@nimbleappgenie.com'

    emailtemplate = Emailtemplate.objects
    emailTemplateData = emailtemplate.get(id=5)

    email_subject = emailTemplateData.subject
    edits = [('[!SITE_TITLE!]', settings.SITE_TITLE)]
    for search, replace in edits:
        email_subject = email_subject.replace(search, replace)

    email_template = emailTemplateData.template
    edits = [('[!subject!]', subject), ('[!message!]', message), ('[!SITE_TITLE!]', settings.SITE_TITLE),('[!REPLY_EMAIL!]',settings.REPLY_EMAIL),('[!REPLY_PHONE!]',settings.REPLY_PHONE),('[!MAIL_SIGNATURE!]',settings.MAIL_SIGNATURE)]
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
    template = env.get_template('enquire_email.html')
    output = template.render(data=jsonData[0])

    send_mail(email, email_subject, output) 

    return HttpResponse(1)

def payment(request):
    user_id = request.session['user_id']

    title = 'Payment List'

    # boltons = Bolton.objects.all().filter(status=1).values()

    start = date.datetime.now()
    end = date.datetime.now() + timedelta(days=60)

    context = {
        'pageTitle': title,
        'user_id': user_id,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
        # 'boltons': boltons,
    }

    return render(request, 'wallets/payment.html', context)

def subscriptionPlans(request):
    user_id = request.session['user_id']
    userData = User.objects.get(id=user_id)
    curr = userData.currency

    title = 'Available Subscription Plans'

    features = Feature.objects.all().filter(status=1).values()
    basicPlan = Plan.objects.get(duration='Weekly',type='Basic')
    premiumPlan = Plan.objects.get(duration='Weekly',type='Premium')

    # defualtCurr = Currency.objects.get(is_default=1)
    # currencies = Currency.objects.all().values()   

    # r = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=0b56eb89edf94afbbc392d5e136dbd17')
    # result = r.json()

    # curr = ''
    # for currency in currencies:
    #     if currency['name'][0:2] == result['country_code']:
    #         curr = currency['name']

    # if curr == '':
    #     curr = defualtCurr.name

    basicPlanPrice = PlanPrice.objects.get(plan_id=basicPlan.id,currency=curr)
    premiumPlanPrice = PlanPrice.objects.get(plan_id=premiumPlan.id,currency=curr)

    context = {
        'pageTitle': title,
        'user_id': user_id,
        'features': features,
        'basicPlan': basicPlan,
        'premiumPlan': premiumPlan,
        'basicPlanPrice': basicPlanPrice,
        'premiumPlanPrice': premiumPlanPrice,
        'curr': curr,
        'type': 'weekly',
    }

    return render(request, 'wallets/subscriptionPlans.html', context)

def myPlan(request):
    user_id = request.session['user_id']

    title = 'My Plan'

    context = {
        'pageTitle': title,
        'user_id': user_id,
    }

    return render(request, 'wallets/myPlan.html', context)

def getPlanData(request):
    user_id = request.session['user_id']
    userData = User.objects.get(id=user_id)
    curr = userData.currency

    data = request.POST

    category = data['category']

    features = Feature.objects.all().filter(status=1).values()
    basicPlan = Plan.objects.get(duration=category,type='Basic')
    premiumPlan = Plan.objects.get(duration=category,type='Premium')

    # defualtCurr = Currency.objects.get(is_default=1)
    # currencies = Currency.objects.all().values()   

    # r = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=0b56eb89edf94afbbc392d5e136dbd17')
    # result = r.json()

    # curr = ''
    # for currency in currencies:
    #     if currency['name'][0:2] == result['country_code']:
    #         curr = currency['name']

    # if curr == '':
    #     curr = defualtCurr.name

    basicPlanPrice = PlanPrice.objects.get(plan_id=basicPlan.id,currency=curr)
    premiumPlanPrice = PlanPrice.objects.get(plan_id=premiumPlan.id,currency=curr)

    context = {
        'user_id': user_id,
        'features': features,
        'basicPlan': basicPlan,
        'premiumPlan': premiumPlan,
        'basicPlanPrice': basicPlanPrice,
        'premiumPlanPrice': premiumPlanPrice,
        'curr': curr,
        'type': category,
    }

    return render(request, 'elements/wallet/feature_table.html', context)

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

def employeeRequest(request):
    user_id = request.session['user_id']

    title = 'Employee Request'

    print(user_id)
    records = Request.objects.all().filter(gym_user_id=user_id).select_related('gym_user','freelancer_user')
    print(records)

    start = date.datetime.now()
    end = date.datetime.now() + timedelta(days=60)
    context = {
        'pageTitle': title,
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'requests/employee-request.html', context)
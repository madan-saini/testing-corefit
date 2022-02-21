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
import requests
import datetime as date
from flask import render_template, make_response, redirect
from django.shortcuts import render  
from django import forms
from django.db.models import Q, Avg, Count

from django.core.files.storage import FileSystemStorage

import os
# Create your views here.


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))

def getCityList(request):
    countryId = request.POST.get("country_id")

    cities = City.objects.filter(country_id=countryId).values_list('id','name').order_by('name')
    context = {
        'cities': cities,
    }

    return render(request, 'elements/city.html', context)

def updateAmenity(request):
    is_select_all = request.POST.get("is_select_all")

    if is_select_all == 'true':
        amenData = Amenity.objects.all().values_list('id','name').order_by('name')

        context = {
            'amenData': amenData,
            'all': 1,
        }

    else:
        value = request.POST.get("value")
        numItems = request.POST.get("numItems")
        # print(int(numItems))
        if Amenity.objects.filter(id=value):
            amenData = Amenity.objects.get(id=value)

        count = 1
        if int(numItems) == 0:
            count = 0
        context = {
            'amenData': amenData,
            'id_val': value,
            'numItems': count,
            'all': 0,
        }

    return render(request, 'elements/amenity_list.html', context)

def updateEquipment(request):
    is_select_all = request.POST.get("is_select_all")

    if is_select_all == 'true':
        eqData = Equipment.objects.all().values_list('id','name').order_by('name')

        context = {
            'eqData': eqData,
            'all': 1,
        }

    else:
        value = request.POST.get("value")
        numItems = request.POST.get("numItems")
        # print(int(numItems))
        if Equipment.objects.filter(id=value):
            eqData = Equipment.objects.get(id=value)

        count = 1
        if int(numItems) == 0:
            count = 0
        context = {
            'eqData': eqData,
            'id_val': value,
            'numItems': count,
            'all': 0,
        }

    return render(request, 'elements/equipment_list.html', context)

def getCityList2(request):
    countryId = request.POST.get("country_id")

    cities = City.objects.filter(country_id=countryId).values_list('id','name').order_by('name')
    context = {
        'cities': cities,
    }

    return render(request, 'elements/city2.html', context)


def getCityList3(request):
    countryId = request.POST.get("country_id")

    cities = City.objects.filter(country_id=countryId).values_list('id','name').order_by('name')
    context = {
        'cities': cities,
    }

    return render(request, 'elements/city3.html', context)

def getTrainList(request):
    countries = Country.objects.all().values_list('id', 'name').order_by('name')

    context = {
        'countries': countries,
    }

    return render(request, 'elements/training_list.html', context)


def basicProfile(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES
    # data = request.POST['serializedData']
    print(data)

    # if data:
    #     explod(data,n)
    #     for records in data:

    print(data)
    # print(files)
    # print(data['facility_profile_level'])

    facility_profile_level = data.get("facility_profile_level")

    if facility_profile_level == 'Brand':
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        facility_type = data.get("facility_type")
        brand_name = data.get("brand_name")
        brand_address = data.get("brand_address")
        branch_id = data.get("branch_id")
        brand_id = data.get("brand_id")
        # print("dat brand_id",data)
        #
        # print("brand_id",brand_id)
        basic_info_id = data.get("basic_info_id")

        User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name)
        if brand_id == '':
            brands = Brand(
                # id=brand_id,
                user_id=user_id,
                brand_name=brand_name,
                brand_address=brand_address,

                slug=slugify(brand_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            brands = Brand(
                id=brand_id,
                user_id=user_id,
                brand_name=brand_name,
                brand_address=brand_address,

                slug=slugify(brand_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        brands.save()
        brand_id = brands.id
        # if branch_id == '':
        #     branch_id = None
        # print("facility_type",facility_type)
        if basic_info_id == '':
            basicInfo = BasicInfo(
                # id=basic_info_id,
                user_id=user_id,
                brand_id=brand_id,
                branch_id=branch_id,
                facility_profile_level=facility_profile_level,
                facility_type=facility_type,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            basicInfo = BasicInfo(
                id=basic_info_id,
                user_id=user_id,
                brand_id=brand_id,
                branch_id=branch_id,
                facility_profile_level=facility_profile_level,
                facility_type=facility_type,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

        basicInfo.save()

    elif facility_profile_level == 'Branch':

        # print(data)
        if request.session['user_type'] == "Personal Training Company":
            own_facility = data.get("own_facility")
            train_country = data.get("train_country")
            train_city = data.get("train_city")
            trainlocation = data.get("trainlocation")
            trainBlocation = data.get("trainBlocation")
            try:
                train_country2 = data.get("train_country2")
                train_city2 = data.get("train_city2")
                trainlocation2 = data.get("trainlocation2")
                trainBlocation2 = data.get("trainBlocation2")
            except:
                train_country2 = None
                train_city2 = None
                trainlocation2 = None
                trainBlocation2 = None
            if own_facility == 'on':
                own_facility = 1
            else:
                own_facility = 0
        else:
            train_country = None
            train_city = None
            trainlocation = None
            trainBlocation = None
            train_country2 = None
            train_city2 = None
            trainlocation2 = None
            trainBlocation2 = None
            own_facility = 0

        first_name = data.get("first_name_2")
        last_name = data.get("last_name_2")
        facility_type = data.get("facility_type_2")
        branch_name = data.get("branch_name")
        year_of_experince = data.get("year_of_experince")
        languages_array = data.getlist("languages")
        languages = ",".join(languages_array)
        training_type = data.get("training_type")
        website = data.get("website")
        about = data.get("about")
        short_bio = data.get("short_bio")
        website = data.get("website")
        location = data.get("location")
        country = data.get("country")
        city = data.get("city")
        key_skills_arr = data.getlist("key_skills")
        key_skills = ",".join(key_skills_arr)

        other_skills_arr = data.getlist("other_skills")
        other_skills = ",".join(other_skills_arr)

        amenities_arr = data.getlist("amenities[]")

        equipment_arr = data.getlist("equipments[]")

        # print(city)

        branch_id = data.get("branch_id_2")
        brand_id = data.get("brand_id_2")
        basic_info_id = data.get("basic_info_id")

        if brand_id == '':
            brand_id1 = 0
        else:
            brand_id1 = brand_id

        User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name,
                                               year_of_experince=year_of_experince, languages=languages)

        if branch_id != '':
            branch = Branch(
                id=branch_id,
                user_id=user_id,
                branch_name=branch_name,
                brand_id=brand_id1,

                slug=slugify(branch_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            branch = Branch(
                user_id=user_id,
                branch_name=branch_name,
                brand_id=brand_id1,

                slug=slugify(branch_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

        branch.save()

        branch_id = branch.id
        # print(basic_info_id)
        if basic_info_id != '':
            basicInfo = BasicInfo(
                id=basic_info_id,
                user_id=user_id,
                brand_id=brand_id,
                branch_id=branch_id,
                facility_profile_level=facility_profile_level,
                facility_type=facility_type,
                training_type=training_type,
                website=website,
                about=about,
                short_bio=short_bio,
                location=location,
                country=country,
                city=city,
                key_skills=key_skills,
                other_skills=other_skills,
                own_facility=own_facility,
                trainBlocation=trainBlocation,
                trainlocation=trainlocation,
                train_city=train_city,
                train_country=train_country,
                trainBlocation2=trainBlocation2,
                trainlocation2=trainlocation2,
                train_city2=train_city2,
                train_country2=train_country2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            basicInfo = BasicInfo(
                user_id=user_id,
                brand_id=brand_id,
                branch_id=branch_id,
                facility_profile_level=facility_profile_level,
                facility_type=facility_type,
                training_type=training_type,
                website=website,
                about=about,
                short_bio=short_bio,
                location=location,
                country=country,
                city=city,
                key_skills=key_skills,
                other_skills=other_skills,
                own_facility=own_facility,
                trainBlocation=trainBlocation,
                trainlocation=trainlocation,
                train_city=train_city,
                train_country=train_country,
                trainBlocation2=trainBlocation2,
                trainlocation2=trainlocation2,
                train_city2=train_city2,
                train_country2=train_country2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

        # print(basicInfo)
        basicInfo.save()

        if not amenities_arr:
            amenities_arr = data.get("amenities")

        UserAmenity.objects.filter(user_id=user_id).delete()
        if amenities_arr == None:
            amenities_arr = ''
        for amenity_id in amenities_arr:

            # print(amenity_id)

            quantity = data.get("ament_quantity[" + amenity_id + "]")
            visible_status = data.get("visible_status[" + amenity_id + "]")
            if quantity == None:
                quantity = 1
            if visible_status == None:
                visible_status = 'Yes'

            user_amenity = UserAmenity(
                user_id=user_id,
                amenity_id=amenity_id,
                quantity=quantity,
                visible_status=visible_status,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            user_amenity.save()

        # print(data)def
        # print(equipment_arr)

        if not equipment_arr:
            equipment_arr = data.get("equipments")

        UserEquipment.objects.filter(user_id=user_id).delete()
        if equipment_arr == None:
            equipment_arr = ''
        for e_id in equipment_arr:
            # print(e_id)

            quantity = data.get("eq_quantity[" + e_id + "]")
            max_value = data.get("eq_max[" + e_id + "]")
            eq_visible_status = data.get("eq_visible_status[" + e_id + "]")
            # print(quantity)
            # print(max_value)
            if quantity == None:
                quantity = 1
            if eq_visible_status == None:
                eq_visible_status = 'Yes'

            user_equip = UserEquipment(
                user_id=user_id,
                equipment_id=e_id,
                quantity=quantity,
                max_value=max_value,
                visible_status=eq_visible_status,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            user_equip.save()
    else:
        if request.session['user_type'] == "Personal Training Company":
            own_facility = data.get("own_facility")
            train_country = data.get("train_country")
            train_city = data.get("train_city")
            trainlocation = data.get("trainlocation")
            trainBlocation = data.get("trainBlocation")
            try:
                train_country2 = data.get("train_country2")
                train_city2 = data.get("train_city2")
                trainlocation2 = data.get("trainlocation2")
                trainBlocation2 = data.get("trainBlocation2")
            except:
                train_country2 = None
                train_city2 = None
                trainlocation2 = None
                trainBlocation2 = None
            if own_facility == 'on':
                own_facility = 1
            else:
                own_facility = 0
        else:
            train_country = None
            train_city = None
            trainlocation = None
            trainBlocation = None
            own_facility = 0
            train_country2 = None
            train_city2 = None
            trainlocation2 = None
            trainBlocation2 = None

        facility_type = data.get("facility_type_3")
        brand_name = data.get("brand_name_3")
        brand_address = data.get("brand_address_3")
        branch_name = data.get("branch_name_3")
        # brand_id_2 = data.get("brand_id_2")
        # print(brand_name)
        first_name = data.get("first_name_2")
        last_name = data.get("last_name_2")
        # facility_type = data.get("facility_type_2")
        # branch_name = data.get("branch_name")
        year_of_experince = data.get("year_of_experince")
        languages_array = data.getlist("languages")

        languages = ",".join(languages_array)
        training_type = data.get("training_type")
        website = data.get("website")
        about = data.get("about")
        short_bio = data.get("short_bio")
        website = data.get("website")
        location = data.get("location")
        country = data.get("country")
        city = data.get("city")
        key_skills_arr = data.getlist("key_skills")
        key_skills = ",".join(key_skills_arr)

        other_skills_arr = data.getlist("other_skills")
        other_skills = ",".join(other_skills_arr)

        amenities_arr = data.getlist("amenities")

        equipment_arr = data.getlist("equipments")

        # print(city)

        branch_id = data.get("branch_id_3")
        brand_id = data.get("brand_id_3")
        basic_info_id = data.get("basic_info_id")
        old_bio_video = data.get("old_bio_video")

        User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name,
                                               year_of_experince=year_of_experince, languages=languages)
        if brand_id == "None":
            brand_id = ''
        if brand_id != '':

            brands = Brand(
                id=brand_id,
                user_id=user_id,
                brand_name=brand_name,
                brand_address=brand_address,

                slug=slugify(brand_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            brands.save()
        else:
            brands = Brand(
                user_id=user_id,
                brand_name=brand_name,
                brand_address=brand_address,

                slug=slugify(brand_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            brands.save()

        brand_id = brands.id

        # print('brand  ',branch_id)
        if branch_id == 'None':
            # print("hello")
            branch_id = ''
        if branch_id != '':
            # print("-------",branch_id)
            branch = Branch(
                id=branch_id,
                brand_id=brand_id,
                user_id=user_id,
                branch_name=branch_name,

                slug=slugify(branch_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            # print("--++++++=-----")
            branch = Branch(
                user_id=user_id,
                brand_id=brand_id,
                branch_name=branch_name,
                slug=slugify(branch_name + "-" + rand_slug()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

        branch.save()
        branch_id = branch.id
        # print(files)
        file_name = old_bio_video
        if files:
            fss = FileSystemStorage()
            bio_video = files['bio_video']
            # print(bio_video)
            file_name = str(bio_video)
            file = fss.save('static/uploads/bioVideo/' + str(bio_video), bio_video)
            file_url = fss.url(file)
            # print('files',file,file_url)

        if basic_info_id != '':
            basicInfo = BasicInfo(
                id=basic_info_id,
                user_id=user_id,
                brand_id=brand_id,
                branch_id=branch_id,
                facility_profile_level=facility_profile_level,
                facility_type=facility_type,
                training_type=training_type,
                website=website,
                about=about,
                short_bio=short_bio,
                location=location,
                country=country,
                own_facility=own_facility,
                city=city,
                key_skills=key_skills,
                other_skills=other_skills,
                bio_video=file_name,
                trainBlocation=trainBlocation,
                trainlocation=trainlocation,
                train_city=train_city,
                train_country=train_country,
                trainBlocation2=trainBlocation2,
                trainlocation2=trainlocation2,
                train_city2=train_city2,
                train_country2=train_country2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            basicInfo = BasicInfo(
                user_id=user_id,
                brand_id=brand_id,
                branch_id=branch_id,
                own_facility=own_facility,
                facility_profile_level=facility_profile_level,
                facility_type=facility_type,
                training_type=training_type,
                website=website,
                about=about,
                short_bio=short_bio,
                location=location,
                country=country,
                city=city,
                key_skills=key_skills,
                other_skills=other_skills,
                bio_video=file_name,
                trainBlocation=trainBlocation,
                trainlocation=trainlocation,
                train_city=train_city,
                trainBlocation2=trainBlocation2,
                trainlocation2=trainlocation2,
                train_city2=train_city2,
                train_country2=train_country2,
                train_country=train_country,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

        basicInfo.save()

        if not amenities_arr:
            amenities_arr = data.get("amenities")

        UserAmenity.objects.filter(user_id=user_id).delete()
        if amenities_arr == None:
            amenities_arr = ''
        for amenity_id in amenities_arr:

            # print(amenity_id)

            quantity = data.get("ament_quantity[" + amenity_id + "]")
            visible_status = data.get("visible_status[" + amenity_id + "]")
            if quantity == None:
                quantity = 1
            if visible_status == None:
                visible_status = 'Yes'

            user_amenity = UserAmenity(
                user_id=user_id,
                amenity_id=amenity_id,
                quantity=quantity,
                visible_status=visible_status,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            user_amenity.save()

        # print(data)def
        # print(equipment_arr)

        if not equipment_arr:
            equipment_arr = data.get("equipments")

        UserEquipment.objects.filter(user_id=user_id).delete()
        if equipment_arr == None:
            equipment_arr = ''
        for e_id in equipment_arr:
            # print(e_id)
            quantity = data.get("eq_quantity[" + e_id + "]")
            max_value = data.get("eq_max[" + e_id + "]")
            eq_visible_status = data.get("eq_visible_status[" + e_id + "]")
            # print(quantity)
            # print(max_value)
            if quantity == None:
                quantity = 1
            if eq_visible_status == None:
                eq_visible_status = 'Yes'

            user_equip = UserEquipment(
                user_id=user_id,
                equipment_id=e_id,
                quantity=quantity,
                max_value=max_value,
                visible_status=eq_visible_status,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            user_equip.save()
        # print("basic_info",basicInfo.bio_video)
    brand_name = ''
    branch_name = ''
    try:
        brand_name = basicInfo.brand.brand_name
    except:
        brand_name = ''
    try:
        branch_name = basicInfo.branch.branch_name
    except:
        branch_name = ''


    # if basicInfo.brand.brand_name:
    #     brand_name = basicInfo.brand.brand_name
    # if basicInfo.branch.branch_name:
    #     branch_name = basicInfo.branch.branch_name
    context = {
        0: basicInfo.id, 1: facility_profile_level, 2: basicInfo.bio_video, 3:brand_name,4:branch_name
    }
    return JsonResponse(context)

def awardProfile(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES

    award_name = data.get("award_name")
    location = data.get("award_location")
    award_date = data.get("award_date")
    file_name = ''
    date_val = ''

    try:
        if bool(files['award_document']):
            award_document = files['award_document']
    except:
        award_document = ''

    try:
        if bool(award_date):
            date_val = date.datetime.strptime(award_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        date_val = ''

    if award_document:
        fss = FileSystemStorage()
        # print(award_document)
        # fileExtension = os.path.splitext(str(award_document))
        # print(fileExtension)
        # ext = award_document.split(".")[-1]
        # file_name = award_document
        # print(os.path.splitext(file_name))
        file_name = rand_slug() + "-" + str(award_document) 
        file = fss.save('static/uploads/documents/'+file_name, award_document)
        file_url = fss.url(file)

    awards = UserAward(
        user_id=user_id,
        award_name=award_name,
        location=location,
        document=file_name,
        status=1,
        date=date_val,
        
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    awards.save()

    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    context = {
        'awardList': awardInfo,
    }

    return render(request, 'elements/users/award_table.html', context)

def saveAvailability(request):
    if request.method == 'POST':
        data = request.POST       

        user_id = request.session['user_id']

        dayArr = data.getlist("serializedData[day_name][]")

        # Availability.objects.filter(user_id=user_id).delete()
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

                if Availability.objects.filter(user_id=user_id,day_name=day):
                    Availability.objects.filter(user_id=user_id,day_name=day).update(start_time=start_arr_json,end_time=end_arr_json)
                else:
                    record = Availability(
                        user_id=user_id,
                        day_name=day,
                        start_time=start_arr_json,
                        end_time=end_arr_json,

                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )

                    record.save()

                day_array.remove(day)
            else:
                Availability.objects.filter(user_id=user_id).delete()

            for day in day_array:
                Availability.objects.filter(user_id=user_id,day_name=day).delete()

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

                if Availability.objects.filter(user_id=user_id,day_name=day):
                    Availability.objects.filter(user_id=user_id,day_name=day).update(start_time=start_arr_json,end_time=end_arr_json)
                else:
                    record = Availability(
                        user_id=user_id,
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
                Availability.objects.filter(user_id=user_id,day_name=day).delete()


    return HttpResponse(1)

def saveAvail(request):
    if request.method == 'POST':
        data = request.POST       

        user_id = request.session['user_id']
        uncheck = data.get("uncheck")
        day = data.get("day")

        if Availability.objects.filter(user_id=user_id,day_name=day):
            Availability.objects.filter(user_id=user_id,day_name=day).update(status=uncheck)

    return HttpResponse(1)

def calenderPost(request):
    user_id = request.session['user_id']
    data = request.POST

    date_Arr = data.get("serializedData[selected_values]")

    aList = json.loads(date_Arr)
    for x in aList:
        chk_date = date.datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")
        # print(chk_date)
        start_arr = data.getlist("serializedData[over_start_time[]][]")
        end_arr = data.getlist("serializedData[over_end_time[]][]")
        if not start_arr:
            start_arr_json = '["'+data.get("serializedData[over_start_time[]]")+'"]'
            end_arr_json = '["'+data.get("serializedData[over_end_time[]]")+'"]'                
        else:
            start_arr_json = json.dumps(start_arr)
            end_arr_json = json.dumps(end_arr)

        if OverAvailability.objects.filter(user_id=user_id,date=chk_date):
            OverAvailability.objects.filter(user_id=user_id,date=chk_date).update(start_time=start_arr_json,end_time=end_arr_json)
        else:
            record = OverAvailability(
                user_id=user_id,
                date=chk_date,
                start_time=start_arr_json,
                end_time=end_arr_json,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            record.save()

    return HttpResponse(1)

def checkCalVal(request):
    data = request.POST
    user_id = request.session['user_id']

    today_date = data.get("date[]")
    new_today_date = date.datetime.strptime(today_date, "%m/%d/%Y").strftime("%Y-%m-%d")

    # basicinfo = OverAvailability.objects.get(user_id=user_id)
    avail_values = OverAvailability.objects.filter(user_id=user_id,date=new_today_date)

    if not avail_values:
        day = date.datetime.strptime(today_date, "%m/%d/%Y").strftime("%a")
        avail_values = Availability.objects.filter(user_id=user_id,day_name=day,status=0)        
        queries = avail_values
            
        if not avail_values:
            queries = 0
    else:
        queries = avail_values
        # for values in avail_values:
        #     startList = json.loads(values.start_time)
        #     endList = json.loads(values.end_time)
        #     # new_list = zip(startList, endList)
        #     # print(values.start_time)
        #     # print(values.end_time)
        #     # print(new_list)
        #     # print(set(new_list))
        #     for a, b in zip(startList, endList):
        #         print(a)
        #         print(b)
        
    context = {
        'queries' : queries
    } 

    # print(data)
    # print(avail_values)
    return render(request, 'elements/calender_section.html', context)

def deleteOver(request):
    data = request.POST
    user_id = request.session['user_id']

    dates = data.get("dates")
    aList = json.loads(dates)
    for x in aList:
        
        dateVal = date.datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")
        OverAvailability.objects.filter(user_id=user_id, date = dateVal).delete()

    return HttpResponse(1)

def deleteAward(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    UserAward.objects.filter(id=id).delete()

    return HttpResponse(1)

def viewAward(request):
    data = request.POST
    data = request.POST

    id = data.get("id")
    awardValue = UserAward.objects.get(id=id)

    countries = Country.objects.all().values_list('id','name').order_by('name')

    context = {
        'awardValue': awardValue,
        'countries': countries,
    }
    
    return render(request, 'elements/users/award_model.html', context)

def editAwardProfile(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES

    # print(data)
    # print(files)

    award_name = data.get("award_title")
    location = data.get("award_location")
    award_date = data.get("award_date")
    id = data.get("award_id")

    file_name = data.get("old_award_document")
    if files:
        fss = FileSystemStorage()
        award_document = files['edit_award_document']
        file_name = rand_slug() + "-" + str(award_document) 
        file = fss.save('static/uploads/documents/'+file_name, award_document)
        file_url = fss.url(file)

    awards = UserAward(
        id=id,
        user_id=user_id,
        award_name=award_name,
        location=location,
        document=file_name,
        date=date.datetime.strptime(award_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
        
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    awards.save()

    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    context = {
        'awardList': awardInfo,
    }

    return render(request, 'elements/users/award_table.html', context)

def viewCopy(request):
    data = request.POST

    id = data.get("id")
    
    return render(request, 'elements/users/copy_cal_section.html')

# userMediaAdd**********
def mediaSocialMedia(request):
    data = request.POST

    # print(data)
    files = request.FILES
    faceBookUrl = data["facebookLink"]
    user_id = request.session['user_id']
    twitterUrl = data["twitterLink"]
    instagramUrl = data["instagramLink"]
    mediaTitle = data["mediaTitle"]

    try:
        if bool(files['profile_photo']):
            profile_image = files['profile_photo']
    except:
        profile_image = ''
    try:
        tile_image = files['tile_image']
    except:
        tile_image = ''
    try:
        virtual_tour = files['virtual_tour']
    except:
        virtual_tour = ''
    try:
        myMedia = files['myMedia[]']
    except:
        myMedia = ''

    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    User.objects.filter(id=user_id).update(facebookLink=faceBookUrl,twitterLink=twitterUrl,instagramLink=instagramUrl)
    

    isUpdateProfile = ''
    if data['profile_photoold'] == '' and profile_image != '':
            fss = FileSystemStorage()
            file_name = rand_slug() + "-" + str(profile_image)
            isUpdateProfile = file_name
            file_image = fss.save('static/uploads/profile/'+file_name, profile_image)
            serMediaRecord= UserMediaRecord(user_id=user_id,type='ProfilePhoto',status=0,data=file_name,created_at=datetime.utcnow(),updated_at=datetime.utcnow())
            serMediaRecord.save()
        # //insert
    elif profile_image == '':
        sd =''
        # //nothing

        # print("2")
    else:
        fss = FileSystemStorage()
        file_name = rand_slug() + "-" + str(profile_image) 
        file_image = fss.save('static/uploads/profile/'+file_name, profile_image)
        UserMediaRecord.objects.filter(user_id=user_id,type='ProfilePhoto').update(data=file_name,updated_at=datetime.utcnow())
            # //update
    isUpdateTile = ''
    if data['tile_imageold'] == '' and tile_image != '':
        fss = FileSystemStorage()
        file_name = rand_slug() + "-" + str(tile_image)
        isUpdateTile = file_name
        file_image = fss.save('static/uploads/profile/'+file_name, tile_image)
        serMediaRecord= UserMediaRecord(user_id=user_id,type='tile_image',status=0,data=file_name,created_at=datetime.utcnow(),updated_at=datetime.utcnow())
        serMediaRecord.save()
        # //insert
    elif tile_image == '':
        # //nothing
        sd = ''
        # print("2")
    else:
        fss = FileSystemStorage()
        file_name = rand_slug() + "-" + str(tile_image) 
        file_image = fss.save('static/uploads/profile/'+file_name, tile_image)
        UserMediaRecord.objects.filter(user_id=user_id,type='tile_image').update(data=file_name,updated_at=datetime.utcnow())
            # //update

    isUpdateVirtual = ''
    auth = User.objects.get(id=user_id)
    virName = ''

    if auth.user_type == "Gym or Studio":
        if data['virtual_tourold'] == '' and virtual_tour != '' :
            fss = FileSystemStorage()
            file_name = rand_slug() + "-" + str(virtual_tour)
            isUpdateVirtual = file_name
            virName=file_name
            file_image = fss.save('static/uploads/virtualTour/'+file_name, virtual_tour)
            serMediaRecord= UserMediaRecord(user_id=user_id,type='virtual_tour',status=0,data=file_name,created_at=datetime.utcnow(),updated_at=datetime.utcnow())
            serMediaRecord.save()
            # //insert
        elif virtual_tour == '':
            te = "nothing"
            # print("2")

            # //nothing
        else:
            fss = FileSystemStorage()
            file_name = rand_slug() + "-" + str(virtual_tour)
            virName = file_name
            file_image = fss.save('static/uploads/virtualTour/'+file_name, virtual_tour)
            UserMediaRecord.objects.filter(user_id=user_id,type='virtual_tour').update(data=file_name,updated_at=datetime.utcnow())
            # //update
    context = {
        0:isUpdateTile,1:isUpdateVirtual,2:isUpdateProfile,3:virName
        }


    return JsonResponse(context)

def edit_media_media(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES
    edit_id = data['edit_id']
    media_title= data['media_title']
    try:
        myMedia = files['edit_media_media']
    except:
        myMedia = ''
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    mediaSocialMedia=UserMediaRecord.objects.all().filter(user_id=user_id,type="myMedia[]").values()

    context={
        'mediaSocialMedia':mediaSocialMedia
    }
    if myMedia == '':
        UserMediaRecord.objects.filter(id=edit_id).update(mediaTitle=media_title,updated_at=datetime.utcnow())
        # print(1)
        return render(request, 'elements/users/media_table.html', context)
    if myMedia != '':
        fss = FileSystemStorage()
        file_name = rand_slug() + "-" + str(myMedia) 
        file_image = fss.save('static/uploads/media/'+file_name, myMedia)
        UserMediaRecord.objects.filter(id=edit_id).update(mediaTitle=media_title,data=file_name,updated_at=datetime.utcnow())
        # print(2)
        return render(request, 'elements/users/media_table.html', context)
        
    
    return  render(request, 'elements/users/media_table.html', context)

def deleteMedia(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST
    id = data.get("id")
    UserMediaRecord.objects.filter(id=id).delete()
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    mediaSocialMedia = UserMediaRecord.objects.all().filter(user_id=user_id, type="myMedia[]").values()

    context = {
        'mediaSocialMedia': mediaSocialMedia
    }
    return  render(request, 'elements/users/media_table.html', context)

def addPricing(request):
    data = request.POST
    # print(data)

    user_id = request.session['user_id']

    categroy_type= int(data['categroy_type'])
    if categroy_type == 1:
        type_of_session = data['type_of_session_1']
        session_type = data['session_type_1']
        number_of_people = data['number_of_people_1']
        session_name = data['session_name_1']
        number_of_session = data['number_of_session_1']
        duration = data['duration_1']
        validity = data['validity_1']
        validity_type = data['validity_type_1']
        currency = data['currency_1']
        price = data['price_1']
        location = data['location_1']
        assign_employee = data['assign_employee_1']
        notes = data['notes_1']
        
        record = UserPrice(
            user_id=user_id,
            session_category=categroy_type,
            type_of_session=type_of_session,
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            number_of_session=number_of_session,
            duration=duration,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,
            type_of_amenity=0,
            sport_type=0,
            number_of_participant=0,

            slug=slugify(session_name + "-" + rand_slug()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()
    elif categroy_type == 2:
        type_of_session = data['type_of_service_2']
        session_type = data['session_type_2']
        number_of_people = data['number_of_people_2']
        session_name = data['service_name_2']
        number_of_session = data['number_of_services_2']
        duration = data['duration_2']
        validity = data['validity_2']
        validity_type = data['validity_type_2']
        currency = data['currency_2']
        price = data['price_2']
        location = data['location_2']
        assign_employee = data['assign_employee_2']
        notes = data['notes_2']
        
        record = UserPrice(
            user_id=user_id,
            session_category=categroy_type,
            type_of_session=type_of_session,
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            number_of_session=number_of_session,
            duration=duration,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,
            type_of_amenity=0,
            sport_type=0,
            number_of_participant=0,

            slug=slugify(session_name + "-" + rand_slug()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    elif categroy_type == 3:
        session_type = data['session_type_3']
        number_of_people = data['number_of_people_3']
        session_name = data['day_pass_name_3']
        validity = data['validity_3']
        validity_type = data['validity_type_3']
        currency = data['currency_3']
        price = data['price_3']
        location = data['location_3']
        # what_included = data['what_included_3']
        what_included_arr = data.getlist("what_included_3") 
        what_included = ",".join( what_included_arr )

        try:
            inclusive_class = data['inclusive_class_3']
        except:
            inclusive_class = 'Yes'

        notes = data['notes_3']
        
        record = UserPrice(
            user_id=user_id,
            session_category=categroy_type,
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,
            what_included=what_included,
            inclusive_class=inclusive_class,
            type_of_amenity=0,
            sport_type=0,
            number_of_participant=0,

            slug=slugify(session_name + "-" + rand_slug()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()
    
    elif categroy_type == 4:
        session_type = data['session_type_4']
        number_of_people = data['number_of_people_4']
        session_name = data['membership_name_4']
        validity = data['validity_4']
        validity_type = data['validity_type_4']
        currency = data['currency_4']
        price = data['price_4']
        location = data['location_4']
        # what_included = data['what_included_4']
        what_included_arr = data.getlist("what_included_4") 
        what_included = ",".join( what_included_arr )
        try:
            inclusive_class = data['inclusive_class_4']
        except:
            inclusive_class = 'Yes'

        notes = data['notes_4']
        
        record = UserPrice(
            user_id=user_id,
            session_category=categroy_type,
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,
            what_included=what_included,
            inclusive_class=inclusive_class,
            type_of_amenity=0,
            sport_type=0,
            number_of_participant=0,

            slug=slugify(session_name + "-" + rand_slug()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()
    
    elif categroy_type == 5:
        type_of_amenity = data['type_of_amenity']
        sport_type = data['sport_type']
        number_of_participant = data['number_of_participant']
        booking_length = data['booking_length']
        validity_type = data['validity_type_4']
        currency = data['currency_5']
        price = data['price_5']
        location = data['location_5']

        notes = data['notes_5']
        
        record = UserPrice(
            user_id=user_id,
            session_category=categroy_type,
            type_of_amenity=type_of_amenity,
            sport_type=sport_type,
            number_of_participant=number_of_participant,
            booking_length=booking_length,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,

            slug=slugify(type_of_amenity + "-" + rand_slug()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    amenityTypes = BookableAmenity.objects.all().values_list('id','name').order_by('name')
    priceList = UserPrice.objects.filter(user_id=user_id).values()

    context = {
        'amenityTypes': amenityTypes,
        'priceList': priceList,
    }

    return render(request, 'elements/users/user_price_table.html', context)

def deletePrice(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    UserPrice.objects.filter(id=id).delete()
    amenityTypes = BookableAmenity.objects.all().values_list('id','name').order_by('name')
    priceList = UserPrice.objects.filter(user_id=user_id).values()

    context = {
        'amenityTypes': amenityTypes,
        'priceList': priceList,
    }
    return render(request, 'elements/users/user_price_table.html', context)

def viewPrice(request):
    data = request.POST

    user_id = request.session['user_id']

    id = data.get("id")
    priceRecords = UserPrice.objects.get(id=id)

    basicinfo = ''
    if BasicInfo.objects.filter(user_id=user_id):
        basicinfo = BasicInfo.objects.get(user_id=user_id)
    services = Service.objects.all().values_list('id','name').order_by('name')
    sesstionTypes = Session.objects.all().values_list('id','name').order_by('name')
    serviceAmenityTypes = ServiceAmenity.objects.all().values_list('id','name').order_by('name')
    amenityTypes = BookableAmenity.objects.all().values_list('id','name').order_by('name')
    sports = Sport.objects.all().values_list('id','name').order_by('name')

    context = {
        'sesstionTypes': sesstionTypes,
        'serviceAmenityTypes': serviceAmenityTypes,
        'amenityTypes': amenityTypes,
        'sports': sports,
        'priceRecord': priceRecords,
        'basicinfo': basicinfo,
        'services': services,
    }
    
    return render(request, 'elements/users/user_price_model.html', context)

def editPricing(request):
    user_id = request.session['user_id']
    data = request.POST

    print(data)

    price_id= int(data['price_id'])
    categroy_type= int(data['categroy_type'])

    # return HttpResponse(1)
    if categroy_type == 1:
        type_of_session = data['type_of_session_1']
        session_type = data['session_type_1']
        number_of_people = data['number_of_people_1']
        session_name = data['session_name_1']
        number_of_session = data['number_of_session_1']
        duration = data['duration_1']
        validity = data['validity_1']
        validity_type = data['validity_type_1']
        currency = data['currency_1']
        price = data['price_1']
        location = data['location_1']
        assign_employee = data['assign_employee_1']
        notes = data['notes_1']
        
        UserPrice.objects.filter(id=price_id).update(
            type_of_session=type_of_session,
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            number_of_session=number_of_session,
            duration=duration,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,

            updated_at=datetime.utcnow()
        )
    elif categroy_type == 2:
        type_of_session = data['type_of_service_2']
        session_type = data['session_type_2']
        number_of_people = data['number_of_people_2']
        session_name = data['service_name_2']
        number_of_session = data['number_of_services_2']
        duration = data['duration_2']
        validity = data['validity_2']
        validity_type = data['validity_type_2']
        currency = data['currency_2']
        price = data['price_2']
        location = data['location_2']
        assign_employee = data['assign_employee_2']
        notes = data['notes_2']
        
        UserPrice.objects.filter(id=price_id).update(
            type_of_session=type_of_session,
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            number_of_session=number_of_session,
            duration=duration,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,

            updated_at=datetime.utcnow()
        )

    elif categroy_type == 3:
        session_type = data['session_type_3']
        number_of_people = data['number_of_people_3']
        session_name = data['day_pass_name_3']
        validity = data['validity_3']
        validity_type = data['validity_type_3']
        currency = data['currency_3']
        price = data['price_3']
        location = data['location_3']
        # what_included = data['what_included_3']
        what_included_arr = data.getlist("what_included_3") 
        what_included = ",".join( what_included_arr )

        try:
            inclusive_class = data['inclusive_class_3']
        except:
            inclusive_class = 'Yes'

        notes = data['notes_3']

        UserPrice.objects.filter(id=price_id).update(
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,
            what_included=what_included,
            inclusive_class=inclusive_class,

            updated_at=datetime.utcnow()
        )
    
    elif categroy_type == 4:
        session_type = data['session_type_4']
        number_of_people = data['number_of_people_4']
        session_name = data['membership_name_4']
        validity = data['validity_4']
        validity_type = data['validity_type_4']
        currency = data['currency_4']
        price = data['price_4']
        location = data['location_4']
        # what_included = data['what_included_4']
        what_included_arr = data.getlist("what_included_4") 
        what_included = ",".join( what_included_arr )
        try:
            inclusive_class = data['inclusive_class_4']
        except:
            inclusive_class = 'Yes'

        notes = data['notes_4']

        UserPrice.objects.filter(id=price_id).update(
            session_type=session_type,
            number_of_people=number_of_people,
            session_name=session_name,
            validity=validity,
            validity_type=validity_type,
            currency=currency,
            price=price,
            location=location,
            notes=notes,
            what_included=what_included,
            inclusive_class=inclusive_class,

            updated_at=datetime.utcnow()
        )
    
    elif categroy_type == 5:
        type_of_amenity = data['type_of_amenity']
        sport_type = data['sport_type']
        number_of_participant = data['number_of_participant']
        booking_length = data['booking_length']
        currency = data['currency_5']
        price = data['price_5']
        location = data['location_5']

        notes = data['notes_5']

        UserPrice.objects.filter(id=price_id).update(
            type_of_amenity=type_of_amenity,
            sport_type=sport_type,
            number_of_participant=number_of_participant,
            booking_length=booking_length,
            currency=currency,
            price=price,
            location=location,
            notes=notes,

            updated_at=datetime.utcnow()
        )

    amenityTypes = BookableAmenity.objects.all().values_list('id','name').order_by('name')
    priceList = UserPrice.objects.filter(user_id=user_id).values()

    context = {
        'amenityTypes': amenityTypes,
        'priceList': priceList,
    }

    # return HttpResponse(1)

    return render(request, 'elements/users/user_price_table.html', context)

def identityForm(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES
    # print(data)

    terms = 1
    old_business_doc = data['old_business_doc']
    old_director_doc = data['old_director_doc']

    try:
        business_doc = files['business_doc']
        fss = FileSystemStorage()
        business_doc_name = rand_slug() + "-" + str(business_doc) 
        file_image = fss.save('static/uploads/documents/'+business_doc_name, business_doc)
    except:
        business_doc_name = old_business_doc

    try:
        director_doc = files['director_doc']
        fss = FileSystemStorage()
        director_doc_name = rand_slug() + "-" + str(director_doc) 
        file_image = fss.save('static/uploads/documents/'+director_doc_name, director_doc)
    except:
        director_doc_name = old_director_doc

    User.objects.filter(id=user_id).update(terms=terms,business_doc=business_doc_name,director_doc=director_doc_name,updated_at=datetime.utcnow())

    return HttpResponse(1)

def updateMedia(request):
    data = request.POST
    user_id = request.session['user_id']
    files = request.FILES
    # print(files)
    myMedia = files["myMedia"]
    mediaTitle = data.get("mediaTitle")
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    if myMedia != '':
        # print(1231123)
        fss = FileSystemStorage()
        fss = FileSystemStorage()
        file_name = rand_slug() + "-" + str(myMedia)
        # print("file_name",file_name)
        file_image = fss.save('static/uploads/media/'+file_name, myMedia)
        serMediaRecord= UserMediaRecord(user_id=user_id,mediaTitle=mediaTitle,type='myMedia[]',status=0,data=file_name,created_at=datetime.utcnow(),updated_at=datetime.utcnow())
        serMediaRecord.save()

    mediaSocialMedia=UserMediaRecord.objects.all().filter(user_id=user_id,type="myMedia[]").values()

    context = {
        'mediaSocialMedia': mediaSocialMedia
    }
    return render(request, 'elements/users/media_table.html', context)

def clientTransformation(request):
    data = request.POST
    user_id = request.session['user_id']
    files = request.FILES
    # print("data",data)
    # print("files",files)
    client_name = data["client_name"].strip()
    client_description = data["client_Description"].strip()

    try:
        if bool(files['client_ProfileImage']):
            client_ProfileImage = files['client_ProfileImage']
            fss = FileSystemStorage()
            file_name_client_ProfileImage = rand_slug() + "-" + str(client_ProfileImage)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_ProfileImage, client_ProfileImage)
    except:
        file_name_client_ProfileImage = ''

    try:
        if bool(files['client_BeforeImageFront']):
            client_BeforeImageFront = files['client_BeforeImageFront']
            fss = FileSystemStorage()
            file_name_client_BeforeImageFront = rand_slug() + "-" + str(client_BeforeImageFront)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_BeforeImageFront, client_BeforeImageFront)
    except:
        file_name_client_BeforeImageFront = ''

    try:
        if bool(files['client_BeforeImageSide']):
            client_BeforeImageSide = files['client_BeforeImageSide']
            fss = FileSystemStorage()
            file_name_client_BeforeImageSide = rand_slug() + "-" + str(client_BeforeImageSide)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_BeforeImageSide, client_BeforeImageSide)
    except:
        file_name_client_BeforeImageSide = ''

    try:
        if bool(files['client_BeforeImageBack']):
            client_BeforeImageBack = files["client_BeforeImageBack"]
            fss = FileSystemStorage()
            file_name_client_BeforeImageBack = rand_slug() + "-" + str(client_BeforeImageBack)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_BeforeImageBack, client_BeforeImageBack)
    except:
        file_name_client_BeforeImageBack = ''

    try:
        if bool(files['client_AfterImageFront']):
            client_AfterImageFront = files["client_AfterImageFront"]
            fss = FileSystemStorage()
            file_name_client_AfterImageFront = rand_slug() + "-" + str(client_AfterImageFront)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_AfterImageFront, client_AfterImageFront)
    except:
        file_name_client_AfterImageFront = ''

    try:
        if bool(files['client_AfterImageFrontSide']):
            client_AfterImageFrontSide = files["client_AfterImageFrontSide"]
            fss = FileSystemStorage()
            file_name_client_AfterImageFrontSide = rand_slug() + "-" + str(client_AfterImageFrontSide)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_AfterImageFrontSide, client_AfterImageFrontSide)
    except:
        file_name_client_AfterImageFrontSide = ''

    try:
        if bool(files['client_AfterImageFrontBack']):
            client_AfterImageFrontBack = files["client_AfterImageFrontBack"]
            fss = FileSystemStorage()
            file_name_client_AfterImageFrontBack = rand_slug() + "-" + str(client_AfterImageFrontBack)
            file_image = fss.save('static/uploads/client_media/' + file_name_client_AfterImageFrontBack, client_AfterImageFrontBack)
    except:
        file_name_client_AfterImageFrontBack = ''

    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    serClientTransformation = UserClientTransformation(user_id=user_id, status=0,
                                                       image=file_name_client_ProfileImage,
                                                       description= client_description,
                                                       name= client_name,
                                                       beforeimage_front=file_name_client_BeforeImageFront,
                                                       beforeimage_back=file_name_client_BeforeImageBack,
                                                       beforeimage_side=file_name_client_BeforeImageSide,
                                                       afterimage_front=file_name_client_AfterImageFront,
                                                       afterimage_side=file_name_client_AfterImageFrontSide,
                                                       afterimage_back=file_name_client_AfterImageFrontBack,
                                                       slug=slugify(client_name + "-" + rand_slug()),
                                     created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    serClientTransformation.save()
    userClientTransformationData=UserClientTransformation.objects.all().filter(user_id=user_id).values()
    context = {
        'userClientTransformationData': userClientTransformationData
    }
    return render(request, 'elements/myProfile/clientTransformation.html', context)

def deleteClientTransformation(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    UserClientTransformation.objects.filter(id=id).delete()
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    userClientTransformationData = UserClientTransformation.objects.all().filter(user_id=user_id).values()
    context = {
        'userClientTransformationData': userClientTransformationData
    }
    return render(request, 'elements/users/client_table.html', context)

def updateClientTransformationSubmit(request):
    data = request.POST
    files = request.FILES
    user_id = request.session['user_id']
    edit_id = data["id"]
    name = data["client_name_id"].strip()
    description = data["client_Description_id"].strip()
    client_ProfileImageOldEdit = data["client_ProfileImageOldEdit"]
    UserClientTransformation.objects.filter(id=edit_id).update(name=name, description=description,
                                                               updated_at=datetime.utcnow())
    try:
        client_ProfileImageEdit = files["client_ProfileImageEdit"]
    except:
        client_ProfileImageEdit = ''
    if client_ProfileImageEdit != '':
        fss = FileSystemStorage()
        file_name_client_ProfileImage = rand_slug() + "-" + str(client_ProfileImageEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_ProfileImage, client_ProfileImageEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(image=file_name_client_ProfileImage,
                                                          updated_at=datetime.utcnow())
    client_BeforeImageFrontOldEdit = data["client_BeforeImageFrontOldEdit"]
    try:
        client_BeforeImageFrontEdit = files["client_BeforeImageFrontEdit"]
    except:
        client_BeforeImageFrontEdit = ''
    if client_BeforeImageFrontEdit != '':
        fss = FileSystemStorage()
        file_name_client_BeforeImageFrontEdit = rand_slug() + "-" + str(client_BeforeImageFrontEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_BeforeImageFrontEdit, client_BeforeImageFrontEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(beforeimage_front=file_name_client_BeforeImageFrontEdit,
                                                                   updated_at=datetime.utcnow())
    try:
        client_BeforeImageSideEdit = files["client_BeforeImageSideEdit"]
    except:
        client_BeforeImageSideEdit = ''
    if client_BeforeImageSideEdit != '':
        fss = FileSystemStorage()
        file_name_client_BeforeImageSideEdit = rand_slug() + "-" + str(client_BeforeImageSideEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_BeforeImageSideEdit, client_BeforeImageSideEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(beforeimage_side=file_name_client_BeforeImageSideEdit,
                                                                   updated_at=datetime.utcnow())
    try:
        client_BeforeImageBackEdit = files["client_BeforeImageBackEdit"]
    except:
        client_BeforeImageBackEdit = ''
    if client_BeforeImageBackEdit != '':
        fss = FileSystemStorage()
        file_name_client_BeforeImageBackEdit = rand_slug() + "-" + str(client_BeforeImageBackEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_BeforeImageBackEdit, client_BeforeImageBackEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(beforeimage_back=file_name_client_BeforeImageBackEdit,
                                                                   updated_at=datetime.utcnow())
    try:
        client_AfterImageFrontEdit = files["client_AfterImageFrontEdit"]
    except:
        client_AfterImageFrontEdit = ''
    if client_AfterImageFrontEdit != '':
        fss = FileSystemStorage()
        file_name_client_AfterImageFrontEdit = rand_slug() + "-" + str(client_AfterImageFrontEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_AfterImageFrontEdit, client_AfterImageFrontEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(afterimage_front=file_name_client_AfterImageFrontEdit,
                                                                   updated_at=datetime.utcnow())
    try:
        client_AfterImageFrontSideEdit = files["client_AfterImageFrontSideEdit"]
    except:
        client_AfterImageFrontSideEdit = ''
    if client_AfterImageFrontSideEdit != '':
        fss = FileSystemStorage()
        file_name_client_AfterImageFrontSideEdit = rand_slug() + "-" + str(client_AfterImageFrontSideEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_AfterImageFrontSideEdit, client_AfterImageFrontSideEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(afterimage_side=file_name_client_AfterImageFrontSideEdit,
                                                                   updated_at=datetime.utcnow())
    try:
        client_AfterImageFrontBackEdit = files["client_AfterImageFrontBackEdit"]
    except:
        client_AfterImageFrontBackEdit = ''
    if client_AfterImageFrontBackEdit != '':
        fss = FileSystemStorage()
        file_name_client_AfterImageFrontBackEdit = rand_slug() + "-" + str(client_AfterImageFrontBackEdit)
        file_image = fss.save('static/uploads/client_media/' + file_name_client_AfterImageFrontBackEdit, client_AfterImageFrontBackEdit)

        UserClientTransformation.objects.filter(id=edit_id).update(afterimage_back=file_name_client_AfterImageFrontBackEdit,
                                                                   updated_at=datetime.utcnow())
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    userClientTransformationData = UserClientTransformation.objects.all().filter(user_id=user_id).values()
    context = {
        'userClientTransformationData': userClientTransformationData
    }
    return render(request, 'elements/users/client_table.html', context)

def faqSend(request):
    data = request.POST
    # print(data)
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id

    faqType = data["faqType"]
    answer = ''
    if faqType== "existingFaqs":
        question = data["faqquestionSelect"]
        answer = data["faqanswer"].strip()
    else:
        question = data["faqquestion"].strip()
        answer = data["faqanswer2"].strip()
    userFaq = UserFaq(user_id=user_id, status=1,question=question,faq_type=faqType,answer=answer,slug=slugify(rand_slug()),
                                               created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    userFaq.save()
    faq_tabless = UserFaq.objects.all().filter(user_id=user_id).values()
    context = {
        'faq_tabless': faq_tabless
    }
    return render(request, 'elements/users/faq_table.html', context)
def updateFaq(request):
    data = request.POST

    # print(data)
    id = data['id']
    question = ''
    type = data["typeedit"]
    if type == "existingFaqs":
        question = data["faqquestionSelectEdit"]
    else:
        question = data["faqquestionEdit"].strip()

    user_id = request.session['user_id']
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id
    answer = data["faqanswerEdit"].strip()

    UserFaq.objects.filter(id=id).update(question=question,answer=answer,updated_at=datetime.utcnow())
    faq_tabless = UserFaq.objects.all().filter(user_id=user_id).values()
    context = {
        'faq_tabless': faq_tabless
    }
    return render(request, 'elements/users/faq_table.html', context)
def updateUserStatus(request):
    data = request.POST
    user_id = request.session['user_id']

    # print(data)
    id = data['id']
    checkbox = data.get("checkbox")
    # print(checkbox)
    if checkbox == "true":
        status = 1
    else:
        status = 0
    # print(status)
    context = {
        '1': 'hello'
    }
    if data["type"] == "media":
        UserMediaRecord.objects.filter(id=id).update(status=status,updated_at=datetime.utcnow())
    if data["type"] == "client":
        UserClientTransformation.objects.filter(id=id).update(status=status,updated_at=datetime.utcnow())
    if data["type"] == "award":
        UserAward.objects.filter(id=id).update(status=status, updated_at=datetime.utcnow())


    return HttpResponse(1)

def deleteFaq(request):
    data = request.POST
    user_id = request.session['user_id']
    user_type = request.session['user_type']
    if user_type == "Personal Trainer":
        user = User.objects.get(freelance_id=user_id)
        user_id = user.id

    id = data.get("id")
    UserFaq.objects.filter(id=id).delete()
    faq_tabless = UserFaq.objects.all().filter(user_id=user_id).values()
    context = {
        'faq_tabless': faq_tabless
    }
    return render(request, 'elements/users/faq_table.html', context)
def viewMedia(request):
    data = request.POST
    user_id = request.session['user_id']
    id = data.get("id")
    mediaSoci = UserMediaRecord.objects.get(id=id)
    context = {
        'mediaSoci': mediaSoci,
    }
    return render(request, 'elements/users/mediaModel.html', context)
def viewFaq(request):
    data = request.POST
    user_id = request.session['user_id']
    id = data.get("id")
    viewFaq = UserFaq.objects.get(id=id)
    existingFaq = ExistingFaq.objects.all().filter().values()

    context = {
        'viewFaq': viewFaq,
        'existingFaq':existingFaq
    }
    return render(request, 'elements/users/faqModel.html', context)
def viewClient(request):
    data = request.POST
    user_id = request.session['user_id']
    id = data.get("id")
    clientTransformationData = UserClientTransformation.objects.get(id=id)

    context = {
        'clientTransformationData': clientTransformationData,
    }
    return render(request, 'elements/users/clientModal.html', context)
def offerSubmit(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    promotion_type= int(data['promotion_type'])
    if promotion_type == 1:
        dataArr = []
        # category= data['category']
        # type_of_service= data['type_of_service']

        
        type_of_service = {
        data['service_id']:[data['type_of_service']]
        }
        dataArr.append(type_of_service)
        # print(dataArr)

        expiry_date= data['expiry_date']
        discount= data['discount']
        # discount_number= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['before_price']
        after_price= data['after_price']
        

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        record = UserOffer(
            user_id=user_id,
            promotion_type=promotion_type,
            # category=category,
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,
            status=1,

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    elif promotion_type == 2:
        # category= data['category']
        # type_of_service= data['type_of_service']

        dataArr = []
        type_of_service = {
        data['service_id']:[data['type_of_service']]
        }
        dataArr.append(type_of_service)

        expiry_date= data['expiry_date']
        discount= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['before_price']
        after_price= data['after_price']

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        record = UserOffer(
            user_id=user_id,
            promotion_type=promotion_type,
            # category=category,
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,
            status=1,

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    elif promotion_type == 3:

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'multi_service-'+str(i)
                # dataArr.append(i)
                # dataArr[i] =[]
                # print(name)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        expiry_date= data['expiry_date']
        discount= data['discount']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['total_before_price']
        after_price= data['total_after_price']

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        record = UserOffer(
            user_id=user_id,
            promotion_type=promotion_type,
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,
            status=1,

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    elif promotion_type == 4:

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'multi_service-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        expiry_date= data['expiry_date']
        discount= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['total_before_price']
        after_price= data['total_after_price']

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        record = UserOffer(
            user_id=user_id,
            promotion_type=promotion_type,
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,
            status=1,

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    elif promotion_type == 5:

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'multi_service_free-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        dataArr1 = []
        type_of_service = {
        data['service_id']:[data['service_purchased']]
        }
        dataArr1.append(type_of_service)

        expiry_date= data['expiry_date']
        # discount= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0


        record = UserOffer(
            user_id=user_id,
            promotion_type=promotion_type,
            type_of_service=json.dumps(dataArr1),
            free_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            # discount=discount,
            avail_limit=avail_limit,
            status=1,

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        record.save()

    offerRecords = UserOffer.objects.filter(user_id=user_id).values()

    

    context = {
        'offerRecords': offerRecords,
        
    }

    return render(request, 'elements/users/offer_table.html', context)

def getServiceList(request):
    category = request.POST.get("category")

    records = UserPrice.objects.filter(session_category=category).values_list('id','session_name').order_by('session_name')
    context = {
        'records': records,
    }

    return render(request, 'elements/getService.html', context)

def getServicePrice(request):
    category = request.POST.get("category")
    service = request.POST.get("service")

    record = UserPrice.objects.filter(id=service).values('currency','price')[0]

    # print(record)
    context = {
        0:record['price'],1:record['currency']
        }
    return JsonResponse(context)

def viewOffer(request):
    data = request.POST

    user_id = request.session['user_id']

    id = data.get("id")
    offer = UserOffer.objects.get(id=id)

    session_records = UserPrice.objects.filter(session_category=1,user_id=user_id).values_list('id','session_name').order_by('session_name')
    service_records = UserPrice.objects.filter(session_category=2,user_id=user_id).values_list('id','session_name').order_by('session_name')
    day_records = UserPrice.objects.filter(session_category=3,user_id=user_id).values_list('id','session_name').order_by('session_name')
    membership_records = UserPrice.objects.filter(session_category=4,user_id=user_id).values_list('id','session_name').order_by('session_name')

    context = {
        'offer': offer,
        'session_records': session_records,
        'service_records': service_records,
        'day_records': day_records,
        'membership_records': membership_records,
    }
    
    return render(request, 'elements/users/offer_model.html', context)

def deleteOffer(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    UserOffer.objects.filter(id=id).delete()

    return HttpResponse(1)

def editOffer(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    offer_id= data['offer_id']
    promotion_type= int(data['promotion_type'])
    if promotion_type == 1:
        # dataArr = []
        
        # type_of_service = {
        # data['service_id']:[data['type_of_service']]
        # }
        # dataArr.append(type_of_service)

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'type_of_service-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        expiry_date= data['expiry_date']
        discount= data['discount']
        # discount_number= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['before_price']
        after_price= data['after_price']
        

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        UserOffer.objects.filter(id=offer_id).update(
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,

            updated_at=datetime.utcnow(),
        )

    elif promotion_type == 2:

        # dataArr = []
        # type_of_service = {
        # data['service_id']:[data['type_of_service']]
        # }
        # dataArr.append(type_of_service)

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'type_of_service-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        expiry_date= data['expiry_date']
        discount= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['before_price']
        after_price= data['after_price']

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        UserOffer.objects.filter(id=offer_id).update(
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,

            updated_at=datetime.utcnow(),
        )

    elif promotion_type == 3:

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'multi_service-'+str(i)
                # dataArr.append(i)
                # dataArr[i] =[]
                # print(name)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        expiry_date= data['expiry_date']
        discount= data['discount']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['total_before_price']
        after_price= data['total_after_price']

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        UserOffer.objects.filter(id=offer_id).update(
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,

            updated_at=datetime.utcnow(),
        )

    elif promotion_type == 4:

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'multi_service-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1

        expiry_date= data['expiry_date']
        discount= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0
        before_price= data['total_before_price']
        after_price= data['total_after_price']

        x = before_price.split()
        y = after_price.split()
        before_price =x[0]
        after_price =y[0]

        currency= x[1]

        UserOffer.objects.filter(id=offer_id).update(
            type_of_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            discount=discount,
            avail_limit=avail_limit,
            before_price=before_price,
            after_price=after_price,
            currency=currency,

            updated_at=datetime.utcnow(),
        )

    elif promotion_type == 5:

        dataArr = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'multi_service_free-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr.append(type_of_service)
                    # print(i)
            except:
                1
                
        dataArr1 = []
        type_of_service = ''
        for i in range(5):
            try:
                name = 'service_purchased-'+str(i)
                Record = data.getlist(name)
                if Record:
                    type_of_service = {
                        str(i):data.getlist(name)
                    }    
                    # print(type_of_service)               
                    dataArr1.append(type_of_service)
                    # print(i)
            except:
                1

        # dataArr1 = []
        # type_of_service = {
        # data['service_id']:[data['service_purchased']]
        # }
        # dataArr1.append(type_of_service)

        expiry_date= data['expiry_date']
        # discount= data['discount_number']
        avail_limit= data['avail_limit']
        if data['avail_limit'] == '':
            avail_limit= 0


        UserOffer.objects.filter(id=offer_id).update(
            type_of_service=json.dumps(dataArr1),
            free_service=json.dumps(dataArr),
            expiry_date=date.datetime.strptime(expiry_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
            # discount=discount,
            avail_limit=avail_limit,

            updated_at=datetime.utcnow(),
        )

    offerRecords = UserOffer.objects.filter(user_id=user_id).values()

    

    context = {
        'offerRecords': offerRecords,
        
    }

    return render(request, 'elements/users/offer_table.html', context)
    
def searchOffer(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    empSearch = data.get("name")

    con1 =con2 = con3 = con4 = con5 = Q()
    str1 = 'Discount (in terms of percentage)'
    str2 = 'Discount (in terms of price reduction)'
    str3 = 'Bundle packages with percentage discount'
    str4 = 'Bundle packages with price reduction'
    str5 = 'Buy X Get Y Free'
    if str1.lower().find(empSearch.lower())!=-1:
        con1 = Q(promotion_type=1)
    if str2.lower().find(empSearch.lower())!=-1:
        con2 = Q(promotion_type=2)
    if str3.lower().find(empSearch.lower())!=-1:
        con3 = Q(promotion_type=3)
    if str4.lower().find(empSearch.lower())!=-1:
        con4 = Q(promotion_type=4)
    if str5.lower().find(empSearch.lower())!=-1:
        con5 = Q(promotion_type=5)
        
    if con1 == Q() and con2 == Q() and con3 == Q() and con4 == Q() and con5 == Q() and empSearch != '': 
        con1 = Q(promotion_type=0)
        con2 = Q(promotion_type=0)
        con3 = Q(promotion_type=0)
        con4 = Q(promotion_type=0)
        con5 = Q(promotion_type=0)

    # print(con1)
    # print(con2)
    # print(con3)
    # print(con4)
    # print(con5)

    # offerRecords = UserOffer.objects.filter(user_id=user_id).values()
    offerRecords = UserOffer.objects.all().filter(Q(user_id=user_id)).filter(con1 | con2 | con3 | con4 | con5)
    context = {
        'offerRecords': offerRecords,
    }

    return render(request, 'elements/users/offer_table.html', context)
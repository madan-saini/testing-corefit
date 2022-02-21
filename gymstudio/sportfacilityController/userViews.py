from django.shortcuts import render
from .. models import *
from django.contrib.auth.hashers import *
import random
import string
from jinja2 import Environment, FileSystemLoader
from django.shortcuts import render
import os
from django.db.models import Q
# Create your views here.


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))



def profile(request):
    title = settings.SITE_TITLE + ' | ' + 'Profile'
    request.session['user_type'] = "Sports Facility"
    user_id = request.session['user_id']
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
        

    amen_arr = []
    if amenityinfo:
        for amm in amenityinfo:
            amen_arr.append(amm['amenity_id'])

    equi_arr = []
    if equipmentinfo:
        for eqmm in equipmentinfo:
            equi_arr.append(eqmm['equipment_id'])

    cities = []

    if basicinfo:
        cities = City.objects.filter(country_id=basicinfo.country).values_list('id','name').order_by('name')



    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    # *******
    mediaSocialMedia = UserMediaRecord.objects.all().filter(user_id=user_id, type="myMedia[]").values()
    mediavirtual_tour = UserMediaRecord.objects.all().filter(user_id=user_id, type="virtual_tour").values()
    mediatile_image = UserMediaRecord.objects.all().filter(user_id=user_id, type="tile_image").values()
    mediamyMedia = UserMediaRecord.objects.all().filter(user_id=user_id, type="myMedia[]").values().order_by(
        '-created_at')
    mediaprofile_photo = UserMediaRecord.objects.filter(user_id=user_id, type='ProfilePhoto').values()
    userClientTransformationData = UserClientTransformation.objects.all().filter(user_id=user_id).values()

    if mediamyMedia:
        mediamyMedia = mediamyMedia[0]

    # **********

    sesstionTypes = Session.objects.all().values_list('id', 'name').order_by('name')
    serviceAmenityTypes = ServiceAmenity.objects.all().values_list('id', 'name').order_by('name')
    amenityTypes = BookableAmenity.objects.all().values_list('id', 'name').order_by('name')
    sports = Sport.objects.all().values_list('id', 'name').order_by('name')
    priceList = UserPrice.objects.filter(user_id=user_id).values()


    existingFaq = ExistingFaq.objects.all().filter().values()
    faq_tabless = UserFaq.objects.all().filter(user_id=user_id).values()
    sportsType = Sport.objects.all().values_list('id','name').order_by('name')
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
        "faq_tabless":faq_tabless,
        "sportsType":sportsType,


        # **********
    }
   
    return render(request, 'sportFacility/users/profile.html', context)






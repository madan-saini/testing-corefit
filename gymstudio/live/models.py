from django.db import models

# Create your models here.
class User(models.Model):
    email_address = models.EmailField(unique=True)
    first_name = models.Field()
    last_name = models.Field()
    contact = models.Field()
    user_type = models.Field()
    uniqueKey = models.Field()
    nationality = models.Field()
    facebookLink = models.Field()
    twitterLink  = models.Field()
    instagramLink = models.Field()
    currency = models.Field()
    # pt profile
    dob = models.Field(default=None)
    # end
    year_of_experince = models.Field()
    languages = models.Field()
    password = models.Field()
    gender = models.Field()
    business_doc = models.Field()
    director_doc = models.Field()
    terms = models.Field(default=0)
    slug = models.Field()
    freelance_id = models.Field(default=0)
    created_at = models.Field()
    updated_at = models.Field()
    
    class Meta:
        db_table = "users"

class Country(models.Model):

    name = models.Field()
    country_code = models.Field()
    sortname = models.Field()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "countries"

class City(models.Model):

    country_id = models.Field()
    name = models.Field()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "cities"

class Language(models.Model):

    name = models.Field()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "languages"

class Amenity(models.Model):

    name = models.Field()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "amenities"

class Equipment(models.Model):

    name = models.Field()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "equipments"

class Service(models.Model):

    name = models.Field()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "services"

class Emailtemplate(models.Model):

    subject = models.Field()
    template = models.Field()

    class Meta:
        db_table = "emailtemplates"

class Branch(models.Model):

    user_id = models.Field()
    brand_id = models.Field(default=0)
    branch_name = models.Field()
    branch_address = models.Field()
    slug = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "branches"

class Brand(models.Model):

    user_id = models.Field()
    brand_name = models.Field()
    brand_address = models.Field()
    slug = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "brands"

class UserAmenity(models.Model):

    # user_id = models.Field()
    # amenity_id = models.Field()
    quantity = models.Field()
    visible_status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_amenities"

class UserEquipment(models.Model):

    # user_id = models.Field()
    # equipment_id = models.Field()
    quantity = models.Field()
    max_value = models.Field()
    visible_status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_equipments"

class BasicInfo(models.Model):
    
    # user_id = models.Field()
    # brand_id = models.Field()
    # branch_id = models.Field()
    facility_profile_level = models.Field()
    facility_type = models.Field()
    training_type = models.Field()
    website = models.Field()
    about = models.Field()
    short_bio = models.Field()
    location = models.Field()
    # pt employee
    homelocation = models.Field()
    homelocation2 = models.Field()
    country = models.Field(default=None)
    height = models.Field(default=0)
    height_type_1 = models.Field(default=0)
    weight = models.Field(default=0)
    weight_type_1 = models.Field(default=0)
    city = models.Field()
    key_skills = models.Field()
    other_skills = models.Field()
    bio_video = models.Field()
    #
    own_facility = models.Field(default=0)
    train_country = models.Field(default=None)
    train_city = models.Field(default=None)
    trainlocation = models.Field(default=None)
    trainBlocation = models.Field(default=None)
    train_country2 = models.Field(default=None)
    train_city2 = models.Field(default=None)
    trainlocation2 = models.Field(default=None)
    trainBlocation2 = models.Field(default=None)
    nationality = models.Field(default=None)

    created_at = models.Field()
    updated_at = models.Field()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,default=None)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,default=None)

    class Meta:
        db_table = "user_basic_infos"

class Availability(models.Model):

    user_id = models.Field()
    day_name = models.Field()
    start_time = models.Field()
    end_time = models.Field()
    status = models.Field(default=0)
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "availabilities"

class OverAvailability(models.Model):

    user_id = models.Field()
    date = models.Field()
    start_time = models.Field()
    end_time = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "overwrite_availabilities"

class UserAward(models.Model):

    user_id = models.Field()
    date = models.Field()
    award_name = models.Field()
    location = models.Field()
    document = models.Field()
    status = models.Field(default=1)
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "user_awards" 

# user_media_records****

class UserMediaRecord(models.Model):

    user_id = models.Field()
    type = models.Field()
    data = models.Field()
    status = models.Field(default=1)
    mediaTitle = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "user_media_records"

class Session(models.Model):
        
    name = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "sessions"

class ServiceAmenity(models.Model):
        
    name = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "service_amenities"

class Sport(models.Model):
        
    name = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "sports"

class BookableAmenity(models.Model):
        
    name = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "bookable_amenities"

class UserPrice(models.Model):
        
    # user_id = models.Field()
    session_category = models.Field()
    type_of_session = models.Field(default=0)
    number_of_people = models.Field(default=0)
    session_type = models.Field()
    session_name = models.Field()
    number_of_session = models.Field(default=0)
    duration = models.Field()
    validity = models.Field(default=0)
    validity_type = models.Field()
    currency = models.Field()
    price = models.Field()
    location = models.Field()
    notes = models.Field()
    what_included = models.Field()
    inclusive_class = models.Field()
    type_of_amenity = models.Field()
    sport_type = models.Field()
    number_of_participant = models.Field()
    booking_length = models.Field()

    slug = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_prices"

class UserClientTransformation(models.Model):

    user_id = models.Field()
    name = models.Field()
    description = models.Field()
    image = models.Field()
    beforeimage_front = models.Field()
    beforeimage_back = models.Field()
    beforeimage_side = models.Field()
    afterimage_front = models.Field()
    afterimage_back = models.Field()
    afterimage_side = models.Field()
    slug = models.Field()
    status = models.Field(default=1)
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "client_transformations"

class ExistingFaq(models.Model):
    question = models.Field()
    slug = models.Field()
    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "existing_faqs"

class UserFaq(models.Model):
    user_id = models.Field()
    question = models.Field()
    answer = models.Field()
    faq_type = models.Field()
    slug = models.Field()
    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()
    class Meta:
        db_table = "user_faqs"

class UserOffer(models.Model):
    user_id = models.Field()
    promotion_type = models.Field()
    category = models.Field(default=None)
    type_of_service = models.Field()
    expiry_date = models.Field()
    discount = models.Field(default=0)
    avail_limit = models.Field(default=0)
    before_price = models.Field()
    after_price = models.Field()
    free_service = models.Field()
    currency = models.Field()

    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()
    class Meta:
        db_table = "user_offers"
        
class UserSchedule(models.Model):
        
    user_id = models.Field()
    employee_id = models.Field()
    schedule_name = models.Field()
    is_default = models.Field(default=0)
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "user_schedules"

class EmployeeAvailability(models.Model):

    user_id = models.Field()
    schedule_id = models.Field()
    day_name = models.Field()
    start_time = models.Field()
    end_time = models.Field()
    status = models.Field(default=0)
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "employee_availabilities"

class EmployeeOverAvailability(models.Model):

    user_id = models.Field()
    schedule_id = models.Field()
    date = models.Field()
    start_time = models.Field()
    end_time = models.Field()
    status = models.Field(default=0)
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "employee_overwrite_availabilities"
        
class Event(models.Model):
        
    # user_id = models.Field()
    date_of_booking = models.Field()
    time_of_booking = models.Field()
    location = models.Field()
    client_name = models.Field()
    pt_name = models.Field()
    type_of_services = models.Field()
    service = models.Field()
    slug = models.Field()

    
    status = models.Field(default=0)
    created_at = models.Field()
    updated_at = models.Field()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "events"

#        comment new table
class Request(models.Model):
    user_id = models.Field()
    invited_user_id = models.Field()
    type = models.Field(default='')
    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()
    class Meta:
        db_table = "requests"
        
# Wallet module
class UserBank(models.Model):
    user_id = models.Field()
    account_name = models.Field()
    bank_name = models.Field()
    routing_number = models.Field()
    account_number = models.Field()
    account_type = models.Field()
    sort_code = models.Field()
    iban_number = models.Field()
    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()
    
    class Meta:
        db_table = "user_banks"

class UserCard(models.Model):
    user_id = models.Field()
    card_holder_name = models.Field()
    card_number = models.Field()
    card_type = models.Field()
    card_cvv = models.Field()
    expiry_date = models.Field()
    
    created_at = models.Field()
    updated_at = models.Field()
    
    class Meta:
        db_table = "user_cards"

class Bolton(models.Model):
    title = models.Field()
    description = models.Field()
    price = models.Field()
    duration = models.Field()
    slug = models.Field()

    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "boltons"

class UserBolton(models.Model):
    user_id = models.Field()
    # print(user_id)
    # bolton_id = models.Field()

    status = models.Field()
    created_at = models.Field()
    updated_at = models.Field()

    bolton = models.ForeignKey(Bolton, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_boltons"

class Enquiry(models.Model):
    user_id = models.Field()
    type = models.Field()
    subject = models.Field()
    message = models.Field()
    slug = models.Field()

    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "enquiries"


class Feature(models.Model):
    title = models.Field()
    description = models.Field()
    status = models.Field()

    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "subscription_plan_features"

class Plan(models.Model):
    type = models.Field()
    description = models.Field()
    
    duration = models.Field()
    features = models.Field()
    slug = models.Field()
    status = models.Field()

    created_at = models.Field()
    updated_at = models.Field()

    class Meta:
        db_table = "plans"

class Currency(models.Model):
    name = models.Field()
    is_default = models.Field()

    created_at = models.Field()
    updated_at = models.Field()

    

    class Meta:
        db_table = "currencies"

class PlanPrice(models.Model):
    currency = models.Field()
    price = models.Field()

    created_at = models.Field()
    updated_at = models.Field()

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    # plan = models.ForeignKey(Plan, related_name='planprice')

    class Meta:
        db_table = "planprices"

from django.contrib import admin
from django.urls import path
from . controller import userViews
from . ptcontroller import userViews as ptUserViews
from . controller import formSubmit
from . ptcontroller import formSubmit as ptformSubmit
from . sportfacilityController import userViews as spCUserViews

from . controller import scheduleView
from . controller import walletController
from . controller import requestController
from . freelancercontroller import formSubmit as fformSubmit
from . freelancercontroller import userViews as fUserViews
from . ptcompanyController import userViews as ptCUserViews
from . sportfacilityController import formSubmit as spformSubmit
from . ptcompanyController import formSubmit as ptCformSubmit

urlpatterns = [
     path('login', userViews.login,name="login"), 
     path('forgot-password', userViews.forgotPassword,name="forgot-password"), 
     path('reset-password/<slug:slug>', userViews.resetPassword,name="reset-password"), 
     path('checkValid', userViews.checkValid,name="checkValid"), 
     path('register', userViews.register,name="register"), 
     path('otp_send', userViews.otp_send,name="otp_send"),
     path('otp_verify', userViews.otp_verify,name="otp_verify"),
     path('forgot_otp_verify', userViews.forgot_otp_verify,name="forgot_otp_verify"),
     path('profile', userViews.profile,name="profile"),
     path('logout', userViews.logout,name="logout"),
     path('thank-you', userViews.thankyou,name="thank-you"),
     path('basicProfile', formSubmit.basicProfile,name="basicProfile"),
     path('awardProfile', formSubmit.awardProfile,name="awardProfile"),
     path('editAwardProfile', formSubmit.editAwardProfile,name="editAwardProfile"),
     path('addPricing', formSubmit.addPricing),
     path('deleteAward', formSubmit.deleteAward),
     path('viewAward', formSubmit.viewAward),
     path('viewCopy', formSubmit.viewCopy),
     path('getCityList', formSubmit.getCityList,name="getCityList"),
     path('updateAmenity', formSubmit.updateAmenity),
     path('updateEquipment', formSubmit.updateEquipment),
     path('saveAvailability', formSubmit.saveAvailability),
     path('calenderPost', formSubmit.calenderPost),
     path('checkCalVal', formSubmit.checkCalVal),
     path('deleteOver', formSubmit.deleteOver),
     path('deletePrice', formSubmit.deletePrice),
     path('viewPrice', formSubmit.viewPrice),
     path('editPricing', formSubmit.editPricing),
     path('identityForm', formSubmit.identityForm),
     path('saveAvail', formSubmit.saveAvail),

     path('overwrite_section', userViews.overwritesection),
     # ******
     path('mediaSocialMedia', formSubmit.mediaSocialMedia,name="mediaSocialMedia"),
     path('edit_media_media', formSubmit.edit_media_media,name="edit_media_media"),
     path('deleteMedia', formSubmit.deleteMedia,name="deleteMedia"),
     path('updateMedia', formSubmit.updateMedia),
     path('clientTransformation', formSubmit.clientTransformation),
     path('deleteClientTransformation', formSubmit.deleteClientTransformation),
     path('updateClientTransformationSubmit', formSubmit.updateClientTransformationSubmit),

     path('viewMedia', formSubmit.viewMedia),
     path('viewClient', formSubmit.viewClient),
     path('faqSend', formSubmit.faqSend),
     path('deleteFaq', formSubmit.deleteFaq),
     path('viewFaq', formSubmit.viewFaq),
     path('updateFaq', formSubmit.updateFaq),
     path('updateUserStatus', formSubmit.updateUserStatus),

     #****Offer Page
     path('new-offer', userViews.newOffer),
     path('offerSubmit', formSubmit.offerSubmit),
     path('getServiceList', formSubmit.getServiceList),
     path('getServicePrice', formSubmit.getServicePrice),
     path('viewOffer', formSubmit.viewOffer),
     path('deleteOffer', formSubmit.deleteOffer),
     path('editOffer', formSubmit.editOffer),
     path('searchOffer', formSubmit.searchOffer),
     
     #****Schedule Page
     path('set-your-availability', scheduleView.setAvailability),
     path('saveSchedule', scheduleView.saveSchedule),
     path('getEmployee', scheduleView.getEmployee),
     path('deleteSchedule', scheduleView.deleteSchedule),
     path('showCalender', scheduleView.showCalender),
     path('showCalenderView', scheduleView.showCalenderView),
     path('saveAvailabilityEmp', scheduleView.saveAvailabilityEmp),
     path('saveAvailEmp', scheduleView.saveAvailEmp),
     path('checkEmpCalVal', scheduleView.checkEmpCalVal),
     path('empCalenderPost', scheduleView.empCalenderPost),
     path('emp_overwrite_section', scheduleView.empOverwritesection),
     path('deleteEmpOver', scheduleView.deleteEmpOver),
     path('makeDefault', scheduleView.makeDefault),
     path('editSchedule', scheduleView.editSchedule),
     path('cloneSchedule', scheduleView.cloneSchedule),
     path('getEventData', scheduleView.getEventData),
     path('checkEmpCalValEdit', scheduleView.checkEmpCalValEdit),
     path('empCalenderPostEdit', scheduleView.empCalenderPostEdit),
     path('calendar', scheduleView.calendar),
     path('getServiceData', scheduleView.getServiceData),
     path('addEvent', scheduleView.addEvent),
     path('editEvent', scheduleView.editEvent),
     path('viewEvent', scheduleView.viewEvent),
     path('deleteEvent', scheduleView.deleteEvent),
     path('searchEvent', scheduleView.searchEvent),
     path('getSEventData', scheduleView.getSEventData),
     path('getEmployeeCal', scheduleView.getEmployeeCal),
     path('getCal', scheduleView.getCal),

     # *****

     path('', userViews.login,name="login"),


#      pt employee urls
     path('ptemployee-profile', ptUserViews.profile,name="ptemployee-profile"),
     path('ptemployee-basicProfile', ptformSubmit.basicProfile, name="ptemployee-basicProfile"),
#Accreditation
     path('ptemployee-awardProfile', ptformSubmit.awardProfile,name="ptemployee-awardProfile"),
     path('ptemployee-editAwardProfile', ptformSubmit.editAwardProfile,name="ptemployee-editAwardProfile"),
     path('ptemployee-deleteAward', ptformSubmit.deleteAward),
     path('ptemployee-viewAward', ptformSubmit.viewAward),
#      identifications
     path('ptemployee-identityForm', ptformSubmit.identityForm),
     # sports facility
     path('sportfacility-profile', spCUserViews.profile, name="sportfacility-profile"),
     path('sportfacility-basicProfile', spformSubmit.basicProfile, name="sportfacility-basicProfile"),


     # #      pt employee urls
#      path('ptemployee-profile', ptUserViews.profile,name="ptemployee-profile"),
#      path('ptemployee-basicProfile', ptformSubmit.basicProfile, name="ptemployee-basicProfile"),
#      path('ptemployee-getCityList', ptformSubmit.getCityList, name="ptemployee-getCityList"),
#      # media
#      path('ptemployee-mediaSocialMedia', ptformSubmit.mediaSocialMedia, name="ptemployee-mediaSocialMedia"),
#      path('ptemployee-edit_media_media', ptformSubmit.edit_media_media, name="ptemployee-edit_media_media"),
#      path('ptemployee-deleteMedia', ptformSubmit.deleteMedia, name="ptemployee-deleteMedia"),
#      path('ptemployee-updateMedia', ptformSubmit.updateMedia),
#      path('ptemployee-viewMedia', ptformSubmit.viewMedia),
#      path('ptemployee-updateUserStatus', ptformSubmit.updateUserStatus),
# #Accreditation
#      path('ptemployee-awardProfile', ptformSubmit.awardProfile,name="ptemployee-awardProfile"),
#      path('ptemployee-editAwardProfile', ptformSubmit.editAwardProfile,name="ptemployee-editAwardProfile"),
#      path('ptemployee-deleteAward', ptformSubmit.deleteAward),
#      path('ptemployee-viewAward', ptformSubmit.viewAward),
# #      client
#      path('ptemployee-clientTransformation', ptformSubmit.clientTransformation),
#      path('ptemployee-deleteClientTransformation', ptformSubmit.deleteClientTransformation),
#      path('ptemployee-updateClientTransformationSubmit', ptformSubmit.updateClientTransformationSubmit),
#      path('ptemployee-viewClient', ptformSubmit.viewClient),
# #      faqs
#      path('ptemployee-faqSend', ptformSubmit.faqSend),
#      path('ptemployee-deleteFaq', ptformSubmit.deleteFaq),
#      path('ptemployee-viewFaq', ptformSubmit.viewFaq),
#      path('ptemployee-updateFaq', ptformSubmit.updateFaq),
# #      identifications
#      path('ptemployee-identityForm', ptformSubmit.identityForm),

# *****25-01-22
#      Freelancer employee urls
     path('freelancer-profile', fUserViews.profile,name="freelancer-profile"),
     path('freelancer-basicProfile', fformSubmit.basicProfile, name="freelancer-basicProfile"),
     # path('freelancer-getCityList', fformSubmit.getCityList, name="freelancer-getCityList"),
#Accreditation
     path('freelancer-awardProfile', fformSubmit.awardProfile,name="freelancer-awardProfile"),
     path('freelancer-editAwardProfile', fformSubmit.editAwardProfile,name="freelancer-editAwardProfile"),
     path('freelancer-deleteAward', fformSubmit.deleteAward),
     path('freelancer-viewAward', fformSubmit.viewAward),
#      identifications
     path('freelancer-identityForm', fformSubmit.identityForm),
     path('association', fformSubmit.association),
     path('ptassociation', ptformSubmit.ptassociation),

     # ptcompany
     path('ptcompany-profile', ptCUserViews.profile, name="ptcompany-profile"),
     path('getCityList2', formSubmit.getCityList2, name="getCityList2"),
     path('getCityList3', formSubmit.getCityList3, name="getCityList3"),
     path('getTrainList', formSubmit.getTrainList, name="getTrainList"),
     
     #****Schedule Page
     path('employee', userViews.employee),
     path('searchEmployee', userViews.searchEmployee),
     path('deleteEmployee', userViews.deleteEmployee),
     
     #****Wallet Module Page     
     path('bank-and-cards', walletController.bankcards),
     path('bankSubmit', walletController.bankSubmit),
     path('cardSubmit', walletController.cardSubmit),
     path('mybolt-ons', walletController.mybolt),
     path('bolt-ons', walletController.boltlist),
     path('updateBoltStatus', walletController.updateBoltStatus),
     path('enquireSubmit', walletController.enquireSubmit),
     path('payment', walletController.payment),
     path('available-subscription-plans', walletController.subscriptionPlans),
     path('my-plan', walletController.myPlan),
     path('getPlanData', walletController.getPlanData),

     #*****Request Module Page*****
     path('employee-requests', requestController.employeeRequest),

]

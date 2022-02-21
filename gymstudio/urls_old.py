
from django.contrib import admin
from django.urls import path
from . controller import userViews
from . controller import formSubmit
from . controller import scheduleView
from . controller import walletController

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

     # *****
     # path('scookie',userViews.setcookie),  
     # path('gcookie',userViews.getcookie),
     path('', userViews.login,name="login"),
]

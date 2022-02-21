import re
from ..models import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
# from django.utils.http import is_safe_url


EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        print('1515151')
        try:    
            if request.session['user_id']:
                path = request.path_info.lstrip('/')
                if any(m.match(path) for m in EXEMPT_URLS):
                    auth = User.objects.get(id=request.session['user_id'])
                    usertype = auth.user_type
                    if usertype == "Personal Trainer":
                        redirect_to = settings.LOGIN_PTEMPLOYEE_PROFILE
                        return HttpResponseRedirect(redirect_to)
                    if usertype == "Gym&Studio":
                        redirect_to = settings.LOGIN_PROFILE
                        return HttpResponseRedirect(redirect_to)
                    if usertype == "FreelanceTrainer":
                        redirect_to = settings.LOGIN_PTFREELANCER_PROFILE
                        return HttpResponseRedirect(redirect_to)
                    redirect_to = settings.LOGIN_PROFILE
                    return HttpResponseRedirect(redirect_to)
                elif path=='':
                    redirect_to = settings.LOGIN_URL
                    return HttpResponseRedirect(redirect_to)

        except:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                redirect_to = f"{settings.LOGIN_URL}"
                return HttpResponseRedirect(redirect_to)



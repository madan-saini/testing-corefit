import re

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
        # print(request.session.items())

        # if not request.session['user_id']:
        #     return 'You are logged in'
        # return 'You are not logged in'
        try:
            sessionid = request.session['user_id']
        except:
            sessionid=False

        try:

            if sessionid:
                # print('try')
                path = request.path_info.lstrip('/')
                if any(m.match(path) for m in EXEMPT_URLS):
                    redirect_to = settings.LOGIN_PROFILE
                    # print(redirect_to)
                    # 'next' variable to support redirection to attempted page after login
                    # if len(path) > 0 and is_safe_url(
                    #     url=request.path_info, allowed_hosts=request.get_host()):
                    redirect_to = f"{settings.LOGIN_PROFILE}"
                        # print(redirect_to)

                    return HttpResponseRedirect(redirect_to)
        except:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                # print(redirect_to)
                # 'next' variable to support redirection to attempted page after login
                # if len(path) > 0 and is_safe_url(
                #     url=request.path_info, allowed_hosts=request.get_host()):
                redirect_to = f"{settings.LOGIN_URL}"
                print(redirect_to)

                return HttpResponseRedirect(redirect_to)



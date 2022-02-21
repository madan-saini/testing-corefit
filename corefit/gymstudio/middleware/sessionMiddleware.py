import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class SessionMiddleware(MiddlewareMixin):
    print('session')
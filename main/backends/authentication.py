from django.contrib import auth
from django.shortcuts import render, redirect, HttpResponse


class ADAuthMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.contrib.auth.models import User
        from django.shortcuts import render
        from django.core.urlresolvers import resolve

        if request.environ.get('HTTP_HOST')[0:9] == 'localhost':
            username = 'kishkurno_as'
        else:
            username = request.environ.get('AUTH_USER')
        if '\\' in username:
            username = username[username.index('\\') + 1:]

        try:
            user = User.objects.get(username=username)
            auth.login(request, user)
            if user.is_superuser:
                from django.conf import settings
                from django.contrib.messages import constants as message_constants

                settings.MESSAGE_LEVEL = message_constants.DEBUG

            if user.is_superuser \
                    or resolve(request.path).app_name == 'main' or resolve(request.path).app_name == 'admin' \
                    or user.groups.filter(name=resolve(request.path).app_name).count() > 0:
                response = self.get_response(request)
                return response
            else:
                return HttpResponse('у вас нет прав на этот блок')
        except User.DoesNotExist:
            return render(request, 'main/unauthenticated.html')

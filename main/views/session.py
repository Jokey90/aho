from django.shortcuts import HttpResponse


def keep_session(request):
    from random import randint
    return HttpResponse(str(randint(1, 10000)))

from django.shortcuts import render, redirect, HttpResponse


def index(request):

    return redirect(to='mobile:sim_list')
    #return render(request, 'mobile/index.html', None)

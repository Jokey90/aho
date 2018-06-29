from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


#@login_required
def index(request):
    return HttpResponse('aho')

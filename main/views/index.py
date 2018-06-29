from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.backends import render_mobile as render


@login_required
def index(request):
    context = {
    }

    return render(request, 'main/index.html', context)

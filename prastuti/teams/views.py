from django.shortcuts import render
from django.http import HttpResponse

html = '<body><h1>Hello %s! How are you?</h1></body>' %'Aman'

def teamsList(request):
    return HttpResponse(html)

def teamRegister(request):
    return HttpResponse(html)

def teamDetail(request):
    return HttpResponse(html)

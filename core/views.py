from django.shortcuts import render

# Create your views here.

def laylo_view(request):
    return request(request, "index.html")
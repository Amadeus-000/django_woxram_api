from django.shortcuts import redirect
from django.http import HttpResponse

def redirect_view(request):
    return HttpResponse("Hello, World! Woxram-api server")

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
def index(request):

    return render(request, "frontend/index.html")

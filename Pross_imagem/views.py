from django.shortcuts import render
from .models import Image
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,'index.html', {'img':Image})
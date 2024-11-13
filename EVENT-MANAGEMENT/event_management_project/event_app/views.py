from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def aboout(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def booking(request):
    return render(request,'booking.html')

def event(request):
    return render(request,'event.html')


from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse



def home(request):
    return render(request, 'index.html')
   
def about(request):
    return render(request, 'about.html')

def book(request):
    if not request.session.get("access"):
        messages.warning(request, "You must be logged in to book a table.")
        return redirect('login')
    return render(request, 'book.html')

def health(request):
    return HttpResponse("OK", status=200)

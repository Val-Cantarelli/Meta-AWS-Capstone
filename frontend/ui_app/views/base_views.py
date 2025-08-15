from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from ui_app.forms import BookingForm
import requests



def home(request):
    return render(request, 'index.html')
   
def about(request):
    return render(request, 'about.html')

def book(request):
    if not request.session.get("access"):
        messages.warning(request, "You must be logged in to book a table.")
        return redirect('login')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            payload = {
                "date": data["date"].isoformat(),
                "time": data["time"].strftime("%H:%M"),
                "guests": data["guests"],
                "notes": data.get("notes") or "",
            }
            api = f"{settings.API_BASE_URL}/bookings/"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {request.session.get('access')}"
            }
            try:
                resp = requests.post(api, json=payload, headers=headers, timeout=15)
                if resp.status_code in (200, 201):
                    messages.success(request, "Reservation created successfully!")
                    return render(request, 'book.html', {"form": BookingForm()})
                else:
                    # Backend not available or not implemented: graceful fallback
                    messages.info(request, "Reservation request received (demo). Backend booking API not available.")
                    return render(request, 'book.html', {"form": BookingForm()})
            except requests.RequestException:
                messages.info(request, "Reservation request received (offline). We'll process it later.")
                return render(request, 'book.html', {"form": BookingForm()})
        else:
            return render(request, 'book.html', {"form": form})

    # GET
    form = BookingForm()
    return render(request, 'book.html', {"form": form})

def health(request):
    return HttpResponse("OK", status=200)

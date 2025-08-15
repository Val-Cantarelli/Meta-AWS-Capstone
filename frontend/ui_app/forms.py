from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from datetime import time, datetime, date, timedelta

_username_validator = UnicodeUsernameValidator()

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        validators=[_username_validator],
        widget=forms.TextInput(attrs={
            "id": "id_username",
            "autocomplete": "username",
            "autofocus": "autofocus",
            "maxlength": "150",
            "pattern": r"^[\w.@+-]{1,150}$",
            "title": "Use letters, numbers e @ . + - _ (no spaces or special characters)",
        }),
        label="Username",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "id": "id_email",
            "autocomplete": "email",
        }),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "id": "id_password",
            "autocomplete": "new-password",
        }),
        label="Password",
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "id": "id_re_password",
            "autocomplete": "new-password",
        }),
        label="Confirm password",
    )

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("re_password"):
            raise forms.ValidationError("Passwords do not match.")
        return data


class BookingForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "id": "id_date",
        }),
        label="Date",
    )
    # time uses native input type="time"; min/max set dynamically in __init__
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            "type": "time",
            "id": "id_time",
            "step": "1800",
        }),
        label="Time",
    )
    guests = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        widget=forms.NumberInput(attrs={
            "id": "id_guests",
        }),
        label="Guests",
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "id": "id_notes",
            "rows": 3,
            "placeholder": "Allergies, seating preferences, occasion...",
        }),
        label="Notes",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Determine date context (use posted date if available, else today)
        ctx_date = None
        raw_date = (self.data.get("date") or self.initial.get("date")) if hasattr(self, 'data') else None
        if raw_date:
            try:
                ctx_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except Exception:
                ctx_date = None
        if ctx_date is None:
            ctx_date = date.today()

        # Fix UI range to 14:00–22:00 and step to 30 minutes; server will still enforce last-bookable per day
        open_t = time(14, 0)  # 2pm
        self.fields['time'].widget.attrs.update({
            "min": open_t.strftime("%H:%M"),
            "max": "22:00",
            "step": "1800",
        })

    def _build_slots_for_date(self, d):
        # Opening hours based on weekday
        open_t = time(14, 0)  # 2pm
        if d.weekday() <= 4:       # Mon-Fri
            close_t = time(22, 0)  # 10pm
        elif d.weekday() == 5:     # Sat
            close_t = time(23, 0)  # 11pm
        else:                      # Sun
            close_t = time(21, 0)  # 9pm
        # Stop slots at last bookable (1h before close)
        last_t = (datetime.combine(d, close_t) - timedelta(hours=1)).time()
        return self._build_half_hour_slots(open_t, last_t)

    def _build_half_hour_slots(self, start, end):
        # Build 30-min increments inclusive of end when on the hour
        slots = []
        dt = datetime.combine(date.today(), start)
        dt_end = datetime.combine(date.today(), end)
        while dt <= dt_end:
            value = dt.strftime("%H:%M")
            label = dt.strftime("%I:%M %p").lstrip('0')  # e.g., 2:00 PM
            slots.append((value, label))
            dt += timedelta(minutes=30)
        return slots

    def clean(self):
        data = super().clean()
        dt = data.get("date")
        tm_val = data.get("time")
        if not dt or not tm_val:
            return data

        # Parse time value (string from input type="time") back to time
        if isinstance(tm_val, str):
            try:
                tm = datetime.strptime(tm_val, "%H:%M").time()
            except Exception:
                self.add_error("time", "Invalid time format.")
                return data
        else:
            tm = tm_val

        # Enforce minutes to be 00 or 30 only
        if tm.minute not in (0, 30):
            self.add_error("time", "Please choose a time with minutes 00 or 30.")
            return data

        # Opening hours check with last bookable = 1 hour before close
        open_time = time(14, 0)
        weekday = dt.weekday()
        if weekday <= 4:
            close_time = time(22, 0)
            last_time = (datetime.combine(dt, close_time) - timedelta(hours=1)).time()  # 9pm
            label = "Mon–Fri: 2pm–10pm (last booking 9pm)"
        elif weekday == 5:
            close_time = time(23, 0)
            last_time = (datetime.combine(dt, close_time) - timedelta(hours=1)).time()  # 10pm
            label = "Sat: 2pm–11pm (last booking 10pm)"
        else:
            close_time = time(21, 0)
            last_time = (datetime.combine(dt, close_time) - timedelta(hours=1)).time()  # 8pm
            label = "Sun: 2pm–9pm (last booking 8pm)"

        if tm < open_time or tm > last_time:
            self.add_error("time", f"Please choose a time within opening hours ({label}).")
        else:
            data["time"] = tm
        return data

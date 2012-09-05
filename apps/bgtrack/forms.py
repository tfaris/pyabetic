from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from models import GlucoseReading

#class ReadingForm(forms.Form):
#    reading = forms.fields.CharField()
#    timestamp = forms.fields.CharField()

class ReadingForm(ModelForm):
    class Meta:
        model = GlucoseReading
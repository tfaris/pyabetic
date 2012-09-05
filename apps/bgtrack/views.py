from forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response

def record_reading(request,template=""):
    print request.user
    context = RequestContext(request)
    form = ReadingForm(request.POST)
    context['reading_form'] = form
    if form.is_valid():
        reading = form.save(commit=False)
        reading.user = request.user
        reading.save()
    return render_to_response(template,context_instance=context)
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal as D

MMOL_L_PER_MG_DL = 18

class GlucoseReading(models.Model):
    reading = models.DecimalField(max_digits=5, decimal_places=2, name='Glucose reading in mg/dl (Milligrams per Deciliter).')
    timestamp = models.DateTimeField(name='Date/time of the reading.')
    user = models.ForeignKey(User)
    
    def mg_dl(self):
        return self.reading
    def mmol_l(self):
        return self.reading / MMOL_L_PER_MG_DL

def get_average(user):
    """Get an average of all readings for the user."""
    readings = GlucoseReading.objects.filter(user=user)
    reading_nums = [r.reading for r in readings]
    avg = 0
    if len(reading_nums) > 0:
        avg = sum(reading_nums)/len(reading_nums)
    return avg
User.get_average = get_average
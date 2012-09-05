from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal as D
from datetime import datetime,timedelta

MMOL_L_PER_MG_DL = 18

class GlucoseReading(models.Model):
    reading = models.DecimalField(max_digits=5, decimal_places=2, name='Glucose reading in mg/dl (Milligrams per Deciliter).')
    timestamp = models.DateTimeField(name='Date/time of the reading.')
    user = models.ForeignKey(User)
    
    def mg_dl(self):
        return self.reading
    def mmol_l(self):
        return self.reading / MMOL_L_PER_MG_DL
        
    def __unicode__(self):
        return "Reading [%s]: %s mg/dl @ %s" % (self.user.email,self.reading,self.timestamp)

def get_average(user,days=None):
    """Get an average of all readings for the user."""
    filter_args = {'user':user}
    if days:
        filter_args['timestamp__gt'] = datetime.now().date()+timedelta(days=-days)
    
    readings = GlucoseReading.objects.filter(**filter_args)
    reading_nums = [r.reading for r in readings]
    avg,count = 0,len(reading_nums)
    if count > 0:
        avg = sum(reading_nums)/count
    return (days,count,avg)
User.get_average = get_average
User.__unicode__ = lambda self:self.email
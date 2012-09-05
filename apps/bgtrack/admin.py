from models import GlucoseReading
from django.contrib import admin

class GlucoseReadingAdmin(admin.ModelAdmin):
    list_display = ('user','reading','timestamp')
    
admin.site.register(GlucoseReading,GlucoseReadingAdmin)
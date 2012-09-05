from models import GlucoseReading,MMOL_L_PER_MG_DL
from datetime import datetime

def record_reading(user,reading_mgdl,timestamp=None):
    """Create and save a glucose reading."""
    if timestamp is None:
        timestamp = datetime.now()
    return GlucoseReading.objects.create(reading=reading_mgdl,user=user,timestamp=timestamp)
    
def to_mgdl(value):
    return int(value*MMOL_L_PER_MG_DL)
def to_mmoll(value):
    return value/MMOL_L_PER_MG_DL
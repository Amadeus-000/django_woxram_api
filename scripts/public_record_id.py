from app1.models import VoiceDataModel
import re
import time
from django.utils.crypto import get_random_string


def run():
    queryset=VoiceDataModel.objects.all()
    for i in queryset:
        print(i.id)
        i.public_record_id=get_random_string(25)
        i.save()

import requests
from app1.models import VoiceDataModel

# work_idの末尾を確認して、aのものをフィルターする

def run():
    pattern = r"a$"
    queryset=VoiceDataModel.objects.all()
    queryset=queryset.filter(work_id__regex=pattern)
    print(len(queryset))

    for i in queryset:
        print(i.work_id)
        print(i.id)
        i.text_version="posted_script"
        # i.save()
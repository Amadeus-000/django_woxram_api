from app1.models import VoiceDataModel

# maintextをmaintext_oldに移す
def run():
    queryset=VoiceDataModel.objects.all()
    for q in queryset[20000:]:
        print(q.id)
        q.maintext_old=q.maintext
        q.save()
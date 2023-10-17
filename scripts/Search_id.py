from app1.models import VoiceDataModel

def run():
    records=VoiceDataModel.objects.all()

    records=records.filter(title__contains="隣の家に住む幼馴染お姉ちゃん")

    for r in records:
        print(r.id)
from app1.models import CircleModel

def has_duplicates(lst):
    return len(lst) != len(set(lst))

def run():
    circles=CircleModel.objects.all()

    cir_id=[]
    for circle in circles:
        cir_id.append(circle.circle_id)

    print(has_duplicates(cir_id))
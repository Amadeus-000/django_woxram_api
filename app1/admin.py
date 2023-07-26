from django.contrib import admin
from .models import GenreModel
from .models import CharacterVoiceModel
from .models import CircleModel
from .models import ScenarioWriterModel
from .models import VoiceDataModel
from .models import SearchLog


admin.site.register(CharacterVoiceModel)
admin.site.register(CircleModel)
admin.site.register(ScenarioWriterModel)
admin.site.register(GenreModel)
admin.site.register(VoiceDataModel)
admin.site.register(SearchLog)

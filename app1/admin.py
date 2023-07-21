from django.contrib import admin
from .models import GenreModel
from .models import SearchInfoModel
from .models import CharacterVoiceModel
from .models import CircleModel
from .models import ScenarioWriterModel
from .models import VoiceDataModel
from .models import OrderMenu
from .models import CircleState,CircleState2
from .models import Upload_file
from .models import WorkTextState
from .models import SearchLog
from .models import UserAccount

admin.site.register(SearchInfoModel)
admin.site.register(CharacterVoiceModel)
admin.site.register(CircleModel)
admin.site.register(ScenarioWriterModel)
admin.site.register(GenreModel)
admin.site.register(VoiceDataModel)
admin.site.register(OrderMenu)
admin.site.register(CircleState)
admin.site.register(CircleState2)
admin.site.register(Upload_file)
admin.site.register(WorkTextState)
admin.site.register(SearchLog)
admin.site.register(UserAccount)

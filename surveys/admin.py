from django.contrib import admin
from .models import Answer, Tag, AnswerTag

admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(AnswerTag)

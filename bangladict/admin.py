from django.contrib import admin

from .models import Dictionary, Word

admin.site.register(Dictionary)
admin.site.register(Word)


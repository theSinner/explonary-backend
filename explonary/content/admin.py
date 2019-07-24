from django.contrib import admin
from content.models import Tag, Word
# Register your models here.


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = [
                    "id",
                    "text",
                    "description",
                    "language",
                    "random",
                    "owner",
                    "translation_of",
                    "created_at",
                    "modified_at"
                ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
                    "id",
                    "name"
                ]

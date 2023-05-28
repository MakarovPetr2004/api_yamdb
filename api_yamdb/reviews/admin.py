from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'score',
        'text',
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)

from django.contrib import admin

from .models import Category, Genre, Genre_title, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreTitleInline(admin.TabularInline):
    model = Title.genre.through


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    inlines = [
        GenreTitleInline,
    ]
    list_display = (
        'id',
        'name',
        'year',
        'get_genres',
        'category',
    )
    search_fields = ('name', 'year',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Жанр'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_editable = ('genre',)


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
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Genre_title, GenreTitleAdmin)
admin.site.register(Title, TitleAdmin)

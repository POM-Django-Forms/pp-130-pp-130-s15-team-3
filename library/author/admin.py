from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'get_books')
    list_filter = ('books__name',)
    search_fields = ('name', 'surname', 'patronymic', 'books__name')
    readonly_fields = ('get_books',)

    fieldsets = (
        ('Authors name', {
            'fields': ('name', 'surname', 'patronymic')
        }),
        ('Books', {
            'fields': ('get_books',)
        }),
    )

    filter_horizontal = ('books',)

    def get_books(self, obj):
        return ", ".join(book.name for book in obj.books.all())
    get_books.short_description = 'Books'

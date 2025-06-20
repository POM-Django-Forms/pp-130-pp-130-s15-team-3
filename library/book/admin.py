from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'get_authors')
    list_filter = ('count', 'authors__surname')
    search_fields = ('name', 'description', 'authors__surname')
    filter_horizontal = ('authors',)
    
    fieldsets = (
        ('Basic information', {
            'fields': ('name', 'description')
        }),
        ('Details', {
            'fields': ('count', 'authors')
        }),
    )

    filter_horizontal = ('authors',)

    def get_authors(self, obj):
        return ", ".join(f"{a.surname}" for a in obj.authors.all())
    get_authors.short_description = 'Authors'

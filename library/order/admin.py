from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'created_at', 'end_at', 'plated_end_at', 'is_overdue_display')
    list_filter = ('created_at', 'end_at', 'plated_end_at', 'book__name', 'user__email')
    search_fields = ('book__name', 'user__email')

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Orders information', {
            'fields': ('user', 'book')
        }),
        ('Date', {
            'fields': ('created_at', 'plated_end_at', 'end_at')
        }),
    )

    def is_overdue_display(self, obj):
        return obj.is_overdue
    is_overdue_display.short_description = 'Overdue'
    is_overdue_display.boolean = True

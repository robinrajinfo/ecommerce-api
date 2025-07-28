from django.contrib import admin
from .models import Organisation


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'created_at', 'updated_at')
    search_fields = ('name', 'display_name')
    ordering = ('-created_at',)

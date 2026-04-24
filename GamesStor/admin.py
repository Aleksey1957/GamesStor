from django.contrib import admin
from .models import InfoGame

@admin.register(InfoGame)
class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ("price", )
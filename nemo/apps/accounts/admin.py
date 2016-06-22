from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):

    readonly_fields = ['created', 'modified']
    search_fields = ['email']

admin.site.register(User, UserAdmin)

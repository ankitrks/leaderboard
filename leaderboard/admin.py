from django.contrib import admin
from .models import User, Winner

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'points', 'address', 'photo')
    search_fields = ('name', 'address')
    list_filter = ('age', 'points')
    ordering = ('-points',)

class WinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp', 'points')
    search_fields = ('user__name',)
    list_filter = ('timestamp', 'points')
    ordering = ('-timestamp',)

admin.site.register(User, UserAdmin)
admin.site.register(Winner, WinnerAdmin)

from django.contrib import admin

# Register your models here.

from .models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'website', 'created_at')
    search_fields = ('user__username', 'bio', 'location', 'website')
    list_filter = ('created_at',)


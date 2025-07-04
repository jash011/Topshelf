from django.contrib import admin
from .models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_url', 'short_url', 'clicks', 'status', 'created_at')
    search_fields = ('original_url', 'short_url')
    list_filter = ('status', 'created_at')

admin.site.register(Link, LinkAdmin)


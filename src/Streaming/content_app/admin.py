from django.contrib import admin
from content_app.models import Content, Playlist

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title','description','upload_date')
    list_filter = ('content_type', 'is_public')
    search_fields = ('title', 'description')
    ordering = ['upload_date', 'title', 'description']
    #fields = ('title', 'description', 'file_url', 'thumbnail_url','creator')
    fieldsets = (
    ('Informações Básicas', {'fields': ('title', 'description')}),
    ('Detalhes do Arquivo', {'fields': ('file_url', 'thumbnail_url')}),
    ('Criação', {'fields': ('is_public','status', 'creator')}),
  )

admin.site.register(Content, ContentAdmin)
admin.site.register(Playlist)
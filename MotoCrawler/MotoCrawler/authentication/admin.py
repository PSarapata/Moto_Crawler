from django.contrib import admin
from authentication.models import MotoCrawlerUser


class MotoCrawlerUserAdmin(admin.ModelAdmin):
    model = MotoCrawlerUser


admin.site.register(MotoCrawlerUser, MotoCrawlerUserAdmin)

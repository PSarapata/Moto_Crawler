from django.contrib import admin
from authentication.models import MotoCrawlerUser


class MotoCrawlerUserAdmin(admin.ModelAdmin):
    """Registers admin user, based on custom MotoCrawlerUser model."""
    model = MotoCrawlerUser


admin.site.register(MotoCrawlerUser, MotoCrawlerUserAdmin)

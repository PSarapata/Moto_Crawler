from django.contrib import admin
from .models import Offer, Photo, OfferPhoto, UserFavouriteOffer


@admin.register(Offer)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'brand', 'model', 'title', 'price', 'description')


admin.site.register(Photo)
admin.site.register(OfferPhoto)
admin.site.register(UserFavouriteOffer)

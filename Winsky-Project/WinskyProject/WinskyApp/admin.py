from django.contrib import admin
from .models import GeneralContent,AddPackage,Package,Wishlist,ContactMessage

admin.site.register(GeneralContent),
admin.site.register(AddPackage),
admin.site.register(Wishlist),
admin.site.register(Package),
admin.site.register(ContactMessage)

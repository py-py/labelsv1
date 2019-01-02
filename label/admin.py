from django.contrib import admin
from .models import *


class ManufactureModelAdmin(admin.ModelAdmin):
    pass


class KindModelAdmin(admin.ModelAdmin):
    pass


class ImageModelAdmin(admin.TabularInline):
    model = Image
    extra = 1


class LabelModelAdmin(admin.ModelAdmin):
    inlines = (ImageModelAdmin, )


admin.site.register(Manufacture, ManufactureModelAdmin)
admin.site.register(Kind, KindModelAdmin)
# admin.site.register(Image, ImageModelAdmin)
admin.site.register(Label, LabelModelAdmin)

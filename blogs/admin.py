from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget


class AlbumAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

# Register your models here.
from .models import Blog

admin.site.register(Blog, AlbumAdmin)
#   Instruction to use this bootstrap in you project
Project description
Django Pagedown
Add Stack Overflow's "Pagedown" Markdown editor to your Django Admin or custom form.

Screenshot of Django Admin with Pagedown initialised

Requirements
Version >= 2.0.0 of django-pagedown requires Django 2.1.0 or above (previous versions should support Django all the way back to around 1.1).

Installation
Get the code: pip install django-pagedown
Add pagedown.apps.PagedownConfig to your INSTALLED_APPS
Collect the static files: python manage.py collectstatic
Usage
The widget can be used both inside the django admin or independendly.

Inside the Django Admin:
If you want to use the pagedown editor in a django admin field, there are numerous possible approaches:

To use it in all TextField's in your admin form:

from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget


class AlbumAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }
To only use it on particular fields, first create a form (in forms.py):

from django import forms

from pagedown.widgets import AdminPagedownWidget

from music.models import Album

class AlbumForm(forms.ModelForm):
    name = forms.CharField(widget=AdminPagedownWidget())
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Album
        fields = "__all__"
and in your admin.py:

from django.contrib import admin

from forms import FooModelForm
from models import FooModel

@admin.register(FooModel)
class FooModelAdmin(admin.ModelAdmin):
    form = FooModelForm
    fields = "__all__"
Outside the Django Admin:
To use the widget outside of the django admin, first create a form similar to the above but using the basic PagedownWidget:

from django import forms

from pagedown.widgets import PagedownWidget

from music.models import Album


class AlbumForm(forms.ModelForm):
    name = forms.CharField(widget=PagedownWidget())
    description = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Album
        fields = ["name", "description"]
Then define your urls/views:

from django.views.generic import FormView
from django.conf.urls import patterns, url

from music.forms import AlbumForm

urlpatterns = patterns('',
    url(r'^$', FormView.as_view(template_name="baz.html",
                                form_class=AlbumForm)),)
then create the template and load the javascipt and css required to create the editor:

<html>
    <head>
        {{ form.media }}
    </head>
    <body>
        <form ...>
            {{ form }}
        </form>
    </body>
</html>
Customizing the Widget
If you want to customize the widget, the easiest way is to simply extend it:

from pagedown.widgets import PagedownWidget


class MyNewWidget(PagedownWidget):
    template_name = '/custom/template.html'

    class Media:
        css = {
            'all': ('custom/stylesheets.css,)
        }
        js = ('custom/javascript.js',)
Rendering Markdown
contrib.markdown was deprecated in Django 1.5 meaning you can no longer use the markdown filter in your template by default.

@wkcd has a good example of how to overcome by installing django-markdown-deux:

{% extends 'base.html' %}
{% load markdown_deux_tags %}

...
<p>{{ entry.body|markdown }}</p>
...
Image Uploads
You can enable image uploads, allowing your users to upload new images to the server and have them automatically inserted into the Pagedown widget (instead of just adding image URLs):

Screenshot of Django Admin with image upload enabled

To do so:

Make sure you have set a MEDIA_URL and MEDIA_ROOT so that uploads will be propertly saved
Add PAGEDOWN_IMAGE_UPLOAD_ENABLED=True to your settings
Include the pagedown paths in your urls.py so that the upload endpoint is available
 # ...
 urlpatterns = [
     path('', include('pagedown.urls')),
     # ...
 ]
This will add the URL /pagedown/image-upload/ endpoint to your project. You can see the default view that handles the upload here

The following options are available via your settings to tweak how the image upload works:

PAGEDOWN_IMAGE_UPLOAD_PATH can be used to change the path within your media root (default is pagedown-uploads)
PAGEDOWN_IMAGE_UPLOAD_EXTENSIONS can be used to limit the extensions allowed for upload (default is jpg, jpeg, png, webp)
Check out the pagedown_init.js script to see how the upload is being performed on the client side.

Example
You can see a fully-fledged example of the widget in django-pagedown-example
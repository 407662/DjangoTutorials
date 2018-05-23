from django.contrib import admin
from wiki.models import Page

# Registers the Page object with the admin site, so we can
# handle Page objects using the admin UI.
admin.site.register(Page)

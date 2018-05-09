import datetime

from django.db import models
from django.utils import timezone


class Page(models.Model):
    page_title = models.CharField(max_length=100)
    page_contents = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.page_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

import datetime

from django.db import models
from django.utils import timezone


class Page(models.Model):
    page_title = models.CharField(max_length=100, primary_key=True)
    page_contents = models.TextField()
    pub_date = models.DateTimeField('date published')
    hits = models.IntegerField(default=0)

    def __str__(self):
        """
        :return: the page title.
        """

        return self.page_title

    def was_published_recently(self):
        """
        Checks to see if the page was published recently. "Recently" being
        within 1 day of the object creation time.

        :return: True if the Page was published recently.
        """

        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # Has to be after the was_published_recently method.
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.short_description = 'Published recently?'


class UploadedFile(models.Model):
    content = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.content.name

    def get_absolute_url(self):
        return self.content.url

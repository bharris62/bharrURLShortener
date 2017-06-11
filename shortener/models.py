from django.db import models
from .utils import code_generator, create_shortcode
# Create your models here.
class BharrURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(BharrURLManager, self).all(*args, **kwargs)
        qs = qs.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):

        qs = BharrURL.objects.filter(id__gte=1) # gets every item gte = greater than or equal
        if items is not None  and isinstance(items, int):
            qs = qs.order_by('-id')[:items]

        count = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            count += 1
        return "new codes made: {}".format(count)


class BharrURL(models.Model):
    url = models.CharField(max_length=225,)
    shortcode = models.CharField(max_length=15, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = BharrURLManager() #overrides django objects could create your own with something=BharrURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        super(BharrURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)
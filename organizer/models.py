from datetime import date

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.')


    def get_absolute_url(self):
        return reverse('organizer_tag_detail', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('organizer_tag_update', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('organizer_tag_delete', kwargs={'slug':self.slug})

    def published_posts(self):
        return self.blog_posts.filter(
            pub_date__lt=date.today()
        )

    def __str__(self):
        return self.name.title()

    class Meta:
        ordering = ['name']

class Startup(models.Model):
    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.')
    description = models.TextField()
    founded_date = models.DateField('date founded')
    contact = models.EmailField('contact email')
    website = models.URLField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)

    def get_absolute_url(self):
        return reverse('organizer_startup_detail', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('organizer_startup_update', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('organizer_startup_delete', kwargs={'slug':self.slug})

    def get_newslink_create_url(self):
        return reverse('organizer_newslink_create',kwargs={'startup_slug': self.slug})

    def published_posts(self):
        return self.blog_posts.filter(
            pub_date__lt=date.today()
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(max_length=63, help_text='A label for URL config.')
    pub_date = models.DateField('date published')
    link = models.URLField(max_length=255)
    startup = models.ForeignKey(Startup)

    def get_absolute_url(self):
        return self.startup.get_absolute_url()

    def get_update_url(self):
        return reverse('organizer_newslink_update',
                       kwargs={'startup_slug':self.startup.slug, 'newslink_slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer_newslink_delete',
                       kwargs={'startup_slug':self.startup.slug, 'newslink_slug': self.slug})

    def __str__(self):
        return "{}:{}".format(self.startup, self.title)

    class Meta:
        verbose_name = 'news article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'startup')


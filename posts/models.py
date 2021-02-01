from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django_comments_xtd.models import XtdComment
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(max_length=70, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('posts:post-by-categories', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name}'


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    POST_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    author = models.ForeignKey(User, related_name='author_post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=POST_STATUS, default='draft')
    content = HTMLField()
    date_posted = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        ordering = ('date_posted',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            count = 1
            if Post.objects.all().filter(slug=self.slug).exists():
                count += 1
                self.slug = slugify(self.title) + '-' + str(count)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'pk': self.pk, 'slugy': self.slug,
                                                    'year': self.date_posted.year,
                                                    'month': self.date_posted.month,
                                                    'day': self.date_posted.day})

    def __str__(self):
        return f'{self.title}'


class PostComment(XtdComment):
    post_comment = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE, default=1)

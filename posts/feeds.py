from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Tech Blog'
    link = reverse_lazy('posts:index')
    description = 'Latest Posts From Tech Blog'

    def items(self):
        return Post.objects.order_by('-date_posted')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

from django.contrib import admin
from .models import Post, Category

from django_comments_xtd.admin import XtdCommentsAdmin
from .models import PostComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author', 'content']
    list_display = ['id', 'title', 'category', 'author', 'date_posted', 'updated']
    list_display_links = ['id', 'title']
    raw_id_fields = ('author', 'category')


@admin.register(PostComment)
class PostCommentAdmin(XtdCommentsAdmin):
    list_display = ('thread_level', 'cid', 'name', 'content_type', 'post_comment',
                    'object_pk', 'submit_date', 'followup', 'is_public',
                    'is_removed')
    list_display_links = ('cid',)
    raw_id_fields = ('post_comment',)
    list_editable = ['post_comment']
    fieldsets = (
        (None, {'fields': ('content_type', 'object_pk', 'post_comment', 'site')}),
        ('Content', {'fields': ('user', 'user_name', 'user_email',
                                'comment', 'followup')}),
        ('Metadata', {'fields': ('submit_date', 'ip_address',
                                 'is_public', 'is_removed')}),
    )

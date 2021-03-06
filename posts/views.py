from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import ListView, DetailView, FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin
from taggit.models import Tag
from .models import Post, Category


class PostListView(ListView):
    """List all published posts."""
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 5
    extra_context = {'title': 'Home'}
    context_object_name = 'posts'

    def get_queryset(self):
        if self.kwargs.get('tag_slug'):
            tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
            return Post.published.filter(tags__in=[tag]).order_by('-date_posted')
        return Post.published.order_by('-date_posted')


class PostDetailView(DetailView):
    """Detail of a post."""
    model = Post
    template_name = 'posts/post_detail.html'
    # slug_field = 'slugy'
    slug_url_kwarg = 'slugy'

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slugy'),
                                 date_posted__year=self.kwargs.get('year'),
                                 date_posted__month=self.kwargs.get('month'),
                                 date_posted__day=self.kwargs.get('day'))
        context = {'title': post.title, 'post': post}
        return context


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a post by authenticated and permitted users."""
    model = Post
    permission_required = 'posts.can_add'
    fields = ['category', 'title', 'content', 'status', 'tags']
    extra_context = {'title': 'Create Post'}
    success_message = 'Post Added!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a post by the author after authentication."""
    model = Post
    permission_denied_message = 'You can\'t edit this post'
    extra_context = {'title': 'Update Post'}
    fields = ['category', 'title', 'content', 'status', 'tags']
    success_message = 'Post Edited Successfully!'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post by the author after authentication."""
    model = Post
    extra_context = {'title': 'Delete Post'}
    success_message = 'Post Deleted Successfully!'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False


class PostCategories(ListView):
    """List all posts' categories and filter posts by categories."""
    model = Post
    template_name = 'posts/posts_by_categories.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.published.order_by('-date_posted')

    def get_context_data(self, *, object_list=None, **kwargs):
        category = None
        all_categories = Category.objects.order_by('name')
        posts = self.get_queryset()
        if self.kwargs.get('slug'):
            category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
            posts = posts.filter(category=category)
        context = {
            'title': 'Categories',
            'category': category,
            'categories': all_categories,
        }
        return super(PostCategories, self).get_context_data(object_list=posts, **context)


class UserPostListView(ListView):
    """List all posts written by an author."""
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'user_posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.published.all().filter(author=user)

    def get_context_data(self, *, object_list=None,  **kwargs):
        data = super(UserPostListView, self).get_context_data(object_list=self.get_queryset(), **kwargs)
        object_list = self.get_queryset()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # data = {
        #     # 'user_posts': self.get_queryset(),
        #     # 'user_posts': object_list,
        #     'title': f'{user.username} Posts',
        #     'user': user,
        # }
        data.update({
            'title': f'{user.username} Posts',
            'user': user,
            'user_posts': self.get_queryset(),
        })
        # return super(UserPostListView, self).get_context_data(object_list=self.get_queryset(), **data)
        return data


class ViewPostAuthorProfile(LoginRequiredMixin, DetailView):
    """View an author's profile."""
    model = User
    template_name = 'posts/user_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = {
            'title': f'{user.username} Profile',
            'user': user
        }
        return context


class SearchView(FormView):
    """Search for posts."""
    template_name = 'posts/search.html'

    def get_context_data(self,  **kwargs):
        results = None
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            search_vector = SearchVector('title', 'content')
            search_query = SearchQuery(keyword)
            results = Post.published.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
                search=search_query).order_by('-rank')
        context = {
            'title': '{} Search Results'.format(self.request.GET['keyword']),
            'object_list': results,
            'values': self.request.GET
        }
        return context


class TrendingPostsView(ListView):
    """List some Trending posts."""
    model = Post
    template_name = 'posts/trending_posts.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        comments = Post.published.annotate(num_comments=Count('post_comments')).order_by('-num_comments')[:6]
        context = {
            'title': 'Trending Posts',
            'comments': comments,
        }
        return super(TrendingPostsView, self).get_context_data(object_list=comments, **context)

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post
from faceblog.settings import POSTS_ON_PAGE_COUNT


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = POSTS_ON_PAGE_COUNT
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

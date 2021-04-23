from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from blog.models import Post
from faceblog.settings import POSTS_ON_PAGE_COUNT
from blog.forms import EmailPostForm


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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    form = EmailPostForm(request.POST or None)
    sent = False
    if form.is_valid():
        post_url = request.build_absolute_uri(post.get_absolute_url())
        cleaned_data = form.cleaned_data
        subject = f'{cleaned_data["name"]} ({cleaned_data["email"]}) ' \
                  f'recommends you reading {post.title}'
        message = f'Read {post.title} at {post_url}\n\n' \
                  f'{cleaned_data["name"]}\'s comments: ' \
                  f'{cleaned_data["comments"]}'
        send_mail(subject, message, 'admin@faceblog.com', [cleaned_data['to']])
        sent = True
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})

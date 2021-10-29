from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post
from faceblog.settings import POSTS_ON_PAGE_COUNT


# Class based view example
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = POSTS_ON_PAGE_COUNT
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'page': page, 'posts': posts, 'tag': tag}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    new_comment = None
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.save()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


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

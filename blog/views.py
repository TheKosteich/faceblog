from django.shortcuts import render, get_object_or_404
from blog.models import Post


def post_list(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/post/list.html', context=context)

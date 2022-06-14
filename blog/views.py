from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Post
from taggit.models import Tag

from .forms import SearchForm


def post_list(request, tag_slug=None):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
                ).filter(search=search_query).order_by('-rank')
    object_list = Post.published.all()
    tag = None
    all_tags = Tag.objects.all()
    queryset_of_tags = all_tags.annotate(num_times=Count('taggit_taggeditem_items'))
    tag_dict = {}
    for tag in queryset_of_tags:
        tag_dict[tag.name] = tag.num_times

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/list.html',
                  {'page': page,
                   'posts': posts,
                   'all_tags': all_tags,
                   'tag': tag,
                   'tag_dict': tag_dict,
                   'form': form,
                   'query': query,
                   'results': results})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/detail.html',
                  {'post': post,
                   'similar_posts': similar_posts})


def post_archive(request, year, month):
    year_month_posts = Post.objects.filter(publish__year=year).filter(publish__month=month)
    return render(request, 'blog/archive.html',
                  {'year_month_posts': year_month_posts,
                   'year': year,
                   'month': month})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(request,
                  'blog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

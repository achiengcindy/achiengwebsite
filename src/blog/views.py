
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchQuery, SearchRank
#from haystack.query import SearchQuerySet
from.models import Post, Category, Comment
from .forms import EmailPostForm, SearchForm, PostForm, CommentForm
from taggit.models import Tag
import markdown

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.post_set.all()
    # meta_keywords = category.meta_keywords
    # meta_description = category.meta_description
    context = {'posts':posts, 'category': category }
    return render(request, 'blog/post/category.html', context)

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    #Instantiate paginator with the number object we want to display
    paginator = Paginator(object_list, 15) # 15 posts in each page
    page = request.GET.get('page')# indicate the current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.get_page(page)
    context={'page': page, 'posts': posts,'tag': tag}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month, publish__day=day)
    categories = post.categories.filter(is_active=True)
    meta_description = post.meta_description
    # list of active parent comments
    comments = post.comments.filter(active=True, parent__isnull=True)
    # if its a POST request
    if request.method == 'POST':
        # comment has been added, create a form instance and populate
        # with data from the request(binding)
        comment_form = CommentForm(data=request.POST)
        #checkif form is valid
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create reply comment object
                    reply_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    reply_comment.parent = parent_obj
                    # reply_comment.commenter = request.user
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post

            if request.user.is_authenticated: 
                #then request.user will be `User` instance
                # assign user to the comment
                new_comment.commenter = request.user
                print(new_comment.commenter )
                # save
                new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context={'post': post, 'categories':categories,'similar_posts': similar_posts,'meta_url':post.get_absolute_url,'meta_image':post.image.url,'meta_title':post.title, 'meta_description':meta_description,'comments': comments,
                   'comment_form': comment_form}
    return render(request, 'blog/post/detail.html', context)


def post_edit(request, id):
    form = PostForm()
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post/edit.html',  {'form': form})

def post_search(request):
    form = SearchForm()
    cd = results = total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results =Post.objects.filter(
                Q(title__icontains=cd['query'])|
                Q(created__icontains=cd['query'])|
                Q(body__icontains=cd['query'])
                ) 
            total_results = results.count()
    context = {'form': form,'cd': cd,'results': results,'total_results': total_results}
    return render(request, 'blog/post/search.html', context) 

""" def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.3).order_by('-similarity')
    return render(request,'blog/post/search.html',{'form': form,'query': query,'results': results})
 """
def post_share(request, post_id):
    """
    """
    #Retrieve the post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            # .... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            #send_mail(subject, message, 'admin@achiengcindy.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post':post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context) 
    #Retrieve the post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            # .... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            #send_mail(subject, message, 'admin@achiengcindy.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post':post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context) 


def permalink(request, id):
    post = get_object_or_404(Post, id=id)
    return HttpResponseRedirect(post.get_absolute_url())
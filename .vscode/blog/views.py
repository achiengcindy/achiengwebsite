
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comment, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from taggit.models import Tag
from django.conf import settings
from django.db.models import Count, Q
from PIL import Image


def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 12)  # 6 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.post_set.all()
    meta_description = category.meta_description
    context = {'posts': posts, 'category': category}
    return render(request, 'blog/post/category.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    categories = post.categories.filter(is_active=True)
    meta_description = post.meta_description

    # list of active parent comments
    comments = post.comments.filter(active=True, parent__isnull=True)
    new_comment = None
    # if its a POST request
    if request.method == 'POST':
        # comment has been added
        # create a form instance and populate with data from the request(binding)
        comment_form = CommentForm(data=request.POST)
        # check if form is valid
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
                    # assign parent_obj to reply comment
                    reply_comment.parent = parent_obj
                    # reply_comment.commenter = request.user
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post

            if request.user.is_authenticated:
                # then request.user will be `User` instance
                # assign user to the comment
                new_comment.commenter = request.user
                # save
                new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]
    context = {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment, 'similar_posts': similar_posts,
               'meta_url': post.get_absolute_url, 'meta_image': post.image.url, 'meta_title': post.title, 'meta_description': meta_description, 'categories': categories}
    return render(request, 'blog/post/detail.html', context)
  

def dynamic_images(request):
    # https://stackoverflow.com/a/150518
    # src/static/dist/images/alc-1080.png
    # http://127.0.0.1:8000/blog/dynamicimages?url=alc-1080.png
    imageName = request.GET.get('url', '')
    imageSize = int(request.GET.get('size', 0))
    imageUrl = '/home/cindy/Documents/achiengwebsite/src/static/dist/images/' + imageName
    # image_data = open(imageUrl, mode='rb').read()
    # https://stackoverflow.com/a/20361739
    original = Image.open(imageUrl)

    width, height = original.size   # Get dimensions
    left = width/imageSize
    top = height/imageSize
    right = 3 * width/imageSize
    bottom = 3 * height/imageSize
    cropped_example = original.crop((left, top, right, bottom))

    return HttpResponse(cropped_example.show(), content_type="image/png")


def permalink(request,  id, slug):
    post = get_object_or_404(Post,id=id,slug=slug)
    return HttpResponseRedirect(post.get_absolute_url())
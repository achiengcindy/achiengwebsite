from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
User = get_user_model()

class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)

class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,  unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveCategoryManager()

     
    class Meta:
        db_table = 'categories'
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ('-created',)
        
    
    def get_absolute_url(self):
        return reverse('blog:category_list',  args=[self.slug])  
 
    def __str__(self):
        return self.title

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published',is_active='True' )
      
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    categories = models.ManyToManyField(Category) 
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
    caption = models.CharField(max_length=250,null=True, blank=True)
    credit = models.URLField(max_length=250,null=True, blank=True)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.


    tags = TaggableManager()

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug]) 

    def get_permalink_url(self):
        return reverse('permalink', args=[self.id])    


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commenter  = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_comments')
    website = models.URLField(null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
   
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.commenter.username, self.post)

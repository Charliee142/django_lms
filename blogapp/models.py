from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from lmsapp.models import *


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    tags = models.ManyToManyField('Tag', related_name='posts')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_related_posts(self):
        return BlogPost.objects.filter(categories__in=self.categories.all()).exclude(id=self.id).distinct()[:5]

    @classmethod
    def get_latest_posts(cls, count=5):
        return cls.objects.order_by('-created_at')[:count]

    @classmethod
    def get_trending_posts(cls, count=5):
        return cls.objects.order_by('-views', '-likes')[:count]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class What_you_learn(models.Model):
    course  = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True, null=True)
    points  = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.points
    

class What_you_learn_image(models.Model):
    course  = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True, null=True)
    learn_image = models.ImageField(upload_to='learn_images/', blank=True, null=True)
    is_primary = models.BooleanField(default=False)  # Optional flag to mark a primary image

    def __str__(self):
        return f"Image for {self.course.title} - {self.id}"
    
    
class Who_should_attend(models.Model):
    course  = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True, null=True)
    points  = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.points


class Requirements(models.Model):
    course  = models.ForeignKey(BlogPost, on_delete=models.CASCADE,  blank=True, null=True)
    points  = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.points


class Review(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.rating}"

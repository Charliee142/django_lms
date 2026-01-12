from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Avg

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    categories = Category.objects.annotate(post_count=Count('posts'))
    tags = Tag.objects.all()
    latest_posts = BlogPost.get_latest_posts()
    trending_posts = BlogPost.get_trending_posts()

    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'latest_posts': latest_posts,
        'trending_posts': trending_posts,
    }
    return render(request, 'blogapp/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    total_reviews = BlogPost.reviews.count()

     # Initialize rating breakdown (1 to 5 stars) with 0 counts
    rating_breakdown = {i: 0 for i in range(1, 6)}

      # Populate the actual counts from the database
    for item in BlogPost.reviews.values('rating').annotate(count=Count('id')).order_by('-rating'):
        rating_breakdown[item['rating']] = item['count']

      # Convert to a list of dictionaries
    rating_breakdown_list = [{'rating': i, 'count': count} for i, count in rating_breakdown.items()]

      # Get average rating and number of reviews
    reviews_summary = BlogPost.reviews.aggregate( avg_rating=Avg('rating'), total_reviews=Count('id'))
    rating_breakdown = BlogPost.reviews.values('rating').annotate(count=Count('id')).order_by('-rating')
    reviews = BlogPost.reviews.all()
    

    # Increment view count
    post.views += 1
    post.save()

    related_posts = post.get_related_posts()
    latest_posts = BlogPost.get_latest_posts()
    trending_posts = BlogPost.get_trending_posts()



    context = {
        'post': post,
        'related_posts': related_posts,
        'latest_posts': latest_posts,
        'trending_posts': trending_posts,
         'reviews_summary': reviews_summary,  # avg_rating and total_reviews
        'reviews': reviews,
        'total_reviews': total_reviews,
        'rating_breakdown': rating_breakdown_list,
    }
    return render(request, 'blogapp/blog_detail.html', context)


def blog_category_view(request, slug):
    category = Category.objects.get(slug=slug)
    posts = category.posts.all()
    categories = Category.objects.annotate(post_count=Count('posts'))
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'blogapp/blog_category.html', context)



def submit_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user_id=request.user.id, course_id=course_id)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated successfully.')
                return redirect(url)
        except Review.DoesNotExist:
            print("Review does not exist for this user and course.")  # Debugging
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.title = form.cleaned_data['title']
                data.content = form.cleaned_data['content']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR', '')  # Capture user's IP address
                data.course = course  # Assign the course
                data.user = request.user # Assign the user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted successfully.')
                return redirect(url)
    else:
        form = ReviewForm()

    context = {
        'course': course,
        'form': form
    }
    return render(request, 'lmsapp/submit_review.html', context)


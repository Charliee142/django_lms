from django.urls import path
from .import views
#from django.contrib.auth import views as auth_view


urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.single_course, name="single_course"),
    path("courses/<slug:slug>", views.course_details, name="course_details"),
    path("filter-data", views.filter_data, name="filter-data"),
    path("404", views.page_not_found, name="404"),
    path("search", views.search_course, name="search_course"),
    path("course/watch-course/<slug:slug>", views.watch_course, name="watch_course"),
    path("my-course/", views.my_course, name="my_course"),
    path("submit_review/<int:course_id>/", views.submit_review, name="submit_review"),
    
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path('download/', views.download, name='download'),

    path('instructors/', views.top_instructors_view, name='instructors'),
    path('instructor/<int:instructor_id>/', views.instructor_detail_view, name='instructor_details'),
    path('become_instructor/', views.become_instructor, name='become_instructor'),
    path('apply_as_instructor/', views.apply_as_instructor, name='apply_as_instructor'),
    
    
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('search/', views.search, name='search'),


    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:course_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:course_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    #Account
    path("accounts/profile/", views.profile, name="profile"),
    #path("profile/update", views.profile_update, name="profile_update"),
    
    #CHECKOUT
    path("checkout/<slug:slug>", views.checkout, name="checkout"),
    path("verify_payment", views.verify_payment, name="verify_payment"),
]
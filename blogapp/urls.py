from django.urls import path
from .import views


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('category/<slug:slug>/', views.blog_category_view, name='blog_category'),

    path("submit_review/<int:course_id>/", views.submit_review, name="submit_review"),
 
]
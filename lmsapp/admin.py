from django.contrib import admin
from .models import *
   
   
class What_you_learn_TublerInline(admin.TabularInline):
    model = What_you_learn


class Requirements_TublerInline(admin.TabularInline):
    model = Requirements
 

class Video_TublerInline(admin.TabularInline):
    model = Video

    
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (What_you_learn_TublerInline, Requirements_TublerInline, Video_TublerInline)
    

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone',
        'street_address',
        'country',
        'state'
        'zip',
        'email',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address', 'country', 'state']
    
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Course, CourseAdmin)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Video)
admin.site.register(UserCourse)
admin.site.register(Lesson)
admin.site.register(Payment)
admin.site.register(CheckoutAddress)
#admin.site.register(Coupon)
admin.site.register(Review)
admin.site.register(Subscriber)
admin.site.register(Instructor)
admin.site.register(InstructorApplication)
admin.site.register(Testimonial)
admin.site.register(Wishlist)
admin.site.register(LearningPath)
admin.site.register(CertificateTemplate)
#admin.site.register(Certificate)
admin.site.register(Prerequisite)
from django.contrib import admin
from .models import *


class What_you_learn_TublerInline(admin.TabularInline):
    model = What_you_learn


class Requirements_TublerInline(admin.TabularInline):
    model = Requirements


class What_you_learn_image_TublerInline(admin.TabularInline):
    model = What_you_learn_image

class Who_should_attend_TublerInline(admin.TabularInline):
    model = Who_should_attend

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views', 'likes', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (What_you_learn_TublerInline, Requirements_TublerInline, 
               What_you_learn_image_TublerInline, Who_should_attend_TublerInline)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(What_you_learn_image)
admin.site.register(Who_should_attend)
admin.site.register(Review)


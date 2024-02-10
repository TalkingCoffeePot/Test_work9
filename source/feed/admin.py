from django.contrib import admin
from accounts.models import Profile
from feed.models import PostModel, CommentModel, Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]

@admin.register(PostModel)
class PPostAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'author',
        'image',
    ]

@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'get_author',
        'post_model',
        'text',
        'date_add',
        'date_edit',
    ]
    @admin.display(ordering='author__username')
    def get_author(self, obj):
        return Profile.objects.get(username=obj.author).id
    @admin.display(ordering='product__title')
    def get_product(self, obj):
        return PostModel.objects.get(id=obj.post_model).id
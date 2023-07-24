from django.contrib import admin

from .models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    readonly_fields = ('id',)
    extra = 1


def short_post_body(obj):
    if obj.body:
        return obj.body[:20]
    return '-'

def post_images_count(obj):
    return obj.images.count()

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    list_display = ['id', short_post_body, post_images_count, 'created_at']
    readonly_fields = ('created_at',)

from django.contrib import admin

from .models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    readonly_fields = ('id',)
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    list_display = ['id', 'description', 'created_at']
    readonly_fields = ('created_at',)

    def description(self, obj):
        return obj.body[:50]

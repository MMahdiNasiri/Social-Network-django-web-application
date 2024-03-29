from django.contrib import admin

# Register your models here.
from .models import Post, PostLike


class PostLikeAdmin(admin.TabularInline):
    model = PostLike


class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin]

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)



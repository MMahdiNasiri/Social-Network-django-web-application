from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Hashtag(models.Model):
    name = models.CharField(max_length=25)


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "username": self.user.username,
        }


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    parent = models.ForeignKey("self", null=True,
                               on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="posts")
    likes = models.ManyToManyField(User, related_name='post_user',
                                   blank=True, through=PostLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True,
                                     related_name='post_hashtag')

    class Meta:
        ordering = ['-id']

    @property
    def is_repost(self):
        return self.parent != None

    def serialize(self):
        data = {
            "id": self.id,
            "content": self.content,
            "likes": PostLike.objects.filter(post=self).count(),
            "username": self.user.username,
            "name": self.user.get_full_name(),
            "profile_img": self.user.profile.profileImage.url,
            "parent": self.parent.serialize() if self.parent else None
        }
        if self.image:
            data["post_img"] = self.image.url
        return data


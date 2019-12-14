from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __repr__(self):
        return f'Category({self.name})'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __repr__(self):
        return f'Tag({self.name})'

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __repr__(self):
        return f'Post({self.title}, {self.author}, {self.date})'

    def __str__(self):
        return f'{self.title} by {self.author} at {self.date}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Comment({self.author}, {self.date}, {self.post.title}, {self.post.author})'

    def __str__(self):
        return f'{self.author} at {self.date} on {self.post.title} by {self.post.author}'

from rest_framework import serializers

from .models import Category, Tag, Post, Comment


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['pk', 'name']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'title', 'content', 'date', 'category', 'tags']
        read_only_fields = ['date']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'post', 'content', 'date']
        read_only_fields = ['date']

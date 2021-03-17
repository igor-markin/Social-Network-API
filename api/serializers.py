from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post, User


class GroupSerializer(ModelSerializer):
    class Meta:
        fields = ('title',)
        model = Group


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        exclude = ('group',)
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True,
                            default=CurrentUserDefault())
    following = SlugRelatedField(slug_field='username',
                                 queryset=User.objects.all())

    def validate(self, attrs):
        if self.context['request'].user == attrs.get('following'):
            raise ValidationError('Нельзя подписываться на себя!')
        return attrs

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

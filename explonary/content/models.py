from django.db import models
from .constants import LANGUAGES
from user.models import User
from django.db.models import Q
from django.db.models import Count
from user.utils import generate_random_code
# Create your models here.


def generate_random():
    generate_random_code(6)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_tags(cls, data):
        return Tag.objects.annotate(
            word_count=Count("word")).order_by(
                '-word_count'
            ).all()

    @classmethod
    def get_tag(cls, name):
        name = name.replace(' ', '_')
        name = name.replace('-', '_')
        name = name.replace('ـ', '_')
        tag = Tag.objects.filter(name=name).first()
        if not tag:
            tag = Tag(
                name=name
            )
            tag.save()
        return tag


class TagFollow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tag_follow_user'
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_follow_tag'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    @classmethod
    def follow_tag(cls, user, tag):
        tag_follow = TagFollow.objects.filter(
            user=user,
            tag=tag
        ).first()
        if not tag_follow:
            tag_follow = TagFollow(
                user=user,
                tag=tag
            )
            tag_follow.save()
        return tag_follow

    @classmethod
    def unfollow_tag(cls, user, tag):
        TagFollow.objects.filter(
            user=user,
            tag=tag
        ).delete()
        return True


class Word(models.Model):
    text = models.CharField(max_length=500)
    description = models.CharField(max_length=2000, null=True, blank=True)
    language = models.CharField(max_length=5, choices=LANGUAGES)
    tags = models.ManyToManyField(Tag, related_name='word', blank=True)
    random = models.CharField(max_length=10, default=generate_random)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='word_owner'
    )
    translation_of = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='word_translation'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.text

    @classmethod
    def get_words(cls, data):
        query = {}
        if 'text' in data:
            query['text__icontains'] = data['text']
        if 'owner' in data:
            query['owner'] = data['owner']
        if 'owner_username' in data:
            query['owner__username'] = data['owner_username']
        if 'description' in data:
            query['description__icontains'] = data['description']
        if 'tags' in data:
            tags = Tag.objects.filter(name__in=data['tags']).all()
            query['tags__in'] = tags
        words = Word.objects.filter(**query).all()
        return words

    @classmethod
    def get_word(cls, id, random):
        return Word.objects.filter(
            id=id,
            random=random
        ).first()

    @classmethod
    def get_related_words(cls, word):
        return Word.filter(~Q(id=word.id), tags__in=word.tags).annotate(
            num_matches=Count('tags')).all()

    @classmethod
    def add_word(cls, text,
                 description,
                 language,
                 owner,
                 tags=[],
                 translation_of_id=None):
        new_word = Word(
            text=text,
            owner=owner,
            description=description,
            language=language,
        )

        if translation_of_id:
            word = Word.objects.filter(id=translation_of_id).first()
            if not word:
                raise ValueError
            new_word.translation_of = word
        new_word.save()

        if tags:
            tags_object = []
            for item in tags:
                tags_object.append(Tag.get_tag(item))
            if tags_object:
                new_word.tags.set(tags_object)
        new_word.save()

        return new_word

    @classmethod
    def update(cls, word, data):
        if 'text' in data:
            word.text = data['text']
        if 'description' in data:
            word.description = data['description']
        if 'tags' in data and data['tags']:
            tags = Tag.objects.filter(name__in=data['tags']).all()
            if tags:
                word.tags = tags
        if 'translation_of_id' in data:
            word = Word.objects.filter(id=data['translation_of_id']).first()
            if not word:
                raise ValueError
            word.translation_of = word
        word.save()
        return word

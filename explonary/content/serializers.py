from rest_framework import serializers
from .models import Tag, Word
from .constants import LANGUAGE_CODES


class RequestWordListGet(serializers.Serializer):
    text = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    owner_username = serializers.IntegerField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, default=None
    )
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=50)


class RequestWordItemGet(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    random = serializers.IntegerField(required=True)


class RequestWordAddPost(serializers.Serializer):
    text = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, default=None
    )
    translation_of_id = serializers.IntegerField(required=False)
    language = serializers.ChoiceField(required=True, choices=LANGUAGE_CODES)


class ResponseWord(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class ResponseTag(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from content.models import Word, Tag
from rest_framework.permissions import IsAuthenticated
from .constants import LANGUAGE_LIST
# Create your views here.


class WordListView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseWord(many=True)
        },
        tags=[
            "Content"
        ],
        operation_summary='Word List',
        query_serializer=serializers.RequestWordListGet
    )
    def get(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestWordListGet(
            data=request.query_params
        )
        if serializer.is_valid():
            words = Word.get_words(
                serializer.validated_data
            )
            return Response(
                {
                    'words': serializers.ResponseWord(
                        words, many=True,
                    ).data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class WordItemView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseWord(many=True)
        },
        tags=[
            "Content"
        ],
        operation_summary='Word Item',
        query_serializer=serializers.RequestWordItemGet
    )
    def get(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestWordItemGet(
            data=request.query_params
        )
        if serializer.is_valid():
            words = Word.get_word(
                serializer.validated_data['id'],
                serializer.validated_data['random'],
            )
            return Response(
                {
                    'words': serializers.ResponseWord(
                        words, many=True,
                    ).data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class WordAddView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseWord(many=False)
        },
        tags=[
            "Content"
        ],
        operation_summary='Add Word',
        query_serializer=serializers.RequestWordAddPost
    )
    def post(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestWordAddPost(
            data=request.data
        )
        if serializer.is_valid():
            word = Word.add_word(
                serializer.validated_data['text'],
                serializer.validated_data['description'],
                serializer.validated_data['language'],
                request.user,
                serializer.validated_data['tags'],
                serializer.validated_data['translation_of_id']
            )
            return Response(
                serializers.ResponseWord(
                    word, many=False,
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TagListView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseTag(many=True)
        },
        tags=[
            "Content"
        ],
        operation_summary='Tag List',
    )
    def get(self, request, version=1, *args, **kwargs):
        tags = Tag.get_tags()
        return Response(
            {
                'tags': serializers.ResponseTag(
                    tags, many=True,
                ).data
            },
            status=status.HTTP_200_OK
        )


class LanguageListView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseTag(many=True)
        },
        tags=[
            "Content"
        ],
        operation_summary='Language List',
    )
    def get(self, request, version=1, *args, **kwargs):
        return Response(
            {
                'languages': LANGUAGE_LIST
            },
            status=status.HTTP_200_OK
        )

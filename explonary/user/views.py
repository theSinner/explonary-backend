from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from user.models import User
from rest_framework.permissions import IsAuthenticated
from user import tasks
from user.utils import generate_random_code
from django.core.cache import cache
# Create your views here.


class UserAuthView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Login',
        query_serializer=serializers.RequestUserAuthPost
    )
    def post(self, request, version=1, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response(
                {
                    "message": "User not found."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                serializers.ResponseProfile(
                    request.user, many=False,
                ).data,
                status=status.HTTP_200_OK
            )

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Register',
        query_serializer=serializers.RequestUserAuthPut
    )
    def put(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserAuth(
            data=request.query_params
        )
        if serializer.is_valid():
            user = User.get_user(
                username=serializer.validated_data['username']
            )
            if not user:
                user = User.get_user(
                    email=serializer.validated_data['email']
                )

            if user:
                return Response(
                    {
                        "message": "Email/username is already exists."
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            else:
                user = User.add_user(
                    serializer.validated_data['username'],
                    serializer.validated_data['fullname'],
                    serializer.validated_data['email'],
                )
                tasks.send_email(
                    user.email,
                    generate_random_code(6),
                    'activation_code'
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserFollowView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Follow',
        query_serializer=serializers.RequestUserFollowBlock
    )
    def post(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserFollowBlock(
            data=request.data
        )
        if serializer.is_valid():
            user = User.get_user(
                username=serializer.validated_data['username']
            )
            if user:
                User.follow_user(
                    request.user,
                    user
                )
                return Response(
                    {

                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "The target user is not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Unfollow',
        query_serializer=serializers.RequestUserFollowBlock
    )
    def delete(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserFollowBlock(
            data=request.query_params
        )
        if serializer.is_valid():
            user = User.get_user(
                username=serializer.validated_data['username']
            )
            if user:
                User.unfollow_user(
                    request.user,
                    user
                )
                return Response(
                    {

                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "The target user is not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserBlockView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Block',
        query_serializer=serializers.RequestUserFollowBlock
    )
    def post(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserFollowBlock(
            data=request.data
        )
        if serializer.is_valid():
            user = User.get_user(
                username=serializer.validated_data['username']
            )
            if user:
                User.block_user(
                    request.user,
                    user
                )
                return Response(
                    {

                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "The target user is not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Unblock',
        query_serializer=serializers.RequestUserFollowBlock
    )
    def delete(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserFollowBlock(
            data=request.query_params
        )
        if serializer.is_valid():
            user = User.get_user(
                username=serializer.validated_data['username']
            )
            if user:
                User.unblock_user(
                    request.user,
                    user
                )
                return Response(
                    {

                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "The target user is not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserItemView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseUserDetail(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='User Item',
        query_serializer=serializers.RequestUserItemGet
    )
    def get(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserItemGet(
            data=request.query_params
        )
        if serializer.is_valid():
            user = User.get_user(
                username=serializer.validated_data['username']
            )

            if user:
                return Response(
                    serializers.ResponseUserDetail(
                        user, many=False,
                    ).data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "User not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Get Profile',
    )
    def get(self, request, version=1, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response(
                {
                    "message": "User is not authenticated."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                serializers.ResponseProfile(
                    request.user, many=False,
                ).data,
                status=status.HTTP_200_OK
            )

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Edit Profile',
        query_serializer=serializers.RequestUserEditPut
    )
    def put(self, request, version=1, user=None, *args, **kwargs):
        serializer = serializers.RequestUserEditPut(
            data=request.data
        )
        if serializer.is_valid():
            request.user = User.update(request.user)
            return Response(
                serializers.ResponseProfile(
                    request.user, many=False,
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


class UserActivateView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
        },
        tags=[
            "User"
        ],
        operation_summary='Activate Request',
        query_serializer=serializers.RequestUserActivateRequestPost
    )
    def post(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserActivateRequestPost(
            data=request.data
        )
        if serializer.is_valid():
            if serializer.validated_data['field'] == 'email':
                verify_code = generate_random_code(6)
                tasks.send_email(
                    request.user.email,
                    verify_code,
                    'activation_code'
                )
                cache.set("user:%d:verify:email" % (
                        request.user.id
                    ),
                    verify_code
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={
        },
        tags=[
            "User"
        ],
        operation_summary='Activate Confirm',
        query_serializer=serializers.RequestUserActivateConfirmPut
    )
    def put(self, request, version=1, *args, **kwargs):
        serializer = serializers.RequestUserActivateConfirmPut(
            data=request.data
        )
        if serializer.is_valid():
            if serializer.validated_data['field'] == 'email':
                verify_code = cache.get(
                    "user:%d:verify:email" % (
                        request.user.id
                    )
                )
                if serializer.validated_data['code'] == verify_code:
                    request.user.verified_email = True
                    request.user.save()
                else:
                    return Response(
                        {
                            "message": "Your entered code is not valid."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

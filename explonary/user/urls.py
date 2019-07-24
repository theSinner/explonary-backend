from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        'auth',
        views.UserAuthView.as_view(),
        name='user_auth'
    ),
    url(
        'item',
        views.UserItemView.as_view(),
        name='user_item'
    ),
    url(
        'profile',
        views.UserProfileView.as_view(),
        name='user_profile'
    ),
    url(
        'activate',
        views.UserActivateView.as_view(),
        name='user_activate'
    ),
]

from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        'word/list',
        views.WordListView.as_view(),
        name='word_list'
    ),
    url(
        'word/item',
        views.WordItemView.as_view(),
        name='word_item'
    ),
    url(
        'word/add',
        views.WordAddView.as_view(),
        name='word_add'
    ),
    url(
        'tag/list',
        views.TagListView.as_view(),
        name='tag_list'
    ),
    url(
        'language/list',
        views.LanguageListView.as_view(),
        name='language_list'
    ),
]

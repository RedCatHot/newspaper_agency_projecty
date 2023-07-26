from django.urls import path

from agency.views import (
    index,
    TopicListView,
    NewspaperListView,
    RedactorListView, NewspaperDetailView, RedactorDetailListView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic-list"
    ),

    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list"
    ),


    path(
        "redactors/",
        RedactorListView.as_view(),
        name="redactor-list"
    ),
    path(
        "newspapers/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail"
    ),

    path(
        "redactors/<int:pk>/",
        RedactorDetailListView.as_view(),
        name="redactor-detail"
    ),
]

app_name = "newspaper"

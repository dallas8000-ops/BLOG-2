from django.urls import path

from .views import (
    PostArchivedListView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostDraftListView,
    PostListView,
    PostUpdateView,
    combined_post_list_detail,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('list/', PostListView.as_view(), name='post_list_legacy'),
    path('browse/', combined_post_list_detail, name='post_browse'),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('archived/', PostArchivedListView.as_view(), name='post_archived_list'),
]

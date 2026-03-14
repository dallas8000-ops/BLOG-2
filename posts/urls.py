from django.urls import path

from .views import (
    PostListView, PostUpdateView, PostDeleteView,
    PostDraftListView, PostArchivedListView, combined_post_list_detail
)

urlpatterns = [
    path('', combined_post_list_detail, name='post_list'),
    path('list/', combined_post_list_detail, name='post_list'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('archived/', PostArchivedListView.as_view(), name='post_archived_list'),
]

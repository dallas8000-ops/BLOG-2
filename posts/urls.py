from django.urls import path

from .views import (
    PostArchivedListView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostDraftListView,
    PostListView,
    PostUpdateView,
    toggle_post_status,
    add_comment,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/toggle-status/', toggle_post_status, name='toggle_post_status'),
    path('<int:pk>/comment/', add_comment, name='add_comment'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('archived/', PostArchivedListView.as_view(), name='post_archived_list'),
]

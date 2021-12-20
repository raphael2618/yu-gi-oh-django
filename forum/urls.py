from django.urls import path
from .views import ForumView, ForumCreate, ForumUpdateView, ForumUserListView, ForumDetailView, ForumDeleteView, \
    CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', ForumView.as_view(), name='forum'),
    path('add/', ForumCreate.as_view(), name='forum-add'),  # need to be before slug
    path('edit/<int:pk>', ForumUpdateView.as_view(), name='forum-edit'),
    path('delete/<int:pk>', ForumDeleteView.as_view(), name='forum-delete'),
    path('<slug:slug>/', ForumDetailView.as_view(), name='forum-detail'),
    path('by/<username>/', ForumUserListView.as_view(), name='forum-user'),
    path('add-comment/<int:pk>', CommentCreateView.as_view(), name='add-comment'),
    path('edit-comment/<int:pk>', CommentUpdateView.as_view(), name='edit-comment'),
    path('delete-comment/<int:pk>', CommentDeleteView.as_view(), name='delete-comment'),
]

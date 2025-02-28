from django.urls import path, include
from rest_framework_nested import routers
from book.views import CategoryViewSet, BookViewSet, AuthorViewSet, BorrowRecordViewSet, MemberViewSet


router = routers.DefaultRouter()


router.register('categories', CategoryViewSet)
router.register('books', BookViewSet, basename='Books')
router.register('author', AuthorViewSet, basename='author')
router.register('borrow', BorrowRecordViewSet, basename='borrow')
router.register('members', MemberViewSet, basename='members')





urlpatterns = [
    path('', include(router.urls)),
]

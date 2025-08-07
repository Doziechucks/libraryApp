
from django.urls import path, include
from . import views
from rest_framework_nested import routers

from .views import BookImageViewSet

router = routers.DefaultRouter()
# router = routers.SimpleRouter()
router.register('books', views.BookViewSet, basename='books')
router.register('images', BookImageViewSet, basename='book-images')

book_image_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
book_image_router.register('images', BookImageViewSet, basename='book-images')

print(router.urls)

urlpatterns = [

    # path("", views.get_books),
    # # path('/greet/<name>', views.greet),
    # path('authors/',views.add_author, name="add_author"),
    # path('get/authors/',views.get_authors, name="get_authors"),
    #
    # path('update/authors/<int:pk>/', views.update_author, name="update_author"),
    # path('delete/authors/<int:pk>/', views.delete_author, name="delete_author"),

    path('', include(router.urls)),
    path('', include(book_image_router.urls)),
    path('authors/', views.AddAuthorView.as_view(), name='add_author'),
    path('authors/<int:pk>/', views.GetUpdateDeleteAuthorView.as_view(), name='get_update_and_delete'),
    path("images/<int:pk>/", views.image_detail, name="book-images-detail"),
    path("borrow-book/<int:pk>/", views.borrow_book, name="borrow_book"),
]
from gc import get_objects

from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Author, BookImage, BookInstance
from .serializers import BookSerializer, AuthorSerializer, AddBookSerializer, BookImageSerializer, \
    BookInstanceSerializer


# Create your views here.
@api_view()
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_author(request):
    author = AuthorSerializer(data=request.data)
    author.is_valid(raise_exception=True)
    author.save()
    return Response(author.data, status=status.HTTP_201_CREATED)

@api_view()
def get_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_author(request, pk):
    author = Author.objects.get(pk=pk)
    serializer = AuthorSerializer(author, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_author(request, pk):
    author = Author.objects.get(pk=pk)
    author.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def greet(request, name):
    return render(request, 'index.html', context={'name': name})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AddBookSerializer
        elif self.request.method == 'POST':
            return AddBookSerializer
        return BookSerializer

@api_view(['GET'])
def image_detail(request, pk):
    book_image = get_object_or_404(BookImage, pk=pk)
    serializer = BookImageSerializer(book_image)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AddAuthorView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GetUpdateDeleteAuthorView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookImageViewSet(viewsets.ModelViewSet):

    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_pk")
        if not book_id:
            raise ValueError("book_id is missing in kwargs")
        serializer.save(book_id=book_id)

    # def get_serializer_class(self):
    #     return {'book_id': self.kwargs['book_pk']}

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user
    data = BookInstanceSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    BookInstance.objects.create(
        user = user,
        book = book,
        return_date = data.validated_data['return_date'],
        comments = data.validated_data['comments']
    )
    subject = "Notification from Library DozieLibrary"
    message = f"""The request to borrow {book.title} was successful."""
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    try:
        send_mail(subject = subject,
                  message=message,
                  from_email=from_email,
                  recipient_list = recipient_list
                  )
    except smiplib.SMTPAuthenticationError:
        return Response('message': f())


    send_mail(message=message, from_email=from_email, , subject=subject)
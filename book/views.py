from django.shortcuts import render
from rest_framework.viewsets  import ModelViewSet
from book.models import Category, Book, Author, BorrowRecord
from users.models import User
from book.serializers import CategorySerializer, BookSerializer, AuthorSerializer, ReturnSerializer, BorrowRecordReadSerializer, BorrowRecordWriteSerializer, MemberSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework import permissions
from api.permissions import IsAdminOrReadOnly
# Create your views here.


class CategoryViewSet(ModelViewSet):
    '''
    API For Managing Category in the Library Management System
     - Managing Categories for Book's 
     - Only Admin Can Create, Update, and Delete
     - Normal User / Member's can Read 
    
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
class BookViewSet(ModelViewSet):
    '''
    API For Managing Book's in the Library Management System
     - Managing Book's
     - Only Admin Can Create, Update, and Delete Books.
     - Normal User / Member's can Read, 
     - Authenticated user can borrow book's and after reading they can Return also.
    
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class AuthorViewSet(ModelViewSet) :
    '''
    API For Managing Book's Author in the Library Management System
     - Managing Book's Author
     - Only Admin Can Create, Update, and Delete Author. 
    '''
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class BorrowRecordViewSet(ModelViewSet):
    '''
    API For Book's Borrow and Return in the Library Management System
     - Member Can Borrow Book's 
     - After Reading Member Can Return the Book's
    '''
    queryset = BorrowRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
           
            return BorrowRecordWriteSerializer
        
        return BorrowRecordReadSerializer
    
    def perform_create(self, serializer):
        serializer.save(return_date=None)
        
    @action(detail=True, methods=['get', 'post'], url_path='return')
    def return_book(self, request, pk=None):
        try:
            borrow_record = self.get_object() 
            
           
            if borrow_record.return_date is not None:
                return Response(
                    {"detail": "This book has already been returned."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            
            borrow_record.return_date = timezone.now().date()
            borrow_record.save()

            
            serializer = ReturnSerializer(borrow_record)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except BorrowRecord.DoesNotExist:
            return Response(
                {"detail": "Borrowing record not found."},
                status=status.HTTP_404_NOT_FOUND
            )



class MemberViewSet(ModelViewSet):
    '''
    API For Managing All The User in the Library Management System
     - Only Admin can visit this Route or View Set
     - Only Admin can Delete and Update Member's or user.
    '''
    queryset = User.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAdminUser]


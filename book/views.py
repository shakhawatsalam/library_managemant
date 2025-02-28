from django.shortcuts import render
from rest_framework.viewsets  import ModelViewSet
from book.models import Category, Book, Author, BorrowRecord
from users.models import User
from book.serializers import CategorySerializer, BookSerializer, AuthorSerializer, ReturnSerializer, BorrowRecordReadSerializer, BorrowRecordWriteSerializer, MemberSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class AuthorViewSet(ModelViewSet) :
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class BorrowRecordViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.all()
    
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
    queryset = User.objects.all()
    serializer_class = MemberSerializer


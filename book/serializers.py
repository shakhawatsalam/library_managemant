from rest_framework import serializers
from book.models  import Book, Category, Author, BorrowRecord
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'availability', 'quantity', 'available_copies', 'category']
        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']
        
        
        
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']   
        
            

class BorrowRecordWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'member', 'borrow_date', 'return_date']
        read_only_fields = ['borrow_date', 'return_date']


class BorrowRecordReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'member', 'borrow_date', 'return_date']





            
class ReturnSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'member', 'borrow_date', 'return_date']
        read_only_fields = ['book', 'member', 'borrow_date']
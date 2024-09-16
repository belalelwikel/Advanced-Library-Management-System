from rest_framework import viewsets
from ..models import Borrowing
from .serializers import BorrowingSerializer, ReturnSerializer
from lms.book.models import BookLibrary
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.views import APIView

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related('user', 'book__book', 'book__library')
    serializer_class = BorrowingSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        book_data = request.data.get('books')  # Expecting a list of books with return dates

        if not book_data:
            return Response({'error': 'You must provide books with return dates.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(book_data) > 3:
            return Response({'error': 'Cannot borrow more than 3 books.'}, status=status.HTTP_400_BAD_REQUEST)

        active_borrowings = Borrowing.objects.filter(user=user, returned=False)
        current_borrowed_count = active_borrowings.count()
         
        books_to_borrow = len(book_data)
        if current_borrowed_count + books_to_borrow > 3:
            return Response({'error': f'You have already borrowed {current_borrowed_count} books. You can only borrow {3 - current_borrowed_count} more.'}, status=status.HTTP_400_BAD_REQUEST)

        borrowings_created = []

        for book in book_data:
            book_id = book.get('book_id')
            return_date = book.get('return_date')

            if not return_date:
                return Response({'error': f'Return date is required for book ID {book_id}.'}, status=status.HTTP_400_BAD_REQUEST)

            if return_date > (timezone.now() + timedelta(days=30)).date():
                return Response({'error': f'Return date for book ID {book_id} cannot exceed 1 month.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                book_library = BookLibrary.objects.get(id=book_id)
                if not book_library.available:
                    return Response({'error': f'{book_library.book.title} is not available.'}, status=status.HTTP_400_BAD_REQUEST)

                borrowing = Borrowing.objects.create(
                    user=user,
                    book=book_library,
                    return_date=return_date
                )
                borrowings_created.append(borrowing)

                book_library.available = False
                book_library.save()

            except BookLibrary.DoesNotExist:
                return Response({'error': f'Book with ID {book_id} not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            [BorrowingSerializer(borrowing).data for borrowing in borrowings_created],
            status=status.HTTP_201_CREATED
        )

from rest_framework.permissions import AllowAny

class ReturnAPIView(APIView):
    
    def post(self, request, pk=None):


        try:
            borrowing = Borrowing.objects.get(pk=pk, returned=False)
        except Borrowing.DoesNotExist:
            return Response({'error': 'Borrowing record not found or already returned.'}, status=status.HTTP_404_NOT_FOUND)

        # Mark the borrowing as returned
        borrowing.returned = True
        borrowing.save()

        # Mark the book as available
        book_library = borrowing.book
        book_library.available = True
        book_library.save()

        # Calculate any overdue penalties
        penalty = borrowing.calculate_penalty()
        response_data = {'message': 'Book returned successfully.'}

        if penalty > 0:
            response_data['penalty'] = penalty

        # Send WebSocket notification to notify users that the book is available
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",  # WebSocket group
            {
                "type": "notify_book_available",
                "book_title": book_library.book.title
            }
        )

        # Use the serializer for the response
        serializer = ReturnSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
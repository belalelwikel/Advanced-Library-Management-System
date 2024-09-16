from rest_framework import serializers
from ..models import Borrowing
class BorrowingSerializer(serializers.ModelSerializer):
    penalty = serializers.SerializerMethodField()
    class Meta:
        model = Borrowing
        fields = ['user', 'book', 'borrow_date', 'return_date', 'returned', 'penalty']

    def get_penalty(self, obj):
        return obj.calculate_penalty()

class ReturnSerializer(serializers.Serializer):
    message = serializers.CharField()
    penalty = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
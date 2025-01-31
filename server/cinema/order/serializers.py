from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    showing_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [ 'id', 'user', 'showing', 'showing_details', 'seats', 'eats', 'total_price', 'created_at', 'updated_at' ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_showing_details(self, obj):
        return {
            "movie": obj.showing.movie.title,
            "date": obj.showing.date,
            "time": obj.showing.time,
        }

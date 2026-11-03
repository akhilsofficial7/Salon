from rest_framework import serializers
from salon_app.models import StylistDb, BookingDb

class Stylist_Serializer(serializers.ModelSerializer):
    class Meta:
        model = StylistDb
        fields = "__all__"
        read_only_fields = ["id"]


class Booking_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDb
        fields = "__all__"
        read_only_fields = ["id"]

    def validate(self, validated_data):
        phone = validated_data.get("phone") 
        booking_date = validated_data.get("booking_date")

        if BookingDb.objects.filter(
            phone=phone,
            booking_date=booking_date).exists():
            raise serializers.ValidationError("Already Booked")
        else:
            return validated_data
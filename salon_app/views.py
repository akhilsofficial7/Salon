from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from salon_app.models import StylistDb, BookingDb
from salon_app.serializers import Stylist_Serializer, Booking_Serializer
from datetime import time, timedelta, datetime
from rest_framework import serializers

# Create your views here.

class StylistListCreateView(APIView):
    def get(self, request):
        qs = StylistDb.objects.all()
        serializer_instance = Stylist_Serializer(qs, many=True)
        return Response(data=serializer_instance.data)
        
    def post(self, request):
        form_data = request.data
        serializer_instance = Stylist_Serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class StylistRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(StylistDb, id=pk)
        serializer_instance = Stylist_Serializer(qs)
        return Response(data=serializer_instance.data)
        
    def put(self, request, pk):
        form_data = request.data
        stylist_object = get_object_or_404(StylistDb, id=pk)
        serializer_instance = Stylist_Serializer(data=form_data, instance=stylist_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self, request, pk):
        stylist_obj = get_object_or_404(StylistDb, id=pk)
        stylist_obj.delete()
        return Response(data={
            "Message": "deleted..!"
        })


class BookingListCreateView(APIView):
    def get(self, request):
        qs = BookingDb.objects.all()
        serializer_instance = Booking_Serializer(qs, many=True)
        return Response(data=serializer_instance.data)

    def post(self, request):
        form_data = request.data
        serializer_instance = Booking_Serializer(data=form_data)
        if serializer_instance.is_valid():
        
            booking_date = serializer_instance.validated_data.get("booking_date")
            stylist_id = serializer_instance.validated_data.get("stylist_id")
            
            last_booking = BookingDb.objects.filter(
                booking_date=booking_date,
                stylist_id=stylist_id
            ).order_by("-token_number").first()

            if last_booking is None:
                form_data["token_number"] = 1
                form_data["booking_time"] = time(10, 0)
            else:
                form_data["token_number"] = last_booking.token_number + 1
                current_time = datetime.combine(booking_date, last_booking.booking_time)
                next_time = current_time + timedelta(minutes=15)

                ### Adding Break / Lunch Time
                if next_time.time() == time(10, 30):
                    next_time = datetime.combine(booking_date, time(13, 30))

                # Slot Completion Check
                if next_time.time() == time(10, 30):
                    raise serializers.ValidationError("No slot Available Today")

                form_data["booking_time"] = next_time.time()
                
            qs = BookingDb.objects.create(**form_data)
            serializer_instance = Booking_Serializer(qs)
            return Response(data={
                "status": "Booked_Successfully...",
                "token_number": form_data["token_number"],
                "booking_time": form_data["booking_time"]
            })
        else: 
            return Response(data=serializer_instance.errors)
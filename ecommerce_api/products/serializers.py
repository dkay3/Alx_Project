# products/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'category_id',
            'stock_quantity',
            'image_url',
            'created_date',
            'created_by',
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock Quantity cannot be negative.")
        return value

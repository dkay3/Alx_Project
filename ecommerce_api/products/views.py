# products/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Category, Product
from .serializers import UserSerializer, CategorySerializer, ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse



def landing_page_view(request, *args, **kwargs):
    return HttpResponse("Welcome to the landing page!")

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    Only admin users can perform CRUD operations on users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'price', 'stock_quantity']
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'created_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='search')
    def search_products(self, request):
        """
        Custom action to search products by name or category with partial matches.
        """
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        products = self.queryset

        if query:
            products = products.filter(name__icontains=query)
        if category:
            products = products.filter(category__name__icontains=category)

        # Apply filters
        filtered = self.filter_queryset(products)

        page = self.paginate_queryset(filtered)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered, many=True)
        return Response(serializer.data)


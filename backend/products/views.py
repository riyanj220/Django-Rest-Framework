from rest_framework.response import Response
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET","POST"])
def product_alt_view(request, pk = None,*args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)

        queryset = Product.objects.all()
        data = ProductSerializer(queryset,many = True).data
        return Response(data)
    
    if method == "POST":

        serializer = ProductSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')

            if content is  None:
                content = title
            
            serializer.save(content = content)

             
        return Response(serializer.data)
    

from rest_framework.response import Response
from rest_framework import generics , mixins , permissions , authentication
from .models import Product
from .serializers import ProductSerializer

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .permissions import IsStaffEditorPermissions

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes =[IsStaffEditorPermissions]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes =[IsStaffEditorPermissions]

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self,serializer):
        instance = serializer.save()

        if not instance.content:
            instance.content = instance.title


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_delete(self,instance):
        super().perform_delete(instance)


class ProductMixinView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, 
                       generics.GenericAPIView,
                       mixins.CreateModelMixin):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self,request,*args, **kwargs):
        print(args,kwargs)
        pk = kwargs.get('pk')

        if pk is not None:
            return self.retrieve(request,*args, **kwargs)

        return self.list(request,*args, **kwargs)

    def post(self, request,*args, **kwargs):
        return self.create(request,*args, **kwargs)

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
    


from rest_framework.response import Response
from rest_framework import generics , mixins   #authentication , permissions
from .models import Product
from .serializers import ProductSerializer

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

# from api.permissions import IsStaffEditorPermissions

# from api.authentication import TokenAuthentication

from api.mixins import StaffEditorPermissionsMixins

class ProductCreateAPIView(StaffEditorPermissionsMixins,generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    ''' authentication_classes = [authentication.SessionAuthentication,
                               authentication.TokenAuthentication] 
                               since we already defined this default in settings

    permission_classes =[IsStaffEditorPermissions] 
                        since we created custom mixins and included that in our view
    '''
class ProductDetailAPIView(StaffEditorPermissionsMixins,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes =[IsStaffEditorPermissions]

class ProductListCreateAPIView(StaffEditorPermissionsMixins,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [authentication.SessionAuthentication,
    #                           TokenAuthentication]
    # permission_classes =[IsStaffEditorPermissions]

    def perform_create(self, serializer):
        # email = serializer.validated_data.pop('email')
        # print(email)
        title = serializer.validated_data.pop('title')
        content = serializer.validated_data.pop('content') or None

        if content is None:
            content = title

        serializer.save(content = content) # its like form.save() 


class ProductUpdateAPIView(StaffEditorPermissionsMixins,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes =[IsStaffEditorPermissions]

    def perform_update(self,serializer):
        instance = serializer.save()

        if not instance.content:
            instance.content = instance.title


class ProductDeleteAPIView(StaffEditorPermissionsMixins,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes =[IsStaffEditorPermissions]

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
    


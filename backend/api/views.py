from products.models import Product

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.serializers import ProductSerializer 

@api_view(["POST"])
def api_home(request,*args,**kwargs):

    """
    This is DRF API VIEW
    """

    serializer = ProductSerializer(data = request.data)

    if serializer.is_valid():
        instance = serializer.save()
        print(instance)
        
    return Response(serializer.data)


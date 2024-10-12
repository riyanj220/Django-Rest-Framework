from django.urls import path
from .views import *

urlpatterns = [
    path('',ProductCreateAPIView.as_view(),name= 'product_create_api_view'),

    path('<int:pk>/',ProductDetailAPIView.as_view(),name= 'product_detail_api_view'),
    path('<int:pk>/update',ProductUpdateAPIView.as_view(),name= 'product_detail_api_view'),
    path('<int:pk>/delete',ProductDeleteAPIView.as_view(),name= 'product_detail_api_view'),

    path('list/',ProductListCreateAPIView.as_view(),name= 'product_list_api_view'),

    # path('<int:pk>/',product_alt_view,name= 'product_detail_api_view'),
    # path('',product_alt_view,name= 'product_create_api_view'),
    # path('list/',product_alt_view,name= 'product_list_api_view'),
]
from rest_framework import serializers
from .models import Product


def validate_title(value):
    if Product.objects.filter(title__iexact = value).exists():
        raise serializers.ValidationError(f"{value} is already a product name")
    return value
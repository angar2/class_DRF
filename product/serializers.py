from rest_framework import serializers
from product.models import Product as ProductModel

class ProductSerializer(serializers.ModelSerializer):

    def validate(self, data):

        return data

    def create(self, validated_data):

        product = ProductModel(**validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = ProductModel
        fields = ['author','title','thumbnail', 'description', 'post_date','start_date','end_date']

        
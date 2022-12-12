from products.models import Product, ProductLabel
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class ProductLabelSerializer(ModelSerializer):
    class Meta:
        model=ProductLabel
        fields=["name",
                "value"]

class ProductSerializer(ModelSerializer):
    labels = ProductLabelSerializer(many=True)
    product_id=serializers.PrimaryKeyRelatedField(read_only=True)
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)
    out_of_stock= serializers.BooleanField(source="get_out_of_stock", read_only=True)
    available_stock= serializers.IntegerField(source="get_available_stock_quantity", read_only= True)
    class Meta:
        model=Product
        fields=["name",
                "category",
                "quantity",
                "price",
                "labels",
                "created_at",
                "updated_at",
                "product_id",
                "out_of_stock",
                "available_stock"
                ]

    def create(self, validated_data):
        label_dict= validated_data.pop('labels')
        instance = Product.objects.create(**validated_data)
        for label in label_dict:
            l=dict(label)
            new_label = ProductLabel.objects.create(**l)
            instance.labels.add(new_label)
        return instance

    def update(self, instance, validated_data):
        try:
            labels_data = validated_data.pop('labels')
            objects_to_delete = ProductLabel.objects.filter(pk__in=[o.pk for o in instance.labels.all()])
            objects_to_delete.delete()
            labels=[]
            for label in labels_data:
                l=dict(label)
                new_label = ProductLabel.objects.create(**l)
                labels.append(new_label)
            instance.labels.set(labels, clear=False)
        except :
            pass
        print(instance)
        instance = super().update(instance, validated_data)
        return instance


class AllProductResponse(serializers.Serializer):
    products = ProductSerializer(many=True)
    message=serializers.CharField(required=False)

class ProductResponse(serializers.Serializer):
    product = ProductSerializer()
    message=serializers.CharField(required=False)

class ErrorResponse(serializers.Serializer):
    errors = serializers.ListField()

class MessageResponse(serializers.Serializer):
    message=serializers.CharField(required=False)
from rest_framework import serializers

from apps.products.models import Category, Image, Product


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image",)


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(read_only=True, source="parent")

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent_id")


class ProductReadSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    category = CategorySerializer()
    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        depth = 1
        fields = (
            "id",
            "user",
            "category",
            "sku",
            "name",
            "brand",
            "price",
            "wholesale_quantity",
            "video",
            "quantity_in_stock",
            "description",
            "manufacturer_country",
            "images",
        )


class ProductWriteSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), required=True)

    class Meta:
        model = Product
        fields = (
            "category",
            "sku",
            "name",
            "brand",
            "price",
            "wholesale_quantity",
            "quantity_in_stock",
            "description",
            "manufacturer_country",
            "video",
            "images",
        )

    def create_or_update_product(self, validated_data, instance=None):
        product = instance if instance else Product()
        image_list = validated_data.pop("images", None)
        for key, val in validated_data.items():
            setattr(product, key, val)
        product.save()
        if image_list:
            product.images.all().delete()
            for image in image_list:
                Image.objects.create(product=product, image=image)
        return product

    def create(self, validated_data):
        return self.create_or_update_product(validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update_product(validated_data, instance=instance)

    def to_representation(self, instance):
        serializer = ProductReadSerializer(instance)
        return serializer.data
